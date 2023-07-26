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

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


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

    def __init__(self, title, post_author, post_content):
        self.title = title
        self.post_author = post_author
        self.post_content = post_content


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(String, nullable=False, primary_key=True)
    comment = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    post_id = Column(ForeignKey("posts.post_id"))
    post = relationship("Post", back_populates="comments")

    user_id = Column(ForeignKey("users.user_id"))
    user = relationship("User", back_populates="comments")

    def __init__(self, comment, user_id, post_id):
        self.comment = comment
        self.user_id = user_id
        self.post_id = post_id


Base.metadata.create_all(bind=engine)
