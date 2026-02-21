from fastapi import  Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)

@router.post("/login")
async def login(user_login: schemas.UserLogin = Depends(), users_db: session = Depends(get_db)):
    
    user = users_db.query(models.User).filter(models.User.email == user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email")
    
    if not utils.verify(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password") 
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
       
    return {"access_token": access_token, "token_type": "bearer"}    