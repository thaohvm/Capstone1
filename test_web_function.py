import os
from unittest import TestCase
from models import (
    db,
    connect_db,
    User,
    Recipes,
    Ingredients,
    RecipesIngredients,
    RecipesUsers,
)

os.environ["DATABASE_URL"] = "postgresql:///healthy_spoon_test"

from app import app, CURR_USER_KEY

app.config["WTF_CSRF_ENABLED"] = False


def clear_database(model_name):
    """Clear database"""
    results = model_name.query.all()
    for result in results:
        db.session.delete(result)
    db.session.commit()


db.drop_all()
db.create_all()


class DietSpoonViewTestCase(TestCase):
    """Test each function of webpage"""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

        # Delete all from database
        for model in [User, Recipes, RecipesUsers, RecipesIngredients, Ingredients]:
            clear_database(model)

        testuser1 = User.register(
            username="testuser1",
            email="test1@test.com",
            password="password1",
            location="United State",
        )
        self.testuser1_id = 1111
        testuser1.id = self.testuser1_id
        testuser2 = User.register(
            username="testuser2",
            email="test2@test.com",
            password="password2",
            location="United State",
        )
        self.testuser2_id = 2222
        testuser2.id = self.testuser2_id
        db.session.add(testuser1)
        db.session.add(testuser2)
        db.session.commit()

        self.recipe1_id = 637569
        self.recipe1_title = "Cheese Pork Chops"
        recipe1 = Recipes(
            id=self.recipe1_id,
            title=self.recipe1_title,
            summary="Cheese Pork Chops",
            image="https://spoonacular.com/recipeImages/637569-556x370.jpg",
            readyInMinutes="30",
            instructions="<ol><li>In a heavy bottom skillet melt the butter with the olive oil. Saut` the pork chops over medium high 3 minutes on each sided. Lower the heat to medium and cook for another 5 to 6 minutes for side.</li><li>Salt and pepper to taste.</li><li>Meanwhile turn on the broil. Mix together in a bowl the heavy cream, mustard and the cheese. Remove the chops from the stove and place them in a oven proof dish. Spread the cheese-cream mixture over the chops and broil for about 5 minutes.</li></ol>",
            vegetarian=False,
            vegan=False,
            glutenFree=True,
            dairyFree=False,
        )

        self.recipe2_id = 637535
        self.recipe2_title = "Cheese and Leek Strata"
        recipe2 = Recipes(
            id=self.recipe2_id,
            title=self.recipe2_title,
            summary="Cheese and Leek Strata",
            image="https://spoonacular.com/recipeImages/637569-556x370.jpg",
            readyInMinutes="30",
            instructions="<ol><li>Preheat oven to 350 degrees F Combine eggs, milk, beer, garlic, salt & pepper in a large bowl and beat well until blended Place 1/2 of the bread cubes on bottom of greased 2.5-quart round baking dish Sprinkle half the leeks and half the bell pepper over bread pieces Top with half the Swiss cheese and half the cheddar cheese Repeat layers with remaining ingredients, ending with cheddar cheese Pour egg mixture evenly over top Cover tightly with foil or plastic wrap and weigh top of the strata down with a slightly smaller baking dish Refrigerate strata at least 2 hours or overnight Bake, uncovered, 40 minutes or until center is set Serve warm</li></ol>",
            vegetarian=True,
            vegan=False,
            glutenFree=False,
            dairyFree=False,
        )

        db.session.add(recipe1)
        db.session.add(recipe2)
        db.session.commit()

        # recipe2_user1 = RecipesUsers(
        #     recipes_id=self.recipe2_id,
        #     user_id=self.testuser1_id
        # )
        # db.session.add(recipe2_user1)
        # db.session.commit()

    def tearDown(self):
        """Tear down"""
        db.session.rollback()

    def test_recipe_detail(self):
        """Test if user can see add to favorite from recipe details page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1_id

            res = c.get(f"/recipe/{self.recipe1_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"{self.recipe1_title}", html)
            self.assertIn(f"Add to favorite", html)

    def test_recipe_detail_no_session(self):
        """Test if guest cannot see add to favorite option from recipe details page"""
        with self.client as c:
            res = c.get(f"/recipe/{self.recipe1_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"{self.recipe1_title}", html)
            self.assertNotIn(f"Add to favorite", html)

    def test_nav(self):
        """Test if log in user can see My Favorites tab from nav bar"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1_id

            res = c.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"My Favorites", html)

    def test_nav_no_session(self):
        """Test if guest cannot see My Favorites tab from nav bar"""
        with self.client as c:
            res = c.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(f"My Favorites", html)

    def test_saved_recipes(self):
        """Test if log in user can see saved recipes"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1_id

            res = c.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"Try recipes saved by people from your country", html)

    def test_saved_recipes_no_session(self):
        """Test if guest cannot see recipes saved by others"""
        with self.client as c:
            res = c.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(f"Try recipes saved by people from your country", html)

    def test_add_to_favorite(self):
        """Test if user can read saved recipes from My Favorites"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1_id

            res = c.post(
                f"/recipe/{self.recipe2_id}/favorite",
                data={"favorited": "False"},
                follow_redirects=True,
            )
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(res.history), 1)  # Ensure redirected
            self.assertEqual(res.history[0].status_code, 302)
            self.assertIn(
                f"/recipe/{self.recipe2_id}",
                res.history[0].location,
            )

            favorited = RecipesUsers.query.filter_by(
                user_id=self.testuser1_id, recipes_id=self.recipe2_id
            ).first()
            self.assertEqual(self.recipe2_id, favorited.recipes_id)
