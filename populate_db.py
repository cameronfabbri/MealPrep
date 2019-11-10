"""

Script to be run (probably) outside of Flask.
This will take the json files containing recipes
and populate our database

"""


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

    recipes_file = os.path.join('data','layers','small.json')
    #recipes_file = os.path.join('data','layers','layer1.json')

    with open(recipes_file, 'r') as json_file:
        recipes = json.load(json_file)

    i = 0

    for recipe in tqdm(recipes):

        # Get data
        rid          = str(recipe['id'])
        title        = str(recipe['title'])
        ingredients  = str(recipe['ingredients'])
        instructions = str(recipe['instructions'])

        ingredients = ast.literal_eval(ingredients)
        ingredients = str([x['text'] for x in ingredients])

        instructions = ast.literal_eval(instructions)
        instructions = str([x['text'] for x in instructions])

        recipe = Recipe(
            rid=rid,
            title=title,
            ingredients=ingredients,
            instructions=instructions)

        session.add(recipe)
        session.commit()

        i += 1

        if i > 1000: exit()
