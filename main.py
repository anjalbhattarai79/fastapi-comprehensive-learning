from fastapi import  FastAPI
from fastapi.params import Body
from pydantic import BaseModel  
from typing import Optional

app = FastAPI()

# pydantic schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # optional field with default value
    rating: Optional[int] = None # optional field with default value None

@app.get("/") # This will be shown
async def read_root():
    return {"message": "Welcome to my api"}   

@app.get("/")
async def read_root():
    return {"message": "Welcome to my api 2"}

# @app.get("/posts/{i}")
# def get_post(i: int):
#     return {"message": f"This is post number {i}"}

# Sending data in Body too the server using POST method

@app.post("/createposts")
def create_post(post : Post):
    print(post)
    # print(post.dict()) DEPRECATED
    print(post.model_dump()) # new way to convert pydantic model to dict
    # return {"message": f"Post created successfully with title {post.title} and content {post.content} and published status {post.published}"}
    return post.model_dump()