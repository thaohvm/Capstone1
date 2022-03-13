# About the project
Project's title: HealthySpoon.

This project is built during the time I attend Software Engineering Career Track bootcamp.

Example template:

<img src="https://github.com/thaohvm/Capstone1/blob/master/static/index-image.png?raw=true" width="500">

## Built With

* [Bootstrap](https://getbootstrap.com)
* [Python](https://www.python.org/)
* [PostSQL](https://www.postgresql.org/)
* [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Jinja](https://jinja2docs.readthedocs.io/en/stable/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [WTForms](https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

This project is deployed on https://healthy-spoon.herokuapp.com/

## What the website does/ User flow
Users can register account and need to fill in their information including username, password, email.
They can search for recipes which they prefer by ingredients (such as mushroom, egg,..). After the search, they can find a list of recipes that match their requirements. They can click on any of the recipes to see the details of the recipes. In the detail page, users can see all the ingredients, steps of the recipes. If they like the recipes and want to save it to read in the future, they can click on the button “Save to my Favorite” to add the recipes to their personal page. Additionally, they also can see the recipes that saved by others people who is in the same country.

## Getting Started
### Installation
1. Get a free API Key at [https://spoonacular.com/food-api/docs](https://spoonacular.com/food-api/docs)
2. Clone the repo
   ```sh
   git clone https://github.com/thaohvm/Capstone1
   ```
3. Create database for both running website and testing
   ```sh
   createdb healthy-spoon
   createdb healthy-spoon-test
   ```
4. Install environtment requirements
   cd to the directory where requirements.txt is located
   ```sh
   $ python3 -m venv venv
   $ source venv/bin/activate
   (env) $ pip install -r requirements.txt
   ```
5. Run the website:
   ```sh
   (venv) $ python seed.py
   (venv) $ flask run
   ```
6. Go to local website: http://localhost:5000
   or live application at: https://healthy-spoon.herokuapp.com/

### Testing

   ```sh
    (venv) $ python -m unittest test_login_logout
    (venv) $ python -m unittest test_user_model
    (venv) $ python -m unittest test_web_function
   ```
## Features
- Searching: user can search recipes based on their favorite ingredients or their diet. This features can help user to easily find the recipes that include the ingrdients on their fridge.
- Save recipes to favorite page: this can helps users to track their recipes that they want to read again in the future.
- Looking for recipes that saved by people from the same country. That helps user to easily find out their common recipes

## APIs: Spoonacular API
API link: https://spoonacular.com/food-api/docs
The API automatically analyze recipes to check for ingredients that contain common allergens, such as wheat, dairy, eggs, soy, nuts, etc. They also determine whether a recipe is vegan, vegetarian, Paleo friendly, Whole30 compliant, and more.

## Database Schema
![alt database schema](https://github.com/thaohvm/Capstone1/blob/master/docs/DBSchema.png?raw=true)
