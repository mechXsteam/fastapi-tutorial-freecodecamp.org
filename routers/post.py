from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.orm import Relationship
import models
import oauth2
import schemas
from database import get_db

router = APIRouter(
    # this is added as most of our url starts with 'posts', so we replaced it with prefix. So now onwards any url
    # will go like this -> localhost:8000/posts/somethingelse...
    prefix="/posts",
    # this is used to group the routers in the documentation
    tags=['posts']
)


# using sqlalchmemy, it converts the python statements into raw sql commands.

# stuff related to perform CRUD operations on post model

@router.get("/", response_model=List[schemas.ResponsePostSchema])
def all_posts(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user), limit: int = 10):
    print(limit) # query parameter
    print(current_user.email)
    posts = db.query(models.Post).all()
    # posgs = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePostSchema)
def create_posts(post: schemas.RequestPostSchema, db: Session = Depends(get_db), current_user=Depends(
    oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content)
    # we need to provide the foreign key as current user id
    new_post = models.Post(owner_id=current_user.id, **post.dict())  # unpacking, because the above way is a little
    # cumbersome,
    # imagine a situation where we've 50 attributes for a post. I'm not going to do that with the fist way,
    # but with the second way.
    db.add(new_post)  # changes staged
    db.commit()  # push the changes
    db.refresh(new_post)  # return the created post
    return new_post


@router.get("/_id", response_model=schemas.ResponsePostSchema)
def get_post(_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == _id).first()  # first matching query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
    return post


@router.delete("/_id", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == _id)  # SQLalchemy model, it got some really serious
    # attributes like update, delete etc...
    post = post_query.first()  # the actual post
    # print("test feature", post in post_query), sqlmodel = {posts with matching query}, eg {post1, post2, post3...}
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="u are trying to delete a post to which u "
                                                                          "donot belongs to")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/_id", response_model=schemas.ResponsePostSchema)
def update_post(_id: int, post: schemas.RequestPostSchema, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == _id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="u are trying to update  a post to which u "
                                                                          "donot belongs to")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post


