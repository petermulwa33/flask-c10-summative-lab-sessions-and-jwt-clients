# Flask JWT Notes API

## Project Overview

This project is a Flask REST API that provides secure user authentication and personal note management using JSON Web Tokens (JWT).

Users can register, log in, and manage their own notes. Each note belongs to a specific user, and users cannot access, modify, or delete notes belonging to other users.

The project uses Flask, SQLAlchemy, Flask-Migrate, Flask-Bcrypt, and Flask-JWT-Extended.

## Technologies Used

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- SQLite
- Pytest
- React frontend

## Project Structure

```text
project/
├── client-with-jwt/
├── client-with-sessions/
├── server/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── seed.py
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── resources/
│   │   ├── auth.py
│   │   └── notes.py
│   ├── migrations/
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       └── test_notes.py
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/petermulwa33/flask-c10-summative-lab-sessions-and-jwt-clients.git

cd flask-c10-summative-lab-sessions-and-jwt-clients
```

### 2. Navigate to the backend

```bash
cd server
```

### 3. Install dependencies

Install Pipenv if it is not already installed:

```bash
pip install pipenv
```

Install the project dependencies:

```bash
pipenv sync
```

### 4. Configure environment variables

Configure strong secret keys before running the application:

```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"

export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

The application uses SQLite by default. A custom database URL can be provided through `DATABASE_URL`.

### 5. Initialize the database

Apply the existing database migrations:

```bash
pipenv run flask --app app db upgrade
```

### 6. Seed the database

```bash
pipenv run python seed.py
```

The seed script creates demonstration users and sample notes.

### 7. Start the backend

```bash
pipenv run flask --app app run --port 5555 --debug
```

The backend will be available at:

`http://127.0.0.1:5555`

## Authentication Endpoints

All authentication responses use JSON.

### Register a user

**POST** `/signup`

Request body:

```json
{
  "username": "example_user",
  "password": "Password123",
  "password_confirmation": "Password123"
}
```

A successful registration returns a JWT token and user information.

### Log in

**POST** `/login`

Request body:

```json
{
  "username": "example_user",
  "password": "Password123"
}
```

A successful login returns a JWT access token.

### Get the authenticated user

**GET** `/me`

Required header:

```text
Authorization: Bearer YOUR_JWT_TOKEN
```

Returns the authenticated user's ID and username.

## Notes Endpoints

All Notes endpoints require a valid JWT access token.

### List notes

**GET** `/notes`

Supports pagination:

```text
GET /notes?page=1&per_page=10
```

Returns only notes belonging to the authenticated user.

### Create a note

**POST** `/notes`

Request body:

```json
{
  "title": "Learning Flask",
  "content": "Flask is a Python web framework."
}
```

The authenticated user's ID is automatically assigned to the note.

### Retrieve a note

**GET** `/notes/<id>`

Retrieves a specific note belonging to the authenticated user.

### Update a note

**PATCH** `/notes/<id>`

Request body:

```json
{
  "title": "Updated title",
  "content": "Updated note content."
}
```

### Delete a note

**DELETE** `/notes/<id>`

Deletes a note belonging to the authenticated user.

## Database Models

### User

The User model contains:

- `id`: Primary key.
- `username`: Unique username.
- `password_hash`: Securely hashed password.

### Note

The Note model contains:

- `id`: Primary key.
- `title`: Note title.
- `content`: Note content.
- `user_id`: Foreign key referencing the note owner.
- `created_at`: Creation timestamp.
- `updated_at`: Last update timestamp.

Each user can have multiple notes through a one-to-many relationship.

## Security Features

- Passwords are hashed using Flask-Bcrypt.
- JWT tokens protect authenticated endpoints.
- User identity is extracted from the JWT token.
- Notes are filtered by the authenticated user's ID.
- Users receive a 404 response when attempting to access another user's note.
- Registration validates required fields and password confirmation.

## Running Tests

From the `server` directory, execute:

```bash
pipenv run pytest -v
```

The test suite covers:

- User registration.
- Login and invalid credentials.
- JWT authentication.
- Notes creation, retrieval, updating and deletion.
- User ownership restrictions.
- Pagination.
- Required note fields.

The current test suite contains 17 passing tests.

## Frontend

The supplied JWT React frontend is located in `client-with-jwt/`.

Install its dependencies:

```bash
cd ../client-with-jwt
npm install
```

Start the frontend:

```bash
npm start
```

The frontend communicates with the Flask backend through the configured proxy on port 5555.

## License

This project was developed as part of a Full Stack Software Engineering summative assignment at Moringa School.