from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from blog import schemas, models, database
from blog.hashing import Hash


router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
)
def create_user(user: schemas.User, db: Session = Depends(database.get_db)):
    hashed_password = Hash.bcrypt_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get(
    "/{id}/",
    response_model=schemas.ShowUser,
)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        return db_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id {user_id} is not found"
    )
