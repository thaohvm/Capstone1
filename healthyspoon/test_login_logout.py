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


class LoginViewTestCase(TestCase):
    """Test views for login, logout, and signup."""

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

    def test_login_form(self):
        """Test the login form displayed and rendered correctly"""
        with self.client as c:

            resp = c.get("/login")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username", html)
            self.assertIn("Password", html)

    def test_login_user(self):
        """Test the log in function is worked if right username, password is filled"""
        with self.client as c:

            resp = c.post("/login", data={
                "username": "testuser1",
                "password": "password1"
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search", html)

    def test_wrong_password(self):
        """Test the function is not worked if wrong password is filled"""
        with self.client as c:

            resp = c.post("/login", data={
                "username": "testuser1",
                "password": "wrongpassword1"
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login", html)

    def test_register_form(self):
        """Test the register form is displayed and rendered correctly """
        with self.client as c:

            resp = c.get("/signup")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username", html)
            self.assertIn("Password", html)
            self.assertIn("Email", html)
            self.assertIn("Location", html)

    def test_signup_user(self):
        """Test new user can sign up with valid account """
        with self.client as c:
            resp = c.post("/signup", data={
                "username": "testuser3",
                "password": "password3",
                "email": "test3@test.com",
                "location": "United State",
                }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search", html)

    def test_duplicate_user_signup(self):
        """Test user can sign up with the account which have been registered before"""
        with self.client as c:
            resp = c.post("/signup", data={
                "username": "testuser1",
                "password": "password1",
                "email": "test1@test.com",
                "location": "United State",
                }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign up!", html)

    def test_logout_user(self):
        """Test user is logout from both UI and backend"""
        with self.client as c:

            testuser1 = User.query.filter_by(username="testuser1").first()
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = testuser1.id

            resp = c.get("/logout",follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login",html)
