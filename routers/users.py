from fastapi import status, HTTPException, Depends, APIRouter
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

router = APIRouter(
    # this is used to group the routers in the documentation
    tags=["users"]
)


# stuff related to perform CRUD operations on USER model

@router.post('/createuser/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUserCreateSchema)
def create_posts(user: schemas.RequestUserCreateSchema, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/_id", response_model=schemas.ResponseUserCreateSchema)
def get_user(_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == _id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {_id} not found")
    return user
