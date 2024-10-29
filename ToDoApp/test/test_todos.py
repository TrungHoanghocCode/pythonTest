from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
# import * nghia la import tat ca tu util
from .util import *

# qua trinh ghi de lam cho data trống
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# ham test read all
# truyen vao test_todo de lay duoc mau todos
def test_read_all_authenticated(test_todo):
    # Gửi một yêu cầu HTTP GET tới endpoint / của ứng dụng
    # để lấy tất cả các bản ghi Todos có trong cơ sở dữ liệu.
    response = client.get("/todos/")
    # Kiểm tra xem mã trạng thái HTTP
    assert response.status_code == status.HTTP_200_OK
    # Kiểm tra xem dữ liệu JSON trả về từ endpoint có giống với dữ liệu mong đợi hay không.
    # = Todos phia tren
    assert response.json() == [
        {'complete': False, 'title': 'Learn to code!',
         'description': 'Need to learn everyday!', 'id': 1,
         'priority': 5, 'owner_id': 1}
    ]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    # assert response.status_code == status.HTTP_200_OK
    assert response.status_code == 200
    assert response.json() == {'complete': False, 'title': 'Learn to code!',
                               'description': 'Need to learn everyday!', 'id': 1,
                               'priority': 5, 'owner_id': 1}


def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/999")
    assert response.status_code == 404
    # thao khao voi   raise HTTPException(status_code=404, detail="Todos not found !") o todos.py
    assert response.json() == {'detail': 'Todo not found !'}


def test_create_todo(test_todo):
    # tạo 1 request dummy
    request_data = {
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    # voi response.status_code == 201 : da check thanh cong create
    response = client.post('/todos/todo/', json=request_data)
    assert response.status_code == 201
    # nhung de check ki hon, ta co the check tung key
    db = TestingSessionLocal()
    # luon luon doi voi moi ham tét se duoc tao 1 dummy todos = 1
    # vay o day sau khi tao them request_data , ta so sanh voi id = 2
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(test_todo):
    # tao 1 data de update cho ID 1
    request_data = {
        'title': 'Change the title of the todo already saved! ',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    # link voi id 1
    response = client.put('/todos/todo/1', json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Change the title of the todo already saved! '


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todos/todo/999', json=request_data)
    assert response.status_code == 404
    # thao khao detail voi todos.py
    assert response.json() == {'detail': 'Todo not found !'}


def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    # model = none vi id = 1 da bi xoa
    assert model is None


def test_delete_todo_not_found():
    response = client.delete('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}
