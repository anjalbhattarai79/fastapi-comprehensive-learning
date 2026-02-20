import random
from fastapi import  FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel  
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# pydantic schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # optional field with default value
    rating: Optional[int] = None # optional field with default value None

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

@app.get("/") # This will be shown
async def read_root():
    return {"message": "Welcome to my api"}   

@app.get("/")
async def read_root():
    return {"message": "Welcome to my api 2"}

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

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id): 
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    
    print(posts)
    return {"data": posts}

# Create
@app.post("/posts")
async def create_post(post : Post):
    post_dict = post.model_dump()
    post_dict['id'] = random.randint(0, 1000000) # generate random id for the post
    my_posts.append(post_dict)
    return {"data": my_posts}

@app.get("/posts/{id}")
async def get_post(id:int, response:Response): #HTTPException is all it takes
    print(type(id))
    post = find_post(id)
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}
    return {"post_detail": post}

# delete operation

@app.delete("/posts/{id}")
async def delete_post(id:int): 
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    my_posts.remove(post)
    return {"message": f"Post with id {id} deleted successfully"}

@app.put("/posts/{id}")
async def update_post(id:int, post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = id
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            my_posts[i] = post_dict
            return {"message": f"Post with id {id} updated successfully", "data": post_dict}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")