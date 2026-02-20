from .database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)    
    published = Column(Boolean, server_default='TRUE', nullable=False)
    