from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog import schemas, database, models

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login/")
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == request.email).first()
    if db_user:
        return db_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
