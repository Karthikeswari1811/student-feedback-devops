import pytest

from app import app, init_db


@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.test_client() as client:
        init_db()
        yield client


def test_home_page(client):

    response = client.get("/")

    assert response.status_code == 200


def test_about_page(client):

    response = client.get("/about")

    assert response.status_code == 200


def test_health_page(client):

    response = client.get("/health")

    assert response.status_code == 200


def test_submit_empty_form(client):

    response = client.post(
        "/submit",
        data={
            "name": "",
            "email": "",
            "message": ""
        }
    )

    assert response.status_code == 400