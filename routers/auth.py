from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # it will generate a request schema for login credential
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import oauth2
import schemas
from database import get_db

router = APIRouter(tags=['Authentication'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # username (email) and password
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user or not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # create a token for JWT authentication
    return {"access_token": access_token, "token_type": "bearer"}
