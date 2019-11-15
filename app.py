from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from google_images_download import google_images_download
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from db_setup import Base, Recipe, Week, Favorite, MyRecipes

import numpy as np
import datetime
import random
import ast

import ops


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

                # If no url for the recipe, find one
                if recipe['url'] is None:
                    print('No recipe')
                    recipe['url'] = ops.get_image_url([recipe['title']])

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
                
                # If no url for the recipe, find one
                if recipe['url'] is None:
                    print('No recipe')
                    recipe['url'] = ops.get_image_url([recipe['title']])

                recipe['ingredients'] = ast.literal_eval(recipe_.ingredients)
                recipe['instructions'] = ast.literal_eval(recipe_.instructions)
                week_recipes.append(recipe)


    return render_template('index.html', app_data=app_data, recipes=week_recipes)


@app.route('/add', methods=['GET','POST'])
def add():

    if request.method == 'POST':
        response = google_images_download.googleimagesdownload()

        rf = request.form

        title = rf['title']
        ingredients = str([x.rstrip() for x in rf['ingredients'].split('\n')])
        instructions = str([x.rstrip() for x in rf['instructions'].split('\n')])

        arguments = {'keywords':title,'limit':1,'print_urls':True,'no_download':True, 'silent_mode':True}
        image_url_ = response.download(arguments)[0][title]
        while image_url_ == []:
            image_url_ = response.download(arguments)[0][title]
        image_url = image_url_[0]

        recipe = MyRecipes(
            title=title,
            start_date=d,
            ingredients=ingredients,
            instructions=instructions,
            url=image_url)

        session.add(recipe)
        session.commit()

        return redirect(url_for('index'))

    else:
        return render_template('add.html', app_data=app_data)


@app.route('/view')
def view():
    """ Page for viewing my recipes that I have added """

    view_recipes_ = session.query(MyRecipes).all()
    recipe_list = []

    for v in view_recipes_:

        v_ingredients = ast.literal_eval(v.ingredients)
        v_instructions = ast.literal_eval(v.instructions)

        ingredients = []
        instructions = []
        for ingredient in v_ingredients:
            ingredients.append(ingredient)
        for instruction in v_instructions:
            instructions.append(instruction)

        view_recipes = {}
        view_recipes['title'] = v.title
        view_recipes['ingredients'] = ingredients
        view_recipes['instructions'] = instructions
        view_recipes['url'] = v.url

        recipe_list.append(view_recipes)

    return render_template('view.html', app_data=app_data, recipe_list=recipe_list)


@app.route('/favorite')
def favorite():
    """ Page for viewing my favorite recipes """
    return render_template('favorite.html', app_data=app_data)


# ------- DEVELOPMENT CONFIG -------
if __name__ == '__main__':
    app.run(debug=True)
