from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)    
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False) 
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))