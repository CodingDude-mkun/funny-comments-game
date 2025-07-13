from sqlalchemy.orm import Session

from . import models, schemas

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user_score(db: Session, user_id: int, score: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.score = score
        db.commit()
        db.refresh(db_user)
    return db_user

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_lobby(db: Session, lobby_id: int):
    return db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()

def get_lobby_by_name(db: Session, name: str):
    return db.query(models.Lobby).filter(models.Lobby.name == name).first()

def get_lobbies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lobby).offset(skip).limit(limit).all()

def create_lobby(db: Session, lobby: schemas.LobbyCreate):
    db_lobby = models.Lobby(name=lobby.name, creator_id=lobby.creator_id)
    db.add(db_lobby)
    db.commit()
    db.refresh(db_lobby)
    return db_lobby

def join_lobby(db: Session, lobby_id: int, user_id: int):
    db_lobby_member = models.LobbyMember(lobby_id=lobby_id, user_id=user_id)
    db.add(db_lobby_member)
    db.commit()
    db.refresh(db_lobby_member)
    return db_lobby_member

def get_lobby_member(db: Session, lobby_id: int, user_id: int):
    return db.query(models.LobbyMember).filter(models.LobbyMember.lobby_id == lobby_id, models.LobbyMember.user_id == user_id).first()

def create_round(db: Session, round: schemas.RoundCreate):
    db_round = models.Round(**round.dict())
    db.add(db_round)
    db.commit()
    db.refresh(db_round)
    return db_round

def get_round(db: Session, round_id: int):
    return db.query(models.Round).filter(models.Round.id == round_id).first()

def get_rounds_by_lobby(db: Session, lobby_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Round).filter(models.Round.lobby_id == lobby_id).offset(skip).limit(limit).all()

def update_round_phase(db: Session, round_id: int, phase: str):
    db_round = db.query(models.Round).filter(models.Round.id == round_id).first()
    if db_round:
        db_round.phase = phase
        db.commit()
        db.refresh(db_round)
    return db_round

def update_round_product(db: Session, round_id: int, product_id: int):
    db_round = db.query(models.Round).filter(models.Round.id == round_id).first()
    if db_round:
        db_round.product_id = product_id
        db.commit()
        db.refresh(db_round)
    return db_round

def update_round_end_time(db: Session, round_id: int, end_time):
    db_round = db.query(models.Round).filter(models.Round.id == round_id).first()
    if db_round:
        db_round.end_time = end_time
        db.commit()
        db.refresh(db_round)
    return db_round

def update_round_current_player(db: Session, round_id: int, current_player_id: int):
    db_round = db.query(models.Round).filter(models.Round.id == round_id).first()
    if db_round:
        db_round.current_player_id = current_player_id
        db.commit()
        db.refresh(db_round)
    return db_round

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def get_comments_by_round(db: Session, round_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).filter(models.Comment.round_id == round_id).offset(skip).limit(limit).all()

def create_vote(db: Session, vote: schemas.VoteCreate):
    db_vote = models.Vote(**vote.dict())
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def get_vote(db: Session, vote_id: int):
    return db.query(models.Vote).filter(models.Vote.id == vote_id).first()

def get_votes_by_comment(db: Session, comment_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Vote).filter(models.Vote.comment_id == comment_id).offset(skip).limit(limit).all()

def get_votes_by_voter(db: Session, voter_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Vote).filter(models.Vote.voter_id == voter_id).offset(skip).limit(limit).all()

def get_comment_votes_count(db: Session, comment_id: int):
    return db.query(models.Vote).filter(models.Vote.comment_id == comment_id).count()

def get_round_by_lobby_id(db: Session, lobby_id: int):
    return db.query(models.Round).filter(models.Round.lobby_id == lobby_id).order_by(models.Round.round_number.desc()).first()

