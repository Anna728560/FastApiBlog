from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from blog.schemas import user_schemas
from blog.crud import user_crud
from blog import database

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schemas.ShowUser,
)
def create_user(request: user_schemas.User, db: Session = Depends(database.get_db)):
    return user_crud.create_new_user(request, db)


@router.get(
    "/{id}/",
    response_model=user_schemas.ShowUser,
)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    return user_crud.get_user_by_id(user_id, db)
