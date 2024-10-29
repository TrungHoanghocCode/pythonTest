from .util import *
from ..routers.user import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# thay vi truyen test_todo, gio day truyen test_user de lay user dummy
def test_user_showInfomation(test_user):
    response = client.get("/user")
    assert response.status_code == 200

    # voi override_get_current_user hien tai duoc ghi de boi dummy
    # {'username': 'TrungHocIT', 'id': 1, 'user_role': 'admin'}
    # nen response.json() ko nhan ra dc user nay

    assert response.json()['username'] == 'okokla'
    assert response.json()['email'] == 'okconde@email.com'
    assert response.json()['first_name'] == 'ok'
    assert response.json()['last_name'] == 'la'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '12345666'
    # ta buoc phai xac minh tung key va bo qua password vi pass da hash


def test_user_change_password(test_user):
    request_data = {"password": "test", "new_password": "newpassword"}
    response = client.put("/user/passwordChange", json=request_data)
    assert response.status_code == 204
    # hash roi ko check dc


def test_user_change_password_invalid_current_password(test_user):
    request_data = {"password": "fail", "new_password": "hehe"}
    response = client.put("/user/passwordChange", json=request_data)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Error on password change !'}


def test_user_change_phoneNumber(test_user):
    response = client.put("/user/phoneNumberChange/021095")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model.phone_number == "021095"
