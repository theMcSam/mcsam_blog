from sqlalchemy import Integer, String, ForeignKey, Column, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from .database import Base, engine
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=True)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    post = relationship("Post")
    comment = relationship("Comment")
    

    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

class Post(Base):
    __tablename__ = "posts"
    post_id = Column(String, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    views = Column(Integer, nullable=False, default=0)
    post_content = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    post_author= Column(String, ForeignKey("users.user_id"))
    user = relationship("User", back_populates="post")
    comment = relationship("Comment")
    

    def __init__(self, post_id, title, views, post_author):
        self.post_id = post_id
        self.title = title
        self.views = views
        self.post_author = post_author

class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(String, nullable=False, primary_key=True)
    comment = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    post_id = Column(String, ForeignKey("posts.post_id"))
    post = relationship("Post", back_populates="comment")

    user_id = Column(String, ForeignKey("users.user_id"))
    user = relationship("User", back_populates="comment")

Base.metadata.create_all(bind=engine)