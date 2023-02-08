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


def create_feature(client) -> dict:
    response = client.post("/features", json={"name": "Fall Tillage", "collectionMethod": "selector", "possibleValues": '"Reduced Tillage", "Conventional Tillage"'})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

def get_all_features(client) -> dict:
    response = client.get("/features")
    assert response.status_code == status.HTTP_200_OK
    return response.json()

def delete_feature(client, feature_id: int):
    response = client.delete(f"/features/{feature_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_crud_features():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_features(client)
        assert len(response) == 0
        # create an entry
        response = create_feature(client)
        feature_id = response["id"]
        # get entry
        response = get_all_features(client)
        assert len(response) == 1
        assert response[0]["id"] == feature_id
        assert response[0]["name"] == "Fall Tillage"
        response = delete_feature(client, feature_id=feature_id)
        response = get_all_features(client)
        assert len(response) == 0


def create_selector_feature_no_possible_values(client):
    response = client.post("/features", json={"name": "Fall Tillage", "collectionMethod": "selector"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == 'selector features must have possible values'

def create_slider_feature_no_min_value(client):
    response = client.post("/features", json={"name": "Fall Tillage", "collectionMethod": "slider", "maxValue": 5.0 })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == 'slider features must have min and max values'

def create_feature_no_name(client):
    response = client.post("/features", json={"collectionMethod": "slider", "maxValue": 5.0, "minValue": 1.0 })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def create_feature_incorrect_collection_method(client):
    response = client.post("/features", json={"name": "Summer Crop", "collectionMethod": 123})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_error_cases():
    with TestClient(app) as client:
        create_selector_feature_no_possible_values(client)
        create_slider_feature_no_min_value(client)
        create_feature_no_name(client)
        create_feature_incorrect_collection_method(client)
        # expect nothing to have been created in db
        response = get_all_features(client)
        assert len(response) == 0

def create_user_input_table(client) -> dict:
    response = client.post("/userInputTables", json={"features": "3792987462,848397756", "startYear": 2015, "endYear": 2023})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

def get_all_user_input_tables(client) -> dict:
    response = client.get("/userInputTables")
    assert response.status_code == status.HTTP_200_OK
    return response.json()

def delete_user_input_table(client, user_input_table_id: int):
    response = client.delete(f"/userInputTables/{user_input_table_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def user_input_valid_feature_ids(client) -> dict:
    response = client.post("/userInputTables", json={"features": "3792987462,848397756", "startYear": 2015, "endYear": 2023})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

def test_crud_user_input_tables():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_user_input_tables(client)
        assert len(response) == 0
        # create an entry
        response = create_user_input_table(client)
        user_input_table_id = response["id"]
        # get entry
        response = get_all_user_input_tables(client)
        assert len(response) == 1
        assert response[0]["id"] == user_input_table_id
        assert response[0]["features"] == "3792987462,848397756"
        assert response[0]["startYear"] == 2015
        assert response[0]["endYear"] == 2023

        response = delete_user_input_table(client, user_input_table_id=user_input_table_id)
        response = get_all_user_input_tables(client)
        assert len(response) == 0
