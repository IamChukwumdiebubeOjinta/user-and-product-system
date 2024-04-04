from main import app
from fastapi.testclient import TestClient
from user.user_controllers import get_users, get_user, create_user, update_user, delete_user

client= TestClient(app)

def test_get_users():
    """
    Generate a test for the get_users function.
    """
    response = client.get("/api/v1/users" )
    assert response.status_code == 201
    
# def test_get_users_failure():
#     """
#     Generate a test for the get_users function.
#     """
#     response = client.get("/api/v1/users" )
#     assert response.status_code == 500

def test_get_user():
    """
    A function to test the GET request for retrieving a specific user.
    """
    response = client.get("/api/v1/user/2")
    assert response.status_code == 200
    assert response.json() == {
        "status_code": 201,
        "data": {
        "id": 2,
        "firstname": "NewTest",
        "lastname": "string",
        "email": "user2@example.com",
        "password": "$2b$10$LW0VMXNQmp1cO8JI.Ojlb.aegAHKGbASwrmxTmxoAOrTJ4hTWwOpG"
    }
    }

# def test_get_user_failure():
#     """Test get_user_route when the user is not found."""
#     # Assuming there's no user with ID 999 in your database
#     response = client.get("api/v1/user/999")
#     assert response.status_code == 404

def test_create_user():
    data = {
        "id": "7",
        "firstname": "Test",
        "lastname": "Testerson",
        "email": "test@example.com",
        "password": "Password123$$"
    }
    response = client.post("/api/v1/create_user", json=data)
    assert response.status_code == 200


def test_update_user():
    data = {"firstname": "NewTest"}
    response = client.patch("/api/v1/users/2", json=data)
    assert response.status_code == 200


def test_delete_user():
    response = client.delete("/api/v1/users/3")
    assert response.status_code == 200

