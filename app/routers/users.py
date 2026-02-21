from fastapi import  Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import session
from ..database import get_db
from .. import models, schemas


router = APIRouter(
    prefix="/users"
)
   
@router.post("/", response_model = schemas.UserOut)    
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
    
@router.get('/{id}', response_model=schemas.UserOut)
async def get_user(id: int, db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user