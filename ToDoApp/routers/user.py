from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from ..database import SessionLocal
from .auth import get_current_user
from ..models import Users

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# tao 1 model cho user nhap vao
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=3)


@router.get("/", status_code=status.HTTP_200_OK)
async def showInfomation(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed ')
    # return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    return user_model


@router.put("/passwordChange", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # lay user trung id truoc
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    # so sanh pass
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change !')
    # update pass
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phoneNumberChange/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phoneNumber(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # lay user trung id truoc
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    # update phone_number
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
