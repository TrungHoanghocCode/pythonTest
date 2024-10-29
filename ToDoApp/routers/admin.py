from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
# doi voi file tren 1 cap thi 2 dau cham
from ..database import SessionLocal
from ..models import Todos
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# set ad co the get duoc all todos
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_byAdmin(db: db_dependency, user: user_dependency):
    if user is None or user.get('user_role') != "admin":
        raise HTTPException(status_code=401, detail='Authentication Failed or You are not Ad')
    # return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    return db.query(Todos).all()
    # return 1


# ham del cho ad
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != "admin":
        raise HTTPException(status_code=401, detail='Authentication Failed or You are not Ad')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found!')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()
