from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship


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
    
    # relationship to the User model, back_populates is used to specify the name of the attribute in the User model that will be used to access the posts of a user.
    owner = relationship("User")  
    ''' Prevents to writed joins manually. But, User schema should be defined within Postschema in schema.py to give output of the owner details when we fetch the posts. '''
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False) 
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    
class Vote(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True) 
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)