from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, RecipesUsers, Recipes, Ingredients, RecipesIngredients

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///healthy_spoon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

@app.route("/")
def homepage():
    return render_template("index.html")
