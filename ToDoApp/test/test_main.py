from fastapi.testclient import TestClient
# import main
from ..main import app
from fastapi import status

# tao bien su dung thu vien TestClient
# client = TestClient(main.app)
client = TestClient(app)


# ham check, voi viec api o file main co return la return {'status': 'Healthy'}
def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}
