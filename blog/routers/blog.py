from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog import schemas, models, database


router = APIRouter()


@router.post(
    "/blog/",
    status_code=status.HTTP_201_CREATED,
    tags=["blogs"],
)
def create_blog(blog: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=blog.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get(
    "/blog/",
    response_model=List[schemas.ShowBlog],
    tags=["blogs"],
)
def get_all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get(
    "/blog/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
    tags=["blogs"],
)
def get_one(blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog:
        return blog

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id {blog_id} is not found"
    )


@router.put(
    "/blog/{id}/",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["blogs"],
)
def update_blog(blog_id: int, blog: schemas.Blog, db: Session = Depends(database.get_db)):
    db_blog = get_one(blog_id=blog_id, db=db)
    for attr, value in blog.dict().items():
        setattr(db_blog, attr, value)
    db.commit()
    return "Updated Blog"


@router.delete(
    "/blog/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["blogs"],
)
def destroy_blog(blog_id: int, db: Session = Depends(database.get_db)):
    db_blog = get_one(blog_id=blog_id, db=db)
    db.delete(db_blog)
    db.commit()
    return "done"
