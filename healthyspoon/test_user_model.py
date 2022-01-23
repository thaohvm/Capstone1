import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///healthy_spoon_test"

from app import app

db.create_all()

def create_user():
    u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            location="United State"
        )
    u.id = 3333

    db.session.add(u)
    db.session.commit()

    return u

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        u1 = User.register("test1", "password", "email1@email.com", "United State")
        uid1 = 1111
        u1.id = uid1

        u2 = User.register("test2", "password", "email2@email.com", "Canada")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            location="United State"
        )

        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_repr(self):
        """Does repr work?"""

        self.assertEqual(repr(self.u1), '<User #1111: test1, email1@email.com, United State>')
