
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Note

notes_bp = Blueprint("notes", __name__)


def serialize_note(note):
    """Convert a Note object into JSON-friendly data."""
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "user_id": note.user_id,
        "created_at": note.created_at.isoformat() if note.created_at else None,
        "updated_at": note.updated_at.isoformat() if note.updated_at else None
    }


# GET ALL NOTES
@notes_bp.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1 or per_page < 1 or per_page > 100:
        return {"errors": ["Invalid pagination parameters"]}, 400

    pagination = Note.query.filter_by(user_id=user_id).order_by(
        Note.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "notes": [serialize_note(note) for note in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": pagination.page,
        "per_page": pagination.per_page
    }, 200


# CREATE A NOTE
@notes_bp.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()

    if not title or not content:
        return {"errors": ["Title and content are required"]}, 400

    note = Note(
        title=title,
        content=content,
        user_id=user_id
    )

    db.session.add(note)
    db.session.commit()

    return serialize_note(note), 201


# GET ONE NOTE
@notes_bp.route("/notes/<int:note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id):
    user_id = int(get_jwt_identity())

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        return {"errors": ["Note not found"]}, 404

    return serialize_note(note), 200


# UPDATE A NOTE
@notes_bp.route("/notes/<int:note_id>", methods=["PATCH"])
@jwt_required()
def update_note(note_id):
    user_id = int(get_jwt_identity())

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        return {"errors": ["Note not found"]}, 404

    data = request.get_json() or {}

    if "title" in data:
        title = data["title"].strip() if isinstance(data["title"], str) else ""
        if not title:
            return {"errors": ["Title cannot be empty"]}, 400
        note.title = title

    if "content" in data:
        content = data["content"].strip() if isinstance(data["content"], str) else ""
        if not content:
            return {"errors": ["Content cannot be empty"]}, 400
        note.content = content

    db.session.commit()

    return serialize_note(note), 200


# DELETE A NOTE
@notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    user_id = int(get_jwt_identity())

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        return {"errors": ["Note not found"]}, 404

    db.session.delete(note)
    db.session.commit()

    return {"message": "Note deleted successfully"}, 200
