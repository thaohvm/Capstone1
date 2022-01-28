from app import app, CURR_USER_KEY
import os
from unittest import TestCase
from models import db, connect_db, User, Recipes, Ingredients, RecipesIngredients, RecipesUsers

os.environ['DATABASE_URL'] = "postgresql:///healthy_spoon_test"


def clear_database(model_name):
    """Clear database"""
    results = model_name.query.all()
    for result in results:
        db.session.delete(result)
    db.session.commit()


db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class DietSpoonViewTestCase(TestCase):
    """Test each function of webpage"""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

        # Delete all from database
        for model in [User, Recipes, RecipesUsers, RecipesIngredients, Ingredients]:
            clear_database(model)

        testuser1 = User.register(username="testuser1",
                                    email="test1@test.com",
                                    password="password1",
                                    location="United State"
                                    )
        testuserid1 = 1111
        testuser1.id = testuserid1
        testuser2 = User.register(username="testuser2",
                                    email="test2@test.com",
                                    password="password2",
                                    location="United State"
                                    )
        testuserid2 = 2222
        testuser2.id = testuserid2
        db.session.add(testuser1)
        db.session.add(testuser2)
        db.session.commit()

    def tearDown(self):
        """Tear down"""
        db.session.rollback()

    def test_guest_account(self):
        """Test if guest can read saved recipes/ favourite list"""
