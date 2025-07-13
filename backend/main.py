import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import socketio
from sqlalchemy.orm import Session
from typing import List
import asyncio
from datetime import datetime, timedelta

from .database import engine, Base, get_db
from . import models, schemas, crud

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app setup
app = FastAPI()

# CORS setup (adjust origins as needed for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO setup
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
app.mount("/ws", socketio.ASGIApp(sio))

game_states = {}

async def next_phase(lobby_id: int, db: Session):
    current_round = crud.get_round_by_lobby_id(db, lobby_id)
    if not current_round:
        return

    if current_round.phase == "product_submission":
        new_phase = "commenting"
        phase_duration = 60  # 60 seconds for commenting
    elif current_round.phase == "commenting":
        new_phase = "voting"
        phase_duration = 30  # 30 seconds for voting
    elif current_round.phase == "voting":
        new_phase = "finished"
        phase_duration = 0
        await calculate_scores(lobby_id, current_round.id, db)
    else:
        return

    crud.update_round_phase(db, current_round.id, new_phase)
    game_states[lobby_id]["current_phase"] = new_phase
    game_states[lobby_id]["phase_end_time"] = datetime.now() + timedelta(seconds=phase_duration)

    await sio.emit("phase_update", {
        "lobby_id": lobby_id,
        "round_id": current_round.id,
        "phase": new_phase,
        "phase_end_time": str(game_states[lobby_id]["phase_end_time"])
    }, room=str(lobby_id))

    if new_phase != "finished":
        asyncio.create_task(start_timer(lobby_id, phase_duration, db))

async def start_timer(lobby_id: int, duration: int, db: Session):
    await asyncio.sleep(duration)
    await next_phase(lobby_id, db)

async def calculate_scores(lobby_id: int, round_id: int, db: Session):
    comments = crud.get_comments_by_round(db, round_id)
    winning_comment = None
    max_votes = -1

    for comment in comments:
        votes_count = crud.get_comment_votes_count(db, comment.id)
        if votes_count > max_votes:
            max_votes = votes_count
            winning_comment = comment

    if winning_comment:
        winner_id = winning_comment.author_id
        winner_user = crud.get_user_by_id(db, winner_id)
        if winner_user:
            new_score = winner_user.score + 10  # Example score increment
            crud.update_user_score(db, winner_id, new_score)
            await sio.emit("round_winner", {
                "lobby_id": lobby_id,
                "round_id": round_id,
                "winner_id": winner_id,
                "winning_comment_id": winning_comment.id,
                "score": new_score
            }, room=str(lobby_id))

async def start_game_round(lobby_id: int, db: Session):
    current_round = crud.get_round_by_lobby_id(db, lobby_id)
    new_round_number = 1
    if current_round:
        new_round_number = current_round.round_number + 1

    # For simplicity, let's assume the first user in the lobby is the current player for product submission
    lobby_members = crud.get_lobby(db, lobby_id).members
    current_player_id = lobby_members[0].user_id if lobby_members else None

    if not current_player_id:
        print(f"No members in lobby {lobby_id} to start a round.")
        return

    new_round = crud.create_round(db=db, round=schemas.RoundCreate(
        lobby_id=lobby_id,
        round_number=new_round_number,
        current_player_id=current_player_id,
        phase="product_submission"
    ))

    game_states[lobby_id] = {
        "current_round_id": new_round.id,
        "current_phase": "product_submission",
        "phase_end_time": datetime.now() + timedelta(seconds=60) # 60 seconds for product submission
    }

    await sio.emit("round_started", {
        "lobby_id": lobby_id,
        "round_id": new_round.id,
        "round_number": new_round.round_number,
        "current_player_id": new_round.current_player_id,
        "phase": new_round.phase,
        "phase_end_time": str(game_states[lobby_id]["phase_end_time"])
    }, room=str(lobby_id))

    asyncio.create_task(start_timer(lobby_id, 60, db))

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Product Review Game Backend!"}

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login/", response_model=schemas.User)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/lobbies/", response_model=schemas.Lobby, status_code=status.HTTP_201_CREATED)
def create_lobby(lobby: schemas.LobbyCreate, db: Session = Depends(get_db)):
    db_lobby = crud.get_lobby_by_name(db, name=lobby.name)
    if db_lobby:
        raise HTTPException(status_code=400, detail="Lobby name already taken")
    return crud.create_lobby(db=db, lobby=lobby)

@app.get("/lobbies/", response_model=List[schemas.Lobby])
def read_lobbies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lobbies = crud.get_lobbies(db, skip=skip, limit=limit)
    return lobbies

@app.post("/lobbies/{lobby_id}/join/{user_id}", response_model=schemas.LobbyMember, status_code=status.HTTP_201_CREATED)
def join_lobby(lobby_id: int, user_id: int, db: Session = Depends(get_db)):
    db_lobby = crud.get_lobby(db, lobby_id=lobby_id)
    if not db_lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_lobby_member = crud.get_lobby_member(db, lobby_id=lobby_id, user_id=user_id)
    if db_lobby_member:
        raise HTTPException(status_code=400, detail="User already in lobby")
    return crud.join_lobby(db=db, lobby_id=lobby_id, user_id=user_id)

@sio.event
async def start_game_ws(sid, data):
    lobby_id = data.get("lobby_id")
    if lobby_id:
        db = next(get_db())
        await start_game_round(lobby_id, db)

@sio.event
async def submit_product_ws(sid, data):
    lobby_id = data.get("lobby_id")
    round_id = data.get("round_id")
    uploader_id = data.get("uploader_id")
    link = data.get("link")
    image_url = data.get("image_url")
    if lobby_id and round_id and uploader_id:
        db = next(get_db())
        new_product = crud.create_product(db=db, product=schemas.ProductCreate(round_id=round_id, uploader_id=uploader_id, link=link, image_url=image_url))
        crud.update_round_product(db=db, round_id=round_id, product_id=new_product.id)
        await sio.emit("product_submitted", schemas.Product.from_orm(new_product).dict(), room=str(lobby_id))
        # Transition to commenting phase immediately after product submission
        await next_phase(lobby_id, db)

@sio.event
async def submit_comment_ws(sid, data):
    lobby_id = data.get("lobby_id")
    round_id = data.get("round_id")
    product_id = data.get("product_id")
    author_id = data.get("author_id")
    content = data.get("content")
    if lobby_id and round_id and product_id and author_id and content:
        db = next(get_db())
        new_comment = crud.create_comment(db=db, comment=schemas.CommentCreate(round_id=round_id, product_id=product_id, author_id=author_id, content=content))
        await sio.emit("comment_submitted", schemas.Comment.from_orm(new_comment).dict(), room=str(lobby_id))

@sio.event
async def submit_vote_ws(sid, data):
    lobby_id = data.get("lobby_id")
    comment_id = data.get("comment_id")
    voter_id = data.get("voter_id")
    if lobby_id and comment_id and voter_id:
        db = next(get_db())
        new_vote = crud.create_vote(db=db, vote=schemas.VoteCreate(comment_id=comment_id, voter_id=voter_id))
        await sio.emit("vote_submitted", schemas.Vote.from_orm(new_vote).dict(), room=str(lobby_id))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
