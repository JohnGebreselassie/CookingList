from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship #declarative_base replaces metadata from Core, and sessionmaker cause ORM uses sessions, not connections

#orm maps python classes to database
engine = create_engine('postgresql+psycopg2://postgres:4641@localhost:5432/cookingAPI', echo = True) #postgres version
    #can read more about this in sqlAlchemyCore

Base = declarative_base()

class User (Base):
    __tablename__ = "user",
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False) #MUST HASH LATER
    
    recipes = relationship('Recipe', back_populates='creator')

class Recipe (Base):
    __tablename__ = "recipe",
    recipe_id = Column(Integer, primary_key=True)
    recipe_name = Column(String, nullable = False)
    recipe_instructions = Column(String, nullable = False)
    recipe_time = Column(Integer, nullable = False)
    owner_id = Column(Integer, ForeignKey('user.user_id'))
    
    creator = relationship('User', back_populates='recipes')