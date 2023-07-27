import uuid

import sqlalchemy
from sqlalchemy import Integer, String, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship
from .database import Base, engine
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    user_id = Column(sqlalchemy.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=True)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    post_id = Column(sqlalchemy.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    views = Column(Integer, nullable=False, default=0)
    post_content = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    post_author = Column(ForeignKey("users.user_id"))

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(sqlalchemy.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    comment = Column(String, nullable=False)
    post_id = Column(ForeignKey("posts.post_id"))
    user_id = Column(ForeignKey("users.user_id"))
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")


Base.metadata.create_all(bind=engine)
