from fastapi import  Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import session
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)

@router.post("/login")
async def login(user_login: schemas.UserLogin, users_db: session = Depends(get_db)):
    
    user = users_db.query(models.User).filter(models.User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email")
    
    if not utils.verify(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")    
    return {"message": "Login successful"}  
    