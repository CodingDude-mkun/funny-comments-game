from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str

class UserLogin(BaseModel):
    username: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class LobbyCreate(BaseModel):
    name: str
    creator_id: int

class Lobby(BaseModel):
    id: int
    name: str
    creator_id: int
    is_active: bool

    class Config:
        orm_mode = True

class LobbyMember(BaseModel):
    id: int
    lobby_id: int
    user_id: int

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    round_id: int
    uploader_id: int
    link: str = None
    image_url: str = None

class Product(BaseModel):
    id: int
    round_id: int
    uploader_id: int
    link: str = None
    image_url: str = None

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    round_id: int
    product_id: int
    author_id: int
    content: str

class Comment(BaseModel):
    id: int
    round_id: int
    product_id: int
    author_id: int
    content: str

    class Config:
        orm_mode = True

class VoteCreate(BaseModel):
    comment_id: int
    voter_id: int

class Vote(BaseModel):
    id: int
    comment_id: int
    voter_id: int

    class Config:
        orm_mode = True

class RoundCreate(BaseModel):
    lobby_id: int
    round_number: int
    current_player_id: int = None

class Round(BaseModel):
    id: int
    lobby_id: int
    round_number: int
    product_id: int = None
    start_time: str
    end_time: str = None
    phase: str
    current_player_id: int = None

    class Config:
        orm_mode = True
