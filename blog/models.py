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
    is_admin = Column(Boolean, nullable=False, default=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, username, password, email, is_admin):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin