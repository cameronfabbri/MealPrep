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
    title = Column(String(256), nullable=False)
    ingredients = Column(String(256), nullable=False)
    instructions = Column(String(256), nullable=False)
    date_made = Column(Date, nullable=True)

class Week(Base):
    """ Table for recipes for the current week """

    __tablename__ = 'week'

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    ingredients = Column(String(256), nullable=False)
    instructions = Column(String(256), nullable=False)
    start_date = Column(Date, nullable=False)
    rating = Column(Integer, nullable=True)


engine = create_engine('sqlite:///recipes.db')


# Create classes above in database
Base.metadata.create_all(engine)
