from fastapi import status
from fastapi.testclient import TestClient

from main import app


def create_user(client: TestClient) -> dict:
    response = client.post("/users", json={"name": "foobar"})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_all_users(client: TestClient) -> dict:
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_user(client: TestClient, user_id: int):
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def create_crop(client: TestClient) -> dict:
    response = client.post(
        "/crops", 
        json={
            "year": 2000,
            "crop_type": "corn",
            "tilled": True,
            "tillage_depth": 2,
            "comments": "Corn was planted",
            "user_id": 1
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def create_crop_400_error(client: TestClient) -> dict:
    response = client.post(
        "/crops", 
        json={
            "year": 2000,
            "crop_type": "corn",
            "tilled": False,
            "tillage_depth": 2,
            "comments": "Corn was planted",
            "user_id": 1
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    return response.json()


def get_all_crops(client: TestClient) -> dict:
    response = client.get("/crops")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def get_crop(client: TestClient, crop_id: int) -> dict:
    response = client.get(f"/crops/{crop_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def get_crop_404_error(client: TestClient, crop_id: int) -> dict:
    response = client.get(f"/crops/{crop_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    return response.json()


def delete_crop(client: TestClient, crop_id: int):
    response = client.delete(f"/crops/{crop_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def delete_crop_404_error(client: TestClient, crop_id: int):
    response = client.delete(f"/crops/{crop_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


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
        delete_user(client, user_id=user_id)
        response = get_all_users(client)
        assert len(response) == 0


def test_crud_crops():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_crops(client)
        assert len(response) == 0
        # create an entry
        response = create_crop(client)
        crop_id = response["id"]
        # get all entries
        response = get_all_crops(client)
        assert len(response) == 1
        assert response[0]["year"] == 2000
        assert response[0]["crop_type"] == "corn"

        # get 1 entry
        response = get_crop(client, crop_id)
        assert response["year"] == 2000
        assert response["crop_type"] == "corn"

        delete_crop(client, crop_id=crop_id)
        response = get_all_crops(client)
        assert len(response) == 0

        delete_crop_404_error(client, crop_id=crop_id)
        create_crop_400_error(client)
        get_crop_404_error(client, crop_id)
