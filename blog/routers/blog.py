from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from blog import database
from blog.authentication import oauth2
from blog.crud import blog_crud
from blog.schemas import blog_schemas, user_schemas

router = APIRouter(
    tags=["Blogs"],
    prefix="/blogs"
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_blog(
        request: blog_schemas.Blog,
        db: Session = Depends(database.get_db),
        current_user: user_schemas.User = Depends(oauth2.get_current_user)
):
    return blog_crud.create_new_blog(request, db)


@router.get(
    "/",
    response_model=List[blog_schemas.ShowBlog],
)
def get_all(db: Session = Depends(database.get_db)):
    return blog_crud.get_all_blogs(db)


@router.get(
    "/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=blog_schemas.ShowBlog,
)
def get_one(blog_id: int, db: Session = Depends(database.get_db)):
    return blog_crud.get_blog_by_id(blog_id, db)


@router.put(
    "/{id}/",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_blog(
        blog_id: int,
        blog: blog_schemas.Blog,
        db: Session = Depends(database.get_db),
        current_user: user_schemas.User = Depends(oauth2.get_current_user),
):
    return blog_crud.update_blog_by_id(blog_id, blog, db)


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def destroy_blog(
        blog_id: int,
        db: Session = Depends(database.get_db),
        current_user: user_schemas.User = Depends(oauth2.get_current_user)
):
    return blog_crud.delete_blog_by_id(blog_id, db)
