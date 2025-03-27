from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


class ShowBlog(BlogBase):
    id: int
    creator: "ShowBlogUser"

    class Config:
        orm_mode = True


class ShowBlogUser(BaseModel):
    email: str

    class Config:
        orm_mode = True
