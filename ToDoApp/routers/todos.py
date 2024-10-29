# from fastapi import  APIRouter
#
# router = APIRouter()

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from ..database import SessionLocal
from ..models import Todos
from .auth import get_current_user

templates = Jinja2Templates(directory="ToDoApp/templates")

# app = FastAPI()
# chuyen tu main sng va doi tu app => router
router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


# chuyen sang todos nen ko con can code nay nua
# # code nay chi chay khi todos.db KHONG ton tai
# models.Base.metadata.create_all(bind = engine)
#
# # code nay de chay router (chung 1 cong, khac ham)
# app.include_router(auth.router)

# ham get_db lay lai ham SessionLocal da khai bao tu database - tao phien cuc bo
def get_db():
    db = SessionLocal()

    # code try nghia la chi co code truoc va yield duoc thuc thi truoc khi gui di response
    try:
        yield db

    # code finally duoc thuc thi sau khi gui response
    finally:
        db.close()


# dat 1 bien cho viec dung database
db_dependency = Annotated[Session, Depends(get_db)]
# dat 1 bien cho v iec dung user, lay ham get_current_user tu auth
user_dependency = Annotated[dict, Depends(get_current_user)]


# BaseModel cho viec validate Request
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=-1, lt=6)
    complete: bool


# ham dieu huong tro lai login page
def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login", status_code=302)
    # tao 1 key de delete cookie
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


# Pages
@router.get("/todo")
async def render_todoPage(request: Request, db: db_dependency):
    try:
        # voi cookie co key trung voi ham redirect
        user = await get_current_user(request.cookies.get("access_token"))
        # neu khong co user thi dieu huong ve login
        if user is None:
            print("ko co ủe")
            return redirect_to_login()
        print("co ủe nè", user)
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        print("request:", request)
        print("todos:", todos)
        print("user:", user)
        # return templates.TemplateResponse("todos.html", {"request": request, "todos": todos, "user": user})
        # return templates.TemplateResponse("test2208.html", {"request": request,  "user": user, "todos": todos})
        return templates.TemplateResponse("todo.html", {"request": request,  "user": user, "todos": todos})
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
        return redirect_to_login()


# EndPoints

# ham get doc info tu todos.db (co gi doc nay, / => ngay trang chu)
# sau khi update user thi doc tat ca todos cua user dang authorize
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    # return 1


# voi tham so todo_id truyen vao , get Todos (path)
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # first : ngay khi co ket qua khop => tra ve ngay (vi thuc ra chi co 1 id key )
    # todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    # sau khi  filter lay todos co id dung thi so sanh voi id trung owner_id
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found !")


# ham post - tao them
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency,
                      user: user_dependency,
                      todo_request: TodoRequest
                      # nap vao data: de post vao, user de xac thuc,
                      # TodoRequest da duoc base truoc, user nhap vao
                      ):
    # check ng dung truoc
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # neu co user thi thuc hien add
    # tuy nhien todo_request chua co owner_id => them thu cong tu user
    todo_model = Todos(**todo_request.model_dump(),
                       owner_id=user.get("id")
                       )
    db.add(todo_model)

    # code nay co them nham connect voi database, day todos vao database va lam rong post
    db.commit()


# ham put - update
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      user: user_dependency,
                      #  todo_request: TodoRequest o truoc id vi co ban phai co request thi moi check id)
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # so sanh id, trung => upd
    # todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    # sau khi update user: loc tim todos co id trung sau do so sanh loc voi owner_id trung
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    # print(f"update_todo called with todo_id: {todo_model}, {todo_id}")
    # test test test
    # Trung oi ko hoc luot nua, ko duoc nan~

    # trg hop ko co id trung
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found !")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # check co todos trung id , trung owner_id khong
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()
