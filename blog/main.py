from fastapi import FastAPI

from blog.schemas import Blog

app = FastAPI()


@app.post("/blog/")
def create_blog(blog: Blog):
    return {"data": f"Blog is created with title as {blog.title}"}
