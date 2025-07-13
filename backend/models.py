from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lobbies_created = relationship("Lobby", back_populates="creator")
    lobby_memberships = relationship("LobbyMember", back_populates="user")
    products = relationship("Product", back_populates="uploader")
    comments = relationship("Comment", back_populates="author")
    votes = relationship("Vote", back_populates="voter")

class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    creator = relationship("User", back_populates="lobbies_created")
    members = relationship("LobbyMember", back_populates="lobby")
    rounds = relationship("Round", back_populates="lobby")

class LobbyMember(Base):
    __tablename__ = "lobby_members"

    id = Column(Integer, primary_key=True, index=True)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    lobby = relationship("Lobby", back_populates="members")
    user = relationship("User", back_populates="lobby_memberships")

class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, index=True)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"))
    round_number = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    phase = Column(String) # e.g., "product_submission", "commenting", "voting", "finished"
    current_player_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    lobby = relationship("Lobby", back_populates="rounds")
    product = relationship("Product", back_populates="round")
    current_player = relationship("User")
    comments = relationship("Comment", back_populates="round")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, ForeignKey("rounds.id"))
    uploader_id = Column(Integer, ForeignKey("users.id"))
    link = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    round = relationship("Round", back_populates="product")
    uploader = relationship("User", back_populates="products")
    comments = relationship("Comment", back_populates="product")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, ForeignKey("rounds.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    round = relationship("Round", back_populates="comments")
    product = relationship("Product", back_populates="comments")
    author = relationship("User", back_populates="comments")
    votes = relationship("Vote", back_populates="comment")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    voter_id = Column(Integer, ForeignKey("users.id"))
    voted_at = Column(DateTime(timezone=True), server_default=func.now())

    comment = relationship("Comment", back_populates="votes")
    voter = relationship("User", back_populates="votes")
