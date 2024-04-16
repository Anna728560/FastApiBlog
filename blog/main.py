from typing import List

from fastapi import FastAPI, Depends, status, HTTPException

from sqlalchemy.orm import Session

from blog import models, schemas
from blog.database import engine, SessionLocal

from blog.hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/blog/",
    status_code=status.HTTP_201_CREATED,
    tags=["blogs"],
)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get(
    "/blog/",
    response_model=List[schemas.ShowBlog],
    tags=["blogs"],
)
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get(
    "/blog/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
    tags=["blogs"],
)
def get_one(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog:
        return blog

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id {blog_id} is not found"
    )


@app.put(
    "/blog/{id}/",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["blogs"],
)
def update_blog(blog_id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    db_blog = get_one(blog_id=blog_id, db=db)
    for attr, value in blog.dict().items():
        setattr(db_blog, attr, value)
    db.commit()
    return "Updated Blog"


@app.delete(
    "/blog/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["blogs"],
)
def destroy_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = get_one(blog_id=blog_id, db=db)
    db.delete(db_blog)
    db.commit()
    return "done"


@app.post(
    "/user/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
    tags=["users"],
)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get(
    "/user/{id}/",
    response_model=schemas.ShowUser,
    tags=["users"],
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        return db_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id {user_id} is not found"
    )
