"""

Script to be run (probably) outside of Flask.
This will take the json files containing recipes
and populate our database

"""

from google_images_download import google_images_download
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Recipe
from tqdm import tqdm
import json
import ast
import os


if __name__ == '__main__':

    engine = create_engine('sqlite:///recipes.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    #recipes_file = os.path.join('data','layers','recipes_small.json')
    #images_file  = os.path.join('data','layers','images_small.json')

    recipes_file = os.path.join('data','layers','layer1.json')
    images_file  = os.path.join('data','layers','layer2.json')

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

    i = 0
    response = google_images_download.googleimagesdownload()

    #for recipe in tqdm(recipes):
    for recipe in recipes:

        # Get data
        rid          = str(recipe['id'])
        title        = str(recipe['title'])
        ingredients  = str(recipe['ingredients'])
        instructions = str(recipe['instructions'])

        ingredients = ast.literal_eval(ingredients)
        ingredients = str([x['text'] for x in ingredients])

        instructions = ast.literal_eval(instructions)
        instructions = str([x['text'] for x in instructions])

        # Strip out ' and " from title
        title = title.replace(',','').replace('.','').replace("'","").replace('"','').rstrip().strip()
        title = ' '.join(title.split())

        if recipe_url_dict.get(rid) is None:
            arguments = {'keywords':title,'limit':1,'print_urls':True,'no_download':True, 'silent_mode':True}
            image_url_ = response.download(arguments)[0][title]

            while image_url_ == []:
                image_url_ = response.download(arguments)[0][title]

            image_url = image_url_[0]
        else:
            image_url = recipe_url_dict.get(rid)

        recipe = Recipe(
            rid=rid,
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            url=image_url)

        session.add(recipe)
        session.commit()

        #i += 1
        #if i > 100: exit()
