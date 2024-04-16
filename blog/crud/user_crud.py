from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog import database, models
from blog.schemas import user_schemas
from blog.authentication.hashing import Hash


def create_new_user(
        request: user_schemas.User,
        db: Session = Depends(database.get_db)
):
    hashed_password = Hash.bcrypt_hash(request.password)
    db_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        return db_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id {user_id} is not found"
    )
