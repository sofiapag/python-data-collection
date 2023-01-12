from fastapi import status
from fastapi.testclient import TestClient

from main import app


def create_user(client) -> dict:
    response = client.post("/users", json={"name": "foobar"})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_all_users(client) -> dict:
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_user(client, user_id: int):
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_crud_users():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_users(client)
        assert len(response) == 0
        # create an entry
        response = create_user(client)
        user_id = response["id"]
        # get entry
        response = get_all_users(client)
        assert len(response) == 1
        assert response[0]["id"] == user_id
        assert response[0]["name"] == "foobar"
        response = delete_user(client, user_id=user_id)
        response = get_all_users(client)
        assert len(response) == 0
