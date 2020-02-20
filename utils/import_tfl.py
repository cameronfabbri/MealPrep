import os
from epub_conversion.utils import open_book, convert_epub_to_lines
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from BingImages import BingImages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Recipes, Week
from tqdm import tqdm
import ast

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        return tag

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        return tag

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        self.data = data


def main():

    engine = create_engine('sqlite:///recipes.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    book = open_book('data/books/TheFoodLab.epub')
    lines = convert_epub_to_lines(book)
    with open('f.txt', 'w') as f:
        for l in lines:
            f.write(l+'\n')

    parser = MyHTMLParser()

    in_recipe = False
    got_ing = False
    got_inst = False
    recipe_count = 0

    recipe_dict = {}

    week_count = 0

    lc = 0
    for line in tqdm(lines):

        if 'recipe_rt' in line:
            in_recipe = True
            parser.feed(line)
            recipe_title = parser.data.title()
            ingredients = []
            instructions = []

            try: url = BingImages(recipe_title, count=1).get()[0]
            except: url = None

        if in_recipe:

            if 'recipe_i' in line:
                parser.feed(line)
                ingredient = parser.data.title()
                ingredients.append(ingredient)
                got_ing = True

            elif 'recipe_rsteps' in line:
                parser.feed(line)
                instruction = parser.data.title()
                instructions.append(instruction)
                got_inst = True

        if lc > 0:
            prev = lines[lc-1]

        if got_inst and got_ing and 'recipe_rsteps' in prev:
            recipe_count+=1
            got_inst = False
            got_ing = False
            in_recipe = False

            recipe = Recipes(
                title=recipe_title,
                ingredients=str(ingredients),
                instructions=str(instructions),
                url=url)

            session.add(recipe)

            if week_count < 3:
                week_recipe = Week(id=recipe.id, slot_num=week_count+1)
                session.add(week_recipe)
                session.commit()
                week_count += 1

        lc += 1

    session.commit()

if __name__ == '__main__':
    main()
