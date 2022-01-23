from email.mime import image
from traceback import StackSummary
from turtle import title
from flask import Flask, request, redirect, render_template, session, g, flash, jsonify, abort
from forms import RegisterForm, LoginForm, FavoriteForm
from models import db, connect_db, User, RecipesUsers, Recipes, Ingredients, RecipesIngredients
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup
import requests
import sys

API_BASE_URL = "https://api.spoonacular.com/recipes/"
key = "e04fa2cf19db48a2a68c53f3f6d8d84c"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///healthy_spoon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

CURR_USER_KEY = "curr_user"


connect_db(app)

##############################################################################
# Cache functions


def get_recipe_from_db_or_404(recipe_id):
    recipe = Recipes.query.get(recipe_id)
    if not recipe:
        # Not found in DB, need to fetch from API
        print(f'Recipe #{recipe_id} not found in database')
        res = requests.get(
            f"{API_BASE_URL}/{recipe_id}/information", params={"apiKey": key})
        results = res.json()
        if res.status_code == 200 and results["id"] == recipe_id:
            print(f'Recipe #{recipe_id} fetched from API')
            # Valid ID from API, need to cache ingredients first, and then recipe
            recipe = Recipes(
                id=recipe_id,
                title=results["title"],
                summary=results["summary"],
                image=results["image"],
                readyInMinutes=results["readyInMinutes"],
                instructions=results["instructions"],
                vegetarian=results["vegetarian"],
                vegan=results["vegan"],
                glutenFree=results["glutenFree"],
                dairyFree=results["dairyFree"],
            )

            for i in results["extendedIngredients"]:
                ingredient = Ingredients.query.get(i["id"])
                if not ingredient:
                    # Ingredient not found in DB, need to store first
                    print(
                        f'Ingredient #{i["id"]} not found in database')
                    ingredient = Ingredients(
                        id=i["id"],
                        name=i["name"],
                    )
                    db.session.add(ingredient)
                    db.session.commit()
                recipe.ingr.append(ingredient)

            db.session.add(recipe)
            db.session.commit()
    else:
        print(f'Recipe #{recipe_id} loaded from database')

    # Always filled in cache if exists
    return Recipes.query.get_or_404(recipe_id)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                location=form.location.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have successfully logout!", "success")
    return redirect("/")

##############################################################################
# Homepage and error pages


@app.route("/")
def homepage():
    if g.user:
        user_country = g.user.location
        similar_users = User.query.filter(User.location.like(f"%{user_country}%")).all()
        saved_recipes = []
        for user in similar_users:
            saved_recipes.extend(user.recipes)
        return render_template("index.html", saved_recipes=saved_recipes)
    else:
        return render_template("index.html")


@app.route("/search")
def handle_search():
    query = request.args["query"]
    res = requests.get(f"{API_BASE_URL}/complexSearch", params={"apiKey": key,
                       "query": {query}, "addRecipeInformation": "true"})
    results = res.json()["results"]
    for r in results:
        soup = BeautifulSoup(r["summary"])
        for a in soup.findAll('a'):
            a.replaceWithChildren()
        r["summary"] = str(soup)
    return render_template("search.html", query=query, search_results=results)


@app.route("/recipe/<int:recipe_id>")
def get_recipe_detail(recipe_id):
    recipe = get_recipe_from_db_or_404(recipe_id)
    favorited = bool(g.user and g.user.recipes.filter_by(id=recipe_id).first())
    favorite_form = FavoriteForm(favorited=str(favorited))
    return render_template("recipe.html", recipe=recipe, favorite_form=favorite_form, favorited=favorited)


@app.route("/<int:user_id>/favorites")
def show_favorite(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    return render_template('favorites.html', user=user, favorites=user.recipes)


@app.route("/recipe/<int:recipe_id>/favorite", methods=["POST"])
def add_favorite(recipe_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipe = get_recipe_from_db_or_404(recipe_id)
    form = FavoriteForm()
    if form.validate_on_submit():
        favorited = form.favorited.data == "True"
        if favorited:
            # Remove favorite
            g.user.recipes.remove(recipe)
            db.session.commit()
        else:
            # Add favorite
            g.user.recipes.append(recipe)
            db.session.commit()
    return redirect(f"/recipe/{recipe_id}")
