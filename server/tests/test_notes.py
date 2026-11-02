def create_user_and_token(client, username):
    response = client.post(
        "/signup",
        json={
            "username": username,
            "password": "Password123",
            "password_confirmation": "Password123"
        }
    )

    return response.get_json()["token"]


def test_create_note(client):
    token = create_user_and_token(client, "user1")

    response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "My First Note",
            "content": "Learning automated testing."
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["title"] == "My First Note"
    assert data["content"] == "Learning automated testing."
    assert data["user_id"] == 1


def test_get_notes(client):
    token = create_user_and_token(client, "user1")

    client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "First Note",
            "content": "First content"
        }
    )

    response = client.get(
        "/notes",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["total"] == 1
    assert len(data["notes"]) == 1


def test_get_single_note(client):
    token = create_user_and_token(client, "user1")

    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "My Note",
            "content": "Some content"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.get_json()["title"] == "My Note"


def test_update_note(client):
    token = create_user_and_token(client, "user1")

    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Original Title",
            "content": "Original content"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Title"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["title"] == "Updated Title"


def test_delete_note(client):
    token = create_user_and_token(client, "user1")

    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Note to Delete",
            "content": "This note will be deleted."
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    # Verify that the note no longer exists.
    get_response = client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_response.status_code == 404


def test_user_cannot_access_another_users_note(client):
    # Create User 1 and User 2.
    token1 = create_user_and_token(client, "user1")
    token2 = create_user_and_token(client, "user2")

    # User 2 creates a private note.
    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token2}"},
        json={
            "title": "Private Note",
            "content": "Only User 2 should see this."
        }
    )

    note_id = create_response.get_json()["id"]

    # User 1 tries to access User 2's note.
    response = client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token1}"}
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_note(client):
    token1 = create_user_and_token(client, "user1")
    token2 = create_user_and_token(client, "user2")

    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token2}"},
        json={
            "title": "Private Note",
            "content": "Original content"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token1}"},
        json={"title": "Hacked"}
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_note(client):
    token1 = create_user_and_token(client, "user1")
    token2 = create_user_and_token(client, "user2")

    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token2}"},
        json={
            "title": "Private Note",
            "content": "Original content"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token1}"}
    )

    assert response.status_code == 404

def test_notes_pagination(client):
    token = create_user_and_token(client, "pagination_user")

    # Create 3 notes.
    for i in range(3):
        client.post(
            "/notes",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": f"Note {i + 1}",
                "content": f"Content {i + 1}"
            }
        )

    # Request only 2 notes per page.
    response = client.get(
        "/notes?page=1&per_page=2",
        headers={"Authorization": f"Bearer {token}"}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert len(data["notes"]) == 2
    assert data["total"] == 3
    assert data["pages"] == 2
    assert data["page"] == 1

def test_create_note_without_title(client):
    token = create_user_and_token(client, "validation_user")

    response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "This note has no title."
        }
    )

    assert response.status_code == 400


def test_create_note_without_content(client):
    token = create_user_and_token(client, "validation_user")

    response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Missing Content"
        }
    )

    assert response.status_code == 400

def test_create_note_with_invalid_json_body(client):
    token = create_user_and_token(client, "invalid_json_user")

    response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json=["Invalid", "body"]
    )

    assert response.status_code == 400


def test_create_note_with_non_string_title(client):
    token = create_user_and_token(client, "invalid_title_user")

    response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": 12345,
            "content": "Valid content"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["errors"] == ["Title must be a string"]


def test_create_note_with_non_string_content(client):
    token = create_user_and_token(client, "invalid_content_user")

    response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Valid title",
            "content": ["Invalid content"]
        }
    )

    assert response.status_code == 400
    assert response.get_json()["errors"] == ["Content must be a string"]


def test_update_note_with_invalid_json_body(client):
    token = create_user_and_token(client, "update_invalid_user")

    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Original title",
            "content": "Original content"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=["Invalid", "body"]
    )

    assert response.status_code == 400


def test_update_note_with_non_string_title(client):
    token = create_user_and_token(client, "update_title_user")

    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Original title",
            "content": "Original content"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": 12345}
    )

    assert response.status_code == 400
    assert response.get_json()["errors"] == ["Title must be a string"]


def test_update_note_with_non_string_content(client):
    token = create_user_and_token(client, "update_content_user")

    create_response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Original title",
            "content": "Original content"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": ["Invalid content"]}
    )

    assert response.status_code == 400
    assert response.get_json()["errors"] == ["Content must be a string"]