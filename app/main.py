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
from typing import Optional, List
from .utils import hash

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

@app.get("/posts", response_model=List[schemas.Post]) # response_model is used to specify the type of response that we want to return. In this case, we want to return a list of Post objects. This will help FastAPI to automatically convert the list of Post objects to JSON response and send it to the client.
async def get_posts(db: session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    print(posts)
    return  posts

# Create
@app.post("/posts", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: session = Depends(get_db)):
        
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                                     (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    ''' 
    Without unpacking the post object, we would have to manually extract each field from the pydantic model and pass it to the Post constructor. 
    This can be tedious and error-prone, especially if we have many fields in our model.'''
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    '''
    unpacking the post object to create a new Post object. 
    This is a more concise way to create a new Post object from the pydantic model.
    '''
    new_post = models.Post(**post.model_dump())
    db.add(new_post)    
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}")
async def get_post(id:int, response:Response, db: session = Depends(get_db)): #HTTPException is all it takes
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()   
    
    post = db.query(models.Post).filter(models.Post.id == id).first() # filter() is used to filter the records based on the condition provided. In this case, we are filtering the posts based on the id. The first() method is used to fetch the first record that matches the condition. If no record is found, it returns None.
    
    print(post)

    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}
    return post

# delete operation

@app.delete("/posts/{id}")
async def delete_post(id:int, db:session = Depends(get_db)): 
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    deleted_post.delete(synchronize_session=False)
    db.commit() 
    return {"message": f"Post with id {id} deleted successfully"}

@app.put("/posts/{id}", response_model=schemas.Post)
async def update_post(id:int, post: schemas.PostCreate, db: session = Depends(get_db)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                                     (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return  post_query.first()
    
@app.post("/users", response_model = schemas.UserOut)    
async def create_user(user: schemas.UserCreate, db: session = Depends(get_db)):
    
    print("RAW PASSWORD:", user.password)
    print("BYTE LENGTH:", len(user.password.encode()))
    
    # hash the password
    hashed_password = hash(user.password)
    
    print("HASHED PASSWORD:", hashed_password)
    print("BYTE LENGTH:", len(hashed_password.encode()))
    user.password = hashed_password
       
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)    
    
    db.commit()
    db.refresh(new_user)
    return new_user 
    
@app.get('/users/{id}', response_model=schemas.UserOut)
async def get_user(id: int, db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user