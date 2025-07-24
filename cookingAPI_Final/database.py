from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship #declarative_base replaces metadata from Core, and sessionmaker cause ORM uses sessions, not connections

#orm maps python classes to database
engine = create_engine('postgresql+psycopg2://postgres:4641@localhost:5432/cookingAPI', echo = True) #postgres version
    #can read more about this in sqlAlchemyCore

Base = declarative_base()

#primary tables
class User (Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False) #MUST HASH LATER
    
    recipes = relationship('Recipe', back_populates='creator')
    shopping_lists = relationship('ShoppingList', back_populates='creator')
    

class Recipe (Base):
    __tablename__ = "recipe"
    recipe_id = Column(Integer, primary_key=True)
    recipe_name = Column(String, nullable = False)
    recipe_instructions = Column(String, nullable = False)
    recipe_time = Column(Integer, nullable = False)
    owner_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    
    creator = relationship('User', back_populates='recipes')
    ingredients = relationship('Ingredient', secondary='recipe_ingredient', back_populates='recipes')

class Ingredient (Base):
    __tablename__ = "ingredient"
    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, nullable = False)
    
    recipes = relationship('Recipe', secondary='recipe_ingredient', back_populates='ingredients')

class ShoppingList (Base):
    __tablename__ = "shopping_list"
    shopping_id = Column(Integer, primary_key=True)
    shopping_name = Column(String, nullable = False)
    owner_id = Column(Integer, ForeignKey('user.user_id'))
    
    creator = relationship('User', back_populates='shopping_lists')

#association tables
class RecipeIngredient (Base):
    __tablename__ = "recipe_ingredient"
    recipe_ingredient_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipe.recipe_id'))
    ingredient_id = Column(Integer, ForeignKey('ingredient.ingredient_id'))
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    
class ShoppingListIngredient (Base):
    __tablename__ = "shopping_list_ingredient"
    shopping_list_ingredient_id = Column(Integer, primary_key=True)
    shopping_list_id = Column(Integer, ForeignKey('shopping_list.shopping_id'))
    ingredient_id = Column(Integer, ForeignKey('ingredient.ingredient_id'))
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    is_checked = Column(Boolean, default=False)