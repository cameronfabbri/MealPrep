"""

Database tables setup.

Recipes table is the

"""
# Copyright (c) 2019.
# Cameron Fabbri

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Recipes(Base):
    """ Table for all recipes """

    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    ingredients = Column(String(256), nullable=False)
    instructions = Column(String(256), nullable=False)
    rating = Column(Integer, nullable=True)
    date_made = Column(Date, nullable=True)
    url = Column(String(512), nullable=True)
    source = Column(String(256), nullable=True)


class Week(Base):
    """ Table for recipe ids for the current week """

    __tablename__ = 'week'

    id = Column(Integer, primary_key=True)
    slot_num = Column(Integer, primary_key=False)


class MyRecipes(Base):
    """ Table for my recipe ids """

    __tablename__ = 'my_recipes'

    id = Column(Integer, primary_key=True)


class Favorites(Base):
    """ Table for recipes for the current week """

    __tablename__ = 'favorite'

    id = Column(Integer, primary_key=True)


class Pantry(Base):
    """ Table for my pantry inventory """

    __tablename__ = 'pantry'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    amount = Column(String(256), nullable=False)
    buy_date = Column(Date, nullable=False)
    expire_date = Column(Date, nullable=False)


connect_args = {'check_same_thread':False}
engine = create_engine('sqlite:///recipes.db', connect_args=connect_args)


# Create classes above in database
Base.metadata.create_all(engine)

