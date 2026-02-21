from fastapi import  Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import session
from pydantic import BaseModel  
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from . import schemas
from .database import engine, get_db
from .utils import hash
from .routers import post, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




while True:    
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="admin", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection  successful")
        break
        
    except Exception as e:
        print("Database connection failed")
        print("Error: ", e)
        time.sleep(2) # wait for 2 seconds before trying to connect again
        
app.include_router(post.router)
app.include_router(users.router)
   

@app.get("/") # This will be shown
async def read_root():
    return {"message": "Welcome to my api"}   

@app.get("/")
async def read_root():
    return {"message": "Welcome to my api 2"}

'''@app.get("/sqlalchemy")
async def read_sqlalchemy(db: session = Depends(get_db)):
    
    posts = db.query(models.Post).all() # db.query() prepares the query to be executed. The actual execution happens when we call .all() method, which fetches all the records from the database and returns them as a list of Post objects.
 
    return {"message": "SQLAlchemy is working", "data": posts}
    # return None
'''

# using path parameters
# @app.get("/posts/{i}")
# def get_post(i: int):
#     return {"message": f"This is post number {i}"}


'''

# Sending data in Body too the server using POST method
@app.post("/posts")
async def create_post(post : Post):
    print(post)
    # print(post.dict()) DEPRECATED
    print(post.model_dump()) # new way to convert pydantic model to dict
    # return {"message": f"Post created successfully with title {post.title} and content {post.content} and published status {post.published}"}
    return post # Even we returned pydantic model or, list of dicts, FastAPI will automatically convert it to JSON response and send it to the client. 
    
    '''

#-------CRUD Operations-------
# GET - Read

'''my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id): 
    for p in my_posts:
        if p['id'] == id:
            return p'''
