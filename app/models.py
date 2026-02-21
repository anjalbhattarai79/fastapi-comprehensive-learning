from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)    
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    
    ''' 
    SQL Alchemy ensure if tablename is create from this code one.
        - If dont exist it creates,
        - if exist it uses the existing one.
        - IF EXIST but different than as defined in code, it will not change the existing one.
        - We can delete table and new table will be created automatically according to the code. 
        
        - We need to use ALBEMIC to solve this.
        
    '''
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # foreign key to the users table, but we will handle it in the code instead of using actual foreign key constraint in the database
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False) 
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))