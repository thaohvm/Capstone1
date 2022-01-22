from email.mime import image
from turtle import title
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import exc

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    recipes = db.relationship(
        'Recipes', secondary='recipes_users', backref='users', lazy="dynamic")

    @classmethod
    def register(cls, username, password, email, location):
        """Register user w/hashed password and return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            email=email,
            location=location
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False


class Recipes(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    readyInMinutes = db.Column(db.Integer, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    vegetarian = db.Column(db.Boolean, default=False, nullable=False)
    vegan = db.Column(db.Boolean, default=False, nullable=False)
    glutenFree = db.Column(db.Boolean, default=False, nullable=False)
    dairyFree = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Recipes {self.id}: {self.title}>"

    def serialize(self):
        return {'id': self.id,
                'title': self.title,
                'summary': self.summary,
                'image': self.image,
                'readyInMinutes': self.readyInMinutes,
                'instructions': self.instructions,
                'vegetarian': self.vegetarian,
                'vegan': self.vegan,
                'glutenFree': self.glutenFree,
                'dairyFree': self.dairyFree
                }


class RecipesUsers(db.Model):
    __tablename__ = "recipes_users"

    recipes_id = db.Column(db.Integer,
                           db.ForeignKey("recipes.id"),
                           primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        primary_key=True)

    def __repr__(self):
        return f"<RecipesUsers {self.recipes_id} - {self.user_id}>"


class Ingredients(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    recipes = db.relationship(
        'Recipes', secondary='recipes_ingr', backref='ingr', lazy="dynamic")

    def __repr__(self):
        return f"<Ingredients {self.id} : {self.name}>"


class RecipesIngredients(db.Model):
    __tablename__ = "recipes_ingr"

    recipes_id = db.Column(db.Integer,
                           db.ForeignKey("recipes.id"),
                           primary_key=True)
    ingr_id = db.Column(db.Integer,
                        db.ForeignKey("ingredients.id"),
                        primary_key=True)

    def __repr__(self):
        return f"<RecipesIngredients {self.recipes_id} - {self.ingr_id}>"
