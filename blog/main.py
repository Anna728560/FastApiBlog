from fastapi import FastAPI

from blog import models, schemas
from blog.database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post("/blog/")
def create_blog(blog: schemas.Blog):
    return {"data": f"Blog is created with title as {blog.title}"}
