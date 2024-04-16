from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from blog import models, schemas
from blog.database import engine, SessionLocal


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog/", status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/")
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}/", status_code=status.HTTP_200_OK)
def get_one(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog:
        return blog

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id {blog_id} is not found"
    )


@app.delete("/blog/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def destroy_blog(blog_id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == blog_id).delete(
        synchronize_session=False
    )
    db.commit()
    return "done"


