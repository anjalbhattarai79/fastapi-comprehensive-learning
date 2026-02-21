from fastapi import  Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import session
from ..database import get_db
from .. import models, schemas
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post]) # response_model is used to specify the type of response that we want to return. In this case, we want to return a list of Post objects. This will help FastAPI to automatically convert the list of Post objects to JSON response and send it to the client.
async def get_posts(db: session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    print(posts)
    return  posts

# Create
@router.post("/", response_model=schemas.Post)
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

@router.get("/{id}")
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

@router.delete("/{id}")
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

@router.put("/{id}", response_model=schemas.Post)
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
 