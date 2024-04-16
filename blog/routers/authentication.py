from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from blog import database, models
from blog.authentication import token
from blog.authentication.hashing import Hash


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/token/")
def login(
        request: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == request.username
    ).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not Hash.verify_password(request.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password"
        )

    access_token = token.create_access_token(
        data={"sub": db_user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
