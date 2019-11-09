from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Recipe

import ast

app_data = {
    "name":         "Meal Prep Web App",
    "description":  "A basic MealPrep Flask app",
    "author":       "Cameron Fabbri",
    "html_title":   "Meal Prep Sunday",
    "project_name": "MealPrep",
    "keywords":     "meal, mealprep, prep, dinner"
}


# Connect to the database
engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)


@app.route('/add', methods=['GET','POST'])
def add():

    if request.method == 'POST':

        rf = request.form

        new_recipe = Recipe(
            title=rf['title'],
            ingredients=rf['ingredients'],
            instructions=rf['instructions'])

        session.add(new_recipe)
        session.commit()

        return redirect(url_for('index'))

    else:
        return render_template('add.html', app_data=app_data)


@app.route('/view')
def view():

    view_recipes_ = session.query(Recipe).all()
    recipe_list = []

    for v in view_recipes_:

        v_ingredients = ast.literal_eval(v.ingredients)

        ingredients = []
        for ingredient in v_ingredients:
            ingredients.append(ingredient['text'])

        view_recipes = {}
        view_recipes['title'] = v.title
        view_recipes['ingredients'] = ingredients
        recipe_list.append(view_recipes)

    print(recipe_list)

    return render_template('view.html', app_data=app_data, recipe_list=recipe_list)

@app.route('/b3')
def b3():
    return render_template('b3.html', app_data=app_data)


# ------- DEVELOPMENT CONFIG -------
if __name__ == '__main__':
    app.run(debug=True)
