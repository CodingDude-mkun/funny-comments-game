import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from .database import engine, Base

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

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Product Review Game Backend!"}

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("message", f"Welcome, {sid}!", room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def chat_message(sid, data):
    print(f"Received message from {sid}: {data}")
    await sio.emit("message", data)  # Broadcast the message to all connected clients

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
