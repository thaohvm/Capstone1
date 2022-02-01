# Healthy Spoon Web Application
Project's title: HealthySpoon.


This project is deployed on https://healthy-spoon.herokuapp.com/

## What the website does/ User flow
Users can register account and need to fill in their information including username, password, email. They can search for recipes which they prefer by ingredients (such as mushroom, egg,..). After the search, they can find a list of recipes that match their requirements. They can click on any of the recipes to see the details of the recipes. In the detail page, users can see all the ingredients, steps of the recipes. If they like the recipes and want to save it to read in the future, they can click on the button “Save to my Favorite” to add the recipes to their personal page. Additionally, they also can see the recipes that saved by others people who is in the same country.

## Features
- Searching: user can search recipes based on their favorite ingredients or their diet. This features can help user to easily find the recipes that include the ingrdients on their fridge.
- Save recipes to favorite page: this can helps users to track their recipes that they want to read again in the future.
- Looking for recipes that saved by people from the same country. That helps user to easily find out their common recipes

## APIs: Spoonacular API
API link: https://spoonacular.com/food-api/docs
The API automatically analyze recipes to check for ingredients that contain common allergens, such as wheat, dairy, eggs, soy, nuts, etc. They also determine whether a recipe is vegan, vegetarian, Paleo friendly, Whole30 compliant, and more.

## Technology Stack
Database: Postgresql
Flask web framework with SQLAlchemy, Jinja, Flask, WTForms


## Database Schema
![alt database schema](https://github.com/thaohvm/Capstone1/blob/master/docs/DBSchema.png?raw=true)
