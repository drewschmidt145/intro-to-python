from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import select

engine = create_engine("mysql://cf-python:password@localhost/my_database")

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "Recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe id: {self.id} - {self.name}>"
    
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"
    
def insert_recipe (name, ingredients, cooking_time):
    difficulty = calculate_difficulty(cooking_time, ingredients)

    ingredients_string = ", ".join(ingredients)

    new_recipe = Recipe(name=name, ingredients=ingredients_string, cooking_time=cooking_time, difficulty=difficulty)

    session.add(new_recipe)

    session.commit()
    print("Recipe added succcessfully")

def create_recipe():
    print()
    print("==================================================")
    print("           *** Create New Recipes ***             ")
    print("==================================================")
    print("Please follow below to add new recipes!\n")

    name=input("Enter the name for the recipe: ")
    cooking_time=int(input("Enter the time it take to make in minutes: "))
    ingredients=input("Enter the list of ingredients: ").split(", ")

    insert_recipe(name, ingredients, cooking_time)

def search_recipe():
    all_ingredients = session.query(func.distinct(Recipe.ingredients)).all()

    all_ingredients = [ingredient[0] for ingredient in all_ingredients]

    print("Available ingredients:")
    ingredient_dict = {}
    count = 1
    for ingredients_str in all_ingredients:
        ingredients_list = ingredients_str.split(", ")
        for ingredient in ingredients_list:
            print(f"{count}. {ingredient}")
            ingredient_dict[count] = ingredient
            count += 1

    ingredient_index = int(input("Enter the number corresponding to the ingredient you want to search for: "))
    search_ingredient = ingredient_dict.get(ingredient_index)

    search_results = session.query(Recipe).filter(Recipe.ingredients.like(f"%{search_ingredient}%")).all()

    print("\nSearch Results:")
    if search_results:
        for result in search_results:
            print("Name:", result.name)
            print("Ingredients:", result.ingredients)
            print("Cooking Time:", result.cooking_time, "minutes")
            print("Difficulty:", result.difficulty)
            print()
    else:
        print("No recipes found containing", search_ingredient)


def update_recipe():
    recipes = session.query(Recipe).all()
    print("Available Recipes:")
    for index, recipe in enumerate(recipes, start=1):
        print(f"{index}. {recipe.name}")

    recipe_index = int(input("Enter the index of the recipe you want to update: ")) - 1

    if 0 <= recipe_index < len(recipes):
        recipe = recipes[recipe_index]

        print("Columns available for update: name, cooking_time, ingredients")
        column = input("Enter the column to be updated: ")

        new_value = input("Enter the new value: ")

        if column == 'cooking_time':
            new_value = int(new_value)

        setattr(recipe, column, new_value)

        if column == 'cooking_time' or column == 'ingredients':
            recipe.difficulty = calculate_difficulty(recipe.cooking_time, recipe.ingredients.split(", "))

        session.commit()
        print("Recipe updated successfully!")
    else:
        print("Error: Recipe not found.")

def delete_recipe():
    recipes = session.query(Recipe).all()
    print("Available Recipes:")
    for index, recipe in enumerate(recipes, start=1):
        print(f"{index}. {recipe.name}")

    recipe_index = int(input("Enter the index of the recipe you want to delete: ")) - 1

    if 0 <= recipe_index < len(recipes):
        recipe = recipes[recipe_index]

        session.delete(recipe)

        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Error: Invalid recipe index.")


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_recipe()
        elif choice == '2':
            search_recipe()
        elif choice == '3':
            update_recipe()
        elif choice == '4':
            delete_recipe()
        elif choice == '5':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()
    print("Session closed.")

main_menu()