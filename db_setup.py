import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Recipe(Base):
    """ Table for all recipes """

    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)

    # This is a string because in the json file it's a string
    rid = Column(String(256), primary_key=False)
    title = Column(String(256), nullable=False)
    ingredients = Column(String(256), nullable=False)
    instructions = Column(String(256), nullable=False)
    date_made = Column(Date, nullable=True)
    url = Column(String(512), nullable=True)


class Week(Base):
    """ Table for recipes for the current week """

    __tablename__ = 'week'

    id = Column(Integer, primary_key=True)
    rid = Column(String(256), primary_key=False)
    title = Column(String(256), nullable=False)
    ingredients = Column(String(256), nullable=False)
    instructions = Column(String(256), nullable=False)
    week_num = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=True)
    url = Column(String(512), nullable=True)


class MyRecipes(Base):
    """ Table for recipes for the current week """

    __tablename__ = 'my_recipes'

    id = Column(Integer, primary_key=True)
    rid = Column(Integer, primary_key=False)
    title = Column(String(256), nullable=False)
    ingredients = Column(String(256), nullable=False)
    instructions = Column(String(256), nullable=False)
    start_date = Column(Date, nullable=True)
    rating = Column(Integer, nullable=True)
    url = Column(String(512), nullable=True)


class Favorite(Base):
    """ Table for recipes for the current week """

    __tablename__ = 'favorite'

    id = Column(Integer, primary_key=True)
    rid = Column(String(256), primary_key=False)
    title = Column(String(256), nullable=False)
    ingredients = Column(String(256), nullable=False)
    instructions = Column(String(256), nullable=False)
    start_date = Column(Date, nullable=False)
    rating = Column(Integer, nullable=True)
    url = Column(String(512), nullable=True)


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

