from fastapi import FastAPI
import models
from database import engine
from routers import post, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)


# psycopg2 connection try and execpt block, not required with an ORM
# just to make this async
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='raziel',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Error", error)

# raw hardcoded ways using sql commands
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
#     "title": "favorite foods", "content": "I like pizza", "id": 2}]
#
# find the post given an id
# def find_post(_id):
#     for post in my_posts:
#         if _id == post["id"]:
#             return post
#

# find the index of a post given an id
# def find_post_index(_id):
#     for index, post in enumerate(my_posts):
#         if _id == post["id"]:
#             return index

# @app.get('/')
# def home():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {'data': posts}

# whenever a new post is created, se the status code to 201, its convention.
# @app.post("/posts/", status_code=status.HTTP_201_CREATED)
# async def create_item(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """,
#                    (post.title, post.content))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {'message': new_post}
#
# @app.get("/posts/_id")
# def get_post(_id: int):
#     cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(_id)))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
#     return {'message': post}
#
# @app.delete("/delete/_id", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(_id: int, response: Response):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(_id))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#
# @app.put("/post/_id")
# def update_post(_id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content), str(_id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
#     return {"message": updated_post}

# Dependency
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# # using sqlalchmemy, it converts the python statements into raw sql commands.
#
# # stuff related to perform CRUD operations on post model
#
# @app.get("/")
# def root():
#     return {"Hello fastapi world"}
#
#
# @app.get("/posts/", response_model=List[schemas.ResponsePostSchema])
# def all_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts
#
#
# @app.post('/posts/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePostSchema)
# def create_posts(post: schemas.RequestPostSchema, db: Session = Depends(get_db)):
#     # new_post = models.Post(title=post.title, content=post.content)
#     new_post = models.Post(**post.dict())  # unpacking, because the above way is a little cumbersome,
#     # imagine a situation where we've 50 attributes for a post. I'm not going to do that with the fist way,
#     # but with the second way.
#     db.add(new_post)  # changes staged
#     db.commit()  # push the changes
#     db.refresh(new_post)  # return the created post
#     return new_post
#
#
# @app.get("/posts/_id", response_model=schemas.ResponsePostSchema)
# def get_post(_id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == _id).first()  # first matching query
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
#     return post
#
#
# @app.delete("/delete/_id", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(_id: int, db: Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == _id)  # SQLalchemy model, it got some really serious
#     # attributes like update, delete etc...
#     post = post_query.first()  # the actual post
#     # print("test feature", post in post_query), sqlmodel = {posts with matching query}, eg {post1, post2, post3...}
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
#     post_query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#
#
# @app.put("/post/_id", response_model=schemas.ResponsePostSchema)
# def update_post(_id: int, post: schemas.RequestPostSchema, db: Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == _id)
#     updated_post = post_query.first()
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {_id} not found")
#     post_query.update(post.dict(), synchronize_session=False)
#     db.commit()
#     return post
#
#
# # sql (a language) is used to communicate with DB.
#
# # we can have a schema for sending a request and similarly a schema for receaving a response.
#
# # synchronize_session attribute mentioning the strategy to update attributes in the session. Valid values are false:
# # for not synchronizing the session, fetch: performs a select query before the update to find objects that are matched
# # by the update query; and evaluate: evaluate criteria on objects in the session.
#
# # stuff related to perform CRUD operations on USER model
#
# @app.post('/createuser/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUserCreateSchema)
# def create_posts(user: schemas.RequestUserCreateSchema, db: Session = Depends(get_db)):
#     # hash the password
#     hashed_password = pwd_context.hash(user.password)
#     user.password = hashed_password
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
#
#
# @app.get("/users/_id", response_model=schemas.ResponseUserCreateSchema)
# def get_user(_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == _id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {_id} not found")
#     return userf
# 8:02