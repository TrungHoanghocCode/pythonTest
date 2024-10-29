from ..routers.admin import get_db, get_current_user
from ..models import Todos
from .util import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_admin_authenticated(test_todo):
    response = client.get("/admin/")
    # print("API response data:", response.json())
    assert response.status_code == 200
    assert response.json() == [
        {'complete': False, 'title': 'Learn to code!',
         'description': 'Need to learn everyday!', 'id': 1,
         'priority': 5, 'owner_id': 1}
    ]


def test_delete_admin_authenticated(test_todo):
    response = client.delete("/admin/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/9999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found!'}
