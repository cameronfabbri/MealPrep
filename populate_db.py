"""

Script to populate the recipes database
This will take the json files containing recipes and populate our database

"""
# Copyright (c) 2019.
# Cameron Fabbri

from google_images_download import google_images_download
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Recipes, Week
from tqdm import tqdm
import json
import ast
import os


if __name__ == '__main__':

    engine = create_engine('sqlite:///recipes.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    recipes_file = os.path.join('data','layers','recipes_small.json')
    images_file  = os.path.join('data','layers','images_small.json')

    #recipes_file = os.path.join('data','layers','layer1.json')
    #images_file  = os.path.join('data','layers','layer2.json')

    with open(recipes_file, 'r') as json_file:
        recipes = json.load(json_file)

    with open(images_file, 'r') as json_file:
        images = json.load(json_file)

    recipe_url_dict = {}

    for line in images:
        recipe_id = line['id']
        images = line['images']

        urls = [x['url'] for x in images]
        filenames = [x['id'] for x in images]

        recipe_url_dict[str(recipe_id)] = urls[0]

    i = 1

    week_count = 0
    for recipe in tqdm(recipes):

        # Get data
        title        = str(recipe['title'])
        ingredients  = str(recipe['ingredients'])
        instructions = str(recipe['instructions'])

        ingredients = ast.literal_eval(ingredients)
        ingredients = str([x['text'] for x in ingredients])

        instructions = ast.literal_eval(instructions)
        instructions = str([x['text'] for x in instructions])

        # Strip out ' and " from title
        new_title = title.replace(',','').replace('.','').replace("'","").replace('"','').rstrip().strip()
        new_title = ' '.join(new_title.split())

        recipe = Recipes(
            title=new_title,
            ingredients=ingredients,
            instructions=instructions,
            url=recipe_url_dict.get(recipe['id']))

        session.add(recipe)

        if week_count < 3:
            week_recipe = Week(id=recipe.id, slot_num=week_count+1)
            session.add(week_recipe)
            session.commit()
            week_count += 1

        if i % 2000 == 0:
            session.commit()
            break
        i += 1

    session.commit()
