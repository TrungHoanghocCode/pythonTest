import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from ..routers.auth import bcrypt_context
from ..database import Base
from ..main import app
# van can import Todos, Users vi can de lay base cho dummy
from ..models import Todos, Users

# thay vi todosApp.db la database chinh, khi test se test tren testdb
SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

# cung nhu luc tao database, engine la bien de link voi testdb
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Tùy chọn này chỉ định rằng các kết nối có thể được sử dụng trên nhiều luồng
    # 'check_same_thread': False => nhieu luồng, default = 1 luồng
    connect_args={'check_same_thread': False},
    # đảm bảo mỗi kết nối là độc lập và không bị ảnh hưởng bởi các kết nối khác.
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    # nghia la phai comit thu cong de luu khi thay doi data
    autocommit=False,
    # dữ liệu sẽ không tự động được gửi xuống
    autoflush=False,
    # Kết nối session với engine vừa tạo, tức là mọi thao tác của session sẽ được thực hiện trên testdb.db
    bind=engine)

# Dòng này tạo tất cả các bảng trong cơ sở dữ liệu, ma Base duoc dinh nghia tu database
Base.metadata.create_all(bind=engine)


# ham ghi de data
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ham ghi de 1 mau current_user
def override_get_current_user():
    return {'username': 'TrungHocIT', 'id': 1, 'user_role': 'admin'}


# bien su dung thu vien TestClient
client = TestClient(app)


# ham test todos voi pytest.fixture
# tao 1 mau ToDos de test
@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )
    # thay vi truyen db: db_dependency db test = TestingSessionLocal()
    # neu khong db nay se chay tren ToDoApp.db
    db = TestingSessionLocal()
    # add vao testdb
    db.add(todo)
    # phai commit thu cong
    db.commit()

    # Dùng yield để trả về đối tượng todos cho các hàm kiểm thử mà sử dụng fixture này.
    # Sau khi các hàm kiểm thử chạy xong, phần mã sau yield sẽ được thực hiện để dọn dẹp dữ liệu thử nghiệm.
    yield todo

    with engine.connect() as connection:
        # Thao tác này sẽ xóa mọi thứ trong bảng TODOS có trong cơ sở dữ liệu thử nghiệm của chúng ta.
        # sau khi các test case đã chạy xong
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="okokla",
        email="okconde@email.com",
        first_name="ok",
        last_name="la",
        hashed_password=bcrypt_context.hash("test"),
        role="admin",
        phone_number="12345666"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
