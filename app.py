from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from db_setup import Base, Recipe, Week

import numpy as np
import datetime
import random
import ast

app_data = {
    "name":         "Meal Prep Web App",
    "description":  "A basic MealPrep Flask app",
    "author":       "Cameron Fabbri",
    "html_title":   "Meal Prep Sunday",
    "project_name": "MealPrep",
    "keywords":     "meal, mealprep, prep, dinner"
}


d = datetime.date.today()
_, week_num, _ = d.isocalendar()


#engine = create_engine('sqlite:///recipes.db')
from db_setup import engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
#session_factory = sessionmaker(bind=engine)
#session = scoped_session(session_factory)

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':

        # Get old recipe from Week table
        old_rid = int(request.form['meal'])
        old_recipe = session.query(Week).get(old_rid)

        # Get new random recipe
        num = session.query(Recipe).count()
        new_rid = random.randint(1, num)

        new_recipe = session.query(Recipe).get(new_rid)

        # Update Week with new recipe
        old_recipe.title = new_recipe.title
        old_recipe.rid = new_recipe.rid
        old_recipe.url = new_recipe.url
        old_recipe.ingredients = new_recipe.ingredients
        old_recipe.instructions = new_recipe.instructions

        session.add(old_recipe)
        session.commit()

        return redirect(url_for('index'))

    else:

        # Get all recipes in current week table
        week_recipes_ = session.query(Week).all()
            
        week_recipes = []

        # No recipes in current week, so add three random ones
        if week_recipes_ == []:

            num = session.query(Recipe).count()
            rand_ids = [random.randint(1, num) for i in range(3)]

            for r_id in rand_ids:

                recipe_ = session.query(Recipe).get(r_id)

                recipe = {}
                recipe['title'] = recipe_.title
                recipe['url'] = recipe_.url
                recipe['ingredients'] = ast.literal_eval(recipe_.ingredients)
                recipe['instructions'] = ast.literal_eval(recipe_.instructions)

                week_recipes.append(recipe)

                # Add to weekly recipe table
                w_r = Week(
                    title=recipe_.title,
                    ingredients=recipe_.ingredients,
                    instructions=recipe_.instructions,
                    week_num=week_num,
                    url=recipe_.url)

                session.add(w_r)
                session.commit()

        else:
            for recipe_ in week_recipes_:
                recipe = {}
                recipe['title'] = recipe_.title
                recipe['url'] = recipe_.url
                recipe['ingredients'] = ast.literal_eval(recipe_.ingredients)
                recipe['instructions'] = ast.literal_eval(recipe_.instructions)
                week_recipes.append(recipe)


    return render_template('index.html', app_data=app_data, recipes=week_recipes)


@app.route('/add', methods=['GET','POST'])
def add():

    if request.method == 'POST':

        rf = request.form

        new_recipe = Recipe(
            title=['title'],
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
