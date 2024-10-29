from fastapi import FastAPI, Request

# import models
# tu nhung file dong cap thi them 1 dau cham
from .models import Base
from .database import engine
from .routers import todos, admin, user, auth
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    # prefix='/',
    # tags=['default']
)

# code nay chi chay khi todos.db KHONG ton tai
#  Lệnh này tạo tất cả các bảng trong cơ sở dữ liệu dựa trên các mô hình được định nghĩa trong models
#  nếu chúng chưa tồn tại. Nó sử dụng engine để kết nối với cơ sở dữ liệu.
# models.Base.metadata.create_all(bind=engine)
# update sau khi import ..models
Base.metadata.create_all(bind=engine)

# link với template html
templates = Jinja2Templates(directory="ToDoApp/templates")

# link voi css name ~ url_for
app.mount("/static", StaticFiles(directory="ToDoApp/static"), name="static")


# ham check html
@app.get("/")
def render_test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
    # return  "dong nay hien len tren giao dien user"


# code check co ban
@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


# code nay de chay router (chung 1 cong, khac ham)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
