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