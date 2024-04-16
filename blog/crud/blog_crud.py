from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog import models, database
from blog.schemas import blog_schemas


def get_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


def create_new_blog(blog: blog_schemas.Blog, db: Session = Depends(database.get_db)):
    db_blog = models.Blog(title=blog.title, body=blog.body, user_id=blog.user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def get_blog_by_id(blog_id: int, db: Session = Depends(database.get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog:
        return db_blog

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id {blog_id} is not found"
    )


def update_blog_by_id(blog_id: int, blog: blog_schemas.Blog, db: Session = Depends(database.get_db)):
    db_blog = get_blog_by_id(blog_id=blog_id, db=db)
    for attr, value in blog.dict().items():
        setattr(db_blog, attr, value)
    db.commit()
    return "Updated Blog"


def delete_blog_by_id(blog_id: int, db: Session = Depends(database.get_db)):
    db_blog = get_blog_by_id(blog_id=blog_id, db=db)
    db.delete(db_blog)
    db.commit()
    return "Done"
