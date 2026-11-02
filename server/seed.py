from app import create_app
from extensions import db
from models import User, Note


app = create_app()


def seed_database():
    with app.app_context():

        # Create the first sample user if they do not exist.
        user1 = User.query.filter_by(
            username="demo_user"
        ).first()

        if not user1:
            user1 = User(username="demo_user")
            user1.set_password("DemoPassword123")
            db.session.add(user1)
            db.session.flush()

        # Create the second sample user if they do not exist.
        user2 = User.query.filter_by(
            username="another_user"
        ).first()

        if not user2:
            user2 = User(username="another_user")
            user2.set_password("AnotherPassword123")
            db.session.add(user2)
            db.session.flush()

        # Add sample notes without duplicating them on reruns.
        sample_notes = [
            {
                "title": "Learning Flask",
                "content": "Flask is a Python web framework.",
                "user_id": user1.id
            },
            {
                "title": "Learning JWT",
                "content": "JWT is used for stateless authentication.",
                "user_id": user1.id
            },
            {
                "title": "Private Note",
                "content": "This note belongs only to another user.",
                "user_id": user2.id
            }
        ]

        for note_data in sample_notes:
            existing_note = Note.query.filter_by(
                title=note_data["title"],
                user_id=note_data["user_id"]
            ).first()

            if not existing_note:
                note = Note(**note_data)
                db.session.add(note)

        db.session.commit()

        print("Database seeding completed successfully.")


if __name__ == "__main__":
    seed_database()