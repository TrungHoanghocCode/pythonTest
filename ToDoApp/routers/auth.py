from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, Request
from starlette.exceptions import HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette.responses import HTMLResponse

from ..models import Users
from ..database import SessionLocal
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# ham router ~ app
router = APIRouter(
    # chia cac api endpoint ra 1 nhanh rieng
    # prefix tao 1 tien to cho cac endpoint
    prefix='/auth',
    # tags hien tren UI
    tags=['auth'],
    # responses={401: {"user": "Not authorized"}}
)

# check lai secret sau khi chay code openssl rand -hex 32
# co ban chua can ...
SECRET_KEY = 'trungHocPython'
# mac dinh
ALGORITHM = 'HS256'
# SECRET_KEY + ALGORITHM => tao nen 1 sig => bao mat

# chua can hieu lam ve bcrypt, no la cong cu de hash pass
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# la cong cu đe check token => 1 object
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


# def a():
#     print(type(bcrypt_context))
#     print(type(oauth2_bearer))
#
#
# a()


def get_db():
    db = SessionLocal()
    # code try nghia la chi co code truoc va yield duoc thuc thi truoc khi gui di response
    try:
        yield db
    # code finally duoc thuc thi sau khi gui response
    finally:
        db.close()


# dat 1 bien cho viec dung database
# db_dependency = Annotated[Session, Depends(get_db)]
db_dependency = Annotated[Session, Depends(get_db)]

# link html
templates = Jinja2Templates(directory="ToDoApp/templates")


# router.mount("/static", StaticFiles(directory="ToDoApp/static"), name="static")

#  html Pages

@router.get("/login")
def render_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
def render_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# End-points

# ham xac thuc users, check xem luc login co user do khong
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    # user add name vao, neu ko co => false
    if not user:
        return False
    # tiep tuc, neu sai pass => false
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    # test
    # user_dict = {c.name: getattr(user, c.name) for c in user.__table__.columns}
    # print(username, password, user_dict)
    return user
    # thuc ra user o day la 1 truy van den Users co dang :
    # < models.Users object at 0x00000235C17355B0 >
    # tuy nhien van co the dung user.username duoc


# ham tao token JWT => sau khi user login, moi hanh dong tiep theo deu phai thong qua jwt de bao mat
# moi endpoint deu se duoc xac minh jwt thong qua token
def create_access_token(
        # nhung thong tin muon co trong 1 jwt
        username: str,
        user_id: int,
        role: str,
        # la 1 kieu JWT, sau khi ko hoat dong 1 thoi gian thi JWT thay doi
        expires_delta: timedelta
):
    # bat dau khai bao JWT, lay thong tin de khi nhan ma json ta co the giai ma nay va xac thuc
    encode = {'name': username, 'id': user_id,
              'role': role
              }
    # lay time de co the thong bao JWT het han
    expires = datetime.now(timezone.utc) + expires_delta

    # update khi het han
    encode.update({'exp': expires})
    # tra ve jwt da ma hoa, key va thuat toan
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# ham check token (decode jwt), tiep nhan tham so token sau do decode
# nghia la doi voi mọi action trong tương lai đều cần xác minh user trước
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        # decode jwt => {}
        # để decode cần token (nguyen lieu), key : ad giữ và thuật toán encode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # sau khi decode thi dung`
        username: str = payload.get('name')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        # decode xong thì check
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        # nếu  có thì return
        return {'username': username, 'id': user_id,
                'user_role': user_role
                }
    # nếu nhu ngay từ đâu có lỗi JWT
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


class CreateUserRequest(BaseModel):
    # bo qua id vi se co fastAPI, sql auto tang
    # bo qua isActive, moi khi tao 1 user, user do se  active by default
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    # password va role se co func trong tuong lai
    password: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ham post user moi
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest,
                      ):
    # khong dung mau create_user_model = Users(**create_user_request.dict())
    # vi CreateUserRequest co password trong khi model co hashed_password
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        # hashed_password=create_user_request.password,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    # o day phai code tung key 1, ko OOP dc

    db.add(create_user_model)
    db.commit()
    # return create_user_model


# ham nay de user nhap form va chung ta check, tao jwt
@router.post("/token",
             # tao 1 phan hoi => ham nay bat buoc phai tra ra 1 baseModel Token
             response_model=Token
             )
async def login_for_access_token(
        # code nay cho phep client nhap form, va ta nhan duoc value thong qua return
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency):
    # tiep nhan user sau khi di qua ham xac thuc
    user = authenticate_user(form_data.username, form_data.password, db)

    # neu khong co => thong bao 401
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    # tao ra 1 token sau khi xac thuc co user
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
    # print(user.username)
    # return user


# ham doc user
@router.get("/User", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency):
    return db.query(Users).all()


# ham xoa user, nhap chinh xac id
@router.delete("/User/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_hardTest(db: db_dependency, user_id: int):
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()

# @router.get("/", response_class=HTMLResponse)
#
# async def authentication_page(request: Request):
#
#     return templates.TemplateResponse("login-register.html", {"request": request})