def test_signup(client):
    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "Password123",
            "password_confirmation": "Password123"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "token" in data
    assert data["user"]["username"] == "testuser"
    assert data["user"]["id"] is not None


def test_signup_password_mismatch(client):
    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "Password123",
            "password_confirmation": "Different123"
        }
    )

    assert response.status_code == 400


def test_login(client):
    # First register a user.
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "Password123",
            "password_confirmation": "Password123"
        }
    )

    # Then attempt to log in.
    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "Password123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "token" in data
    assert data["user"]["username"] == "testuser"


def test_login_invalid_password(client):
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "Password123",
            "password_confirmation": "Password123"
        }
    )

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401


def test_me_with_valid_token(client):
    signup_response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "Password123",
            "password_confirmation": "Password123"
        }
    )

    token = signup_response.get_json()["token"]

    response = client.get(
        "/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["username"] == "testuser"


def test_me_without_token(client):
    response = client.get("/me")

    assert response.status_code == 401

def test_signup_with_invalid_json_body(client):
    response = client.post(
        "/signup",
        json=["testuser", "Password123"]
    )

    assert response.status_code == 400
    assert "errors" in response.get_json()


def test_signup_with_non_string_username(client):
    response = client.post(
        "/signup",
        json={
            "username": 123,
            "password": "Password123",
            "password_confirmation": "Password123"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["errors"] == ["Username must be a string"]


def test_signup_with_non_string_password(client):
    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": 12345,
            "password_confirmation": "12345"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["errors"] == ["Password must be a string"]


def test_login_with_non_string_username(client):
    response = client.post(
        "/login",
        json={
            "username": 123,
            "password": "Password123"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["errors"] == ["Username must be a string"]