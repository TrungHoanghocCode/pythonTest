from .util import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

# ghi de override_get_db de lam trong db
app.dependency_overrides[get_db] = override_get_db

# test xac thuc
# truyen dummy vao
def test_auth_authenticate_user(test_user):
    db = TestingSessionLocal()
    # tao bien authenticated_user_test = ham da tao o auth nhan username + pass
    authenticated_user_test = authenticate_user(test_user.username, 'test', db)
    # xac thuc co user
    assert authenticated_user_test is not None
    # xac thuc dung username
    assert authenticated_user_test.username == test_user.username


    # check xac thuc sai username
    non_existent_user = authenticate_user('FailName', 'test', db)
    assert non_existent_user is False
    #  check xac thuc sai pass
    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False


# test ham tao token,
def test_auth_create_access_token():
    # thong tin dummy
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    # dung ham create_access_token de test
    token = create_access_token(username, user_id, role, expires_delta)

    # decode tro lai de test
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                               options={'verify_signature': False})

    assert decoded_token['name'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


# test ham async
# pytest ko check dc ham async - tru khi cai thu vien asyncio
@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'name': 'test_user', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'test_user', 'id': 1, 'user_role': 'admin'}


# @pytest.mark.asyncio
# async def test_get_current_user_missing_payload():
#     # phan encode dummy nay sai => 401
#     encode = {'role': 'user'}
#     token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
# #
#     with pytest.raises(HTTPException) as alo:
#         await get_current_user(token=token)
#
#     assert alo.value.status_code == 401
#     assert alo.value.detail == 'Could not validate user.'
#     assert 1==1






