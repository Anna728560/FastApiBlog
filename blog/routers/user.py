from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from blog import schemas, database
from blog.crud import user_crud

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user_crud.create_new_user(request, db)


@router.get(
    "/{id}/",
    response_model=schemas.ShowUser,
)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    return user_crud.get_user_by_id(user_id, db)
