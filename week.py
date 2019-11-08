"""

Randomly selects 3 meals from the dataset

"""

import random
import json
import os

if __name__ == '__main__':


    recipes_file = os.path.join('data','full_format_recipes.json')

    with open(recipes_file, 'r') as json_file:
        recipes = json.load(json_file)

    meals = []
    desserts = []
    for recipe in recipes:
        if 'categories' in recipe.keys():
            categories = [x.lower() for x in recipe['categories']]
            if 'lunch' in categories or 'dinner' in categories:
                meals.append(recipe)
            if 'dessert' in categories:
                desserts.append(recipe)

    random_meal = random.choice(meals)

    print(random_meal['title'])
    print(random_meal)





