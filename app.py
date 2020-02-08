"""

"""
# Copyright (c) 2019.
# Cameron Fabbri

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from google_images_download import google_images_download
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from db_setup import Base, Recipes, Week, Favorites, MyRecipes, Pantry

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

from db_setup import engine

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_recipe_by_id(recipe_id):
    return session.query(Recipes).get(recipe_id)


@app.route('/', methods=['GET','POST'])
def index():

    # Getting a new random recipe
    if request.method == 'POST':

        # Get recipe id we want to swap out
        old_id = int(request.form['recipe_id'].split('/')[0])

        # Old recipe object
        old_recipe = session.query(Week).get(old_id)

        # Get new random recipe from Recipes table
        new_recipe = random.choice(session.query(Recipes).all())

        # Update Week with new recipe
        old_recipe.id = new_recipe.id

        session.add(old_recipe)
        session.commit()

        return redirect(url_for('index'))

    else:

        # Get all recipes in current week table
        # This will just return 3 ids which we go to the main table for
        week_rows = session.query(Week).all()

        # Slot numbers so they aren't re-ordered by db id
        slots = [x.slot_num for x in week_rows]

        week_recipes = [None, None, None]

        # Loop through the week rows, find the 3 recipes, and return them
        for row in week_rows:

            # Get recipe details from main table based on id
            recipe_obj = get_recipe_by_id(row.id)

            recipe = {}
            recipe['title'] = recipe_obj.title
            recipe['url'] = recipe_obj.url
            recipe['id'] = recipe_obj.id
            recipe['rating'] = recipe_obj.rating
            recipe['slot_num'] = row.slot_num

            # If no image url for the recipe, find one
            if recipe['url'] is None:
                recipe['url'] = ops.get_image_url([recipe['title']])
                recipe_obj.url = recipe['url']
                session.commit()

            recipe['ingredients'] = ast.literal_eval(recipe_obj.ingredients)
            recipe['instructions'] = ast.literal_eval(recipe_obj.instructions)
            week_recipes[row.slot_num-1] = recipe

    return render_template('index.html', app_data=app_data, recipes=week_recipes)


@app.route('/ingredients', methods=['GET','POST'])
def ingredients():
    """ Shows the ingredients for the current meals of the week """

    week_rows = session.query(Week).all()

    week_ingredients = []

    for row in week_rows:
        recipe_obj = get_recipe_by_id(row.id)
        ingredients = ast.literal_eval(recipe_obj.ingredients)
        for ing in ingredients:
            week_ingredients.append(ing)

    return render_template('ingredients.html', ingredients=week_ingredients, app_data=app_data)


@app.route('/add', methods=['GET','POST'])
def add():

    if request.method == 'POST':
        response = google_images_download.googleimagesdownload()

        rf = request.form

        title = rf['title']
        source = rf['source']
        ingredients = str([x.rstrip() for x in rf['ingredients'].split('\n')])
        instructions = str([x.rstrip() for x in rf['instructions'].split('\n')])

        arguments = {'keywords':title,'limit':1,'print_urls':True,'no_download':True, 'silent_mode':True}
        image_url_ = response.download(arguments)[0][title]
        while image_url_ == []:
            image_url_ = response.download(arguments)[0][title]
        image_url = image_url_[0]

        recipe = Recipes(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            url=image_url,
            source=source)

        session.add(recipe)
        session.flush()
        session.commit()

        # Looks like the id is right but it didn't add to MyRecipes
        my_recipe = MyRecipes(id=recipe.id)
        session.commit()

        return redirect(url_for('index'))

    else:
        return render_template('add.html', app_data=app_data)

@app.route('/pantry', methods=['GET','POST'])
def pantry():
    """ Inventory of my pantry """

    if request.method == 'POST':

        rf = request.form

        name = rf['name']
        amount = rf['amount']
        buy_date = rf['buy_date']
        expire_date = rf['expire_date']

        buy_date = datetime.datetime.strptime(buy_date, '%Y-%m-%d')
        expire_date = datetime.datetime.strptime(expire_date, '%Y-%m-%d')

        pantry_entry = Pantry(
                name=name,
                amount=amount,
                buy_date=buy_date,
                expire_date=expire_date)

        session.add(pantry_entry)
        session.commit()

    pantry_items = session.query(Pantry).all()

    pantry_list = []
    for pitem in pantry_items:

        pantry_obj = {
                'name':pitem.name,
                'amount':pitem.amount,
                'buy_date':pitem.buy_date,
                'expire_date':pitem.expire_date
        }

        pantry_list.append(pantry_obj)

    return render_template('pantry.html', app_data=app_data, pantry_list=pantry_list)

@app.route('/my_recipes', methods=['GET','POST'])
def my_recipes():
    """ Page for viewing my recipes that I have added """

    if request.method == 'POST':

        old_recipe = session.query(Week).filter_by(id=request.form['old_id']).one()
        new_recipe = session.query(MyRecipes).filter_by(id=request.form['new_id']).one()

        # Update old recipe in the week table with our new one
        old_recipe.title = new_recipe.title
        old_recipe.rid = new_recipe.rid
        old_recipe.url = new_recipe.url
        old_recipe.ingredients = new_recipe.ingredients
        old_recipe.instructions = new_recipe.instructions

        session.add(old_recipe)
        session.commit()

        return redirect(url_for('index'))

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
        view_recipes['id'] = v.id

        recipe_list.append(view_recipes)

    return render_template('my_recipes.html', app_data=app_data, recipe_list=recipe_list)


@app.route('/delete', methods=['GET','POST'])
def delete():

    if request.method == 'POST':

        del_id = int(request.form['recipe_id'].split('/')[0])

        # TODO - change this to `if id in week_ids`
        # Delete from week if in week
        try:
            # Get recipe to delete from Week table - don't need to delete, just change id
            del_recipe_w = session.query(Week).filter_by(id=del_id).one()

            # Get new random recipe from Recipes table
            new_recipe = random.choice(session.query(Recipes).all())

            # Update Week with new recipe
            del_recipe_w.id = new_recipe.id

            session.add(del_recipe_w)
            session.commit()

            # Get recipe to delete from Recipes table
            del_recipe_r = session.query(Recipes).filter_by(id=del_id).one()

            # Delete recipe from Recipes table
            session.delete(del_recipe_r)
            session.commit()

        except:

            # Get recipe to delete from Recipes table
            del_recipe_r = session.query(Recipes).filter_by(id=del_id).one()

            # Delete recipe from Recipes table
            session.delete(del_recipe_r)
            session.commit()

    return redirect(url_for('index'))


@app.route('/search', methods=['GET','POST'])
def search():
    """ Page for searching for recipes """

    if request.method == 'POST':
        search_term = request.form['search']
        recipes = session.query(Recipes).filter(Recipes.title.contains(search_term)).all()

    else:
        recipes = []

    return render_template('search.html', app_data=app_data, recipes=recipes, num_recipes=len(recipes))


@app.route('/view')
def view():
    """ Page for viewing my favorite recipes """

    recipe_obj = session.query(Recipes).get(request.args.get('id'))

    recipe = {}
    recipe['title'] = recipe_obj.title
    recipe['url'] = recipe_obj.url
    recipe['id'] = recipe_obj.id
    recipe['rating'] = recipe_obj.rating

    # If no image url for the recipe, find one
    if recipe['url'] is None:
        recipe['url'] = ops.get_image_url([recipe['title']])
        recipe_obj.url = recipe['url']
        session.commit()

    recipe['ingredients'] = ast.literal_eval(recipe_obj.ingredients)
    recipe['instructions'] = ast.literal_eval(recipe_obj.instructions)

    return render_template('view.html', app_data=app_data, recipe=recipe)


@app.route('/favorite')
def favorite():
    """ Page for viewing my favorite recipes """
    return render_template('favorite.html', app_data=app_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
