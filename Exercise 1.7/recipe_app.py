from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.expression import or_

USERNAME = "cf-python"
PASSWORD = "password"
HOST = "localhost"
DATABASE = "task_database"

engine = create_engine(f"mysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})>"
    
    def __str__(self):
        ingredients_list = self.ingredients.split(", ")
        formatted_ingredients = "\n ".join(f"  - {ingredient.title()}" for ingredient in ingredients_list)

        return (f"Recipe ID: {self.id}\n"
                f"  Name: {self.name.title()}\n"
                f"  Ingredients:\n {formatted_ingredients}\n"
                f"  Cooking Time: {self.cooking_time} minutes\n"
                f"  Difficulty: {self.difficulty}\n")
    
    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")

Base.metadata.create_all(engine)


def create_recipe():
    print()
    print("==================================================")
    print("           *** Create New Recipes ***             ")
    print("==================================================")
    print("Please follow the steps below to add new recipes!\n")
    
    while True:
        try:
            number_of_recipes = int(input("How many recipes would you like to enter? "))
            if number_of_recipes < 1:
                print("Please enter a positive number.\n")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.\n")
    
    for i in range(number_of_recipes):
        print(f"\nEnter recipe #{i + 1}")
        print("---------------------")

        while True:
            name = input("  Enter the recipe name: ").strip()
            if 0 < len(name) <= 50:
                break
            else:
                print("Please enter a valid recipe name (1-50 characters).\n")

        while True:
            try:
                cooking_time = int(input("  Enter the cooking time in minutes: "))
                if cooking_time > 0:
                    break
                else:
                    print("Please enter a positive number for cooking time.\n")
            except ValueError:
                print("Invalid input. Please enter a positive number for cooking time.\n")

        while True:
                ingredients_input = input("  Enter the recipe's ingredients, separated by a comma: ").strip()
                if ingredients_input:
                    break
                else:
                    print("Please enter at least one ingredient.\n")

        new_recipe = Recipe(name=name, ingredients=ingredients_input, cooking_time=cooking_time)
        new_recipe.calculate_difficulty()

        session.add(new_recipe)
        try:
            session.commit()
            print("  ** Recipe successfully added! **")

        except Exception as err:
            session.rollback()
            print("Error occurred: ", err)

    final_message = "Recipe successfully added!" if number_of_recipes == 1 else "All recipes successfully added!"
    print()
    print("--------------------------------------------------")
    print(f"            {final_message}            ")
    print("--------------------------------------------------\n")
    
    pause()


def view_all_recipes():
    recipes = session.query(Recipe).all()

    if not recipes:
        print("***************************************************************")
        print("         There are no recipes in the database to view.         ")
        print("                 Please create a new recipe!                   ")
        print("***************************************************************\n")
        pause()
        return None

    print("=================================================================")
    print("                  *** View All Recipes ***                   ")
    print("=================================================================")

    recipe_count = len(recipes)
    recipe_word = "recipe" if recipe_count == 1 else "recipes"
    print(f"Displaying {recipe_count} {recipe_word}\n")

    for i, recipe in enumerate(recipes, start=1):
        print(f"Recipe #{i}\n----------")
        print(format_recipe_for_search(recipe))
        print()
    
    print("\n--------------------------------------------------")
    print("             List Display Successful!              ")
    print("--------------------------------------------------\n")
    
    pause()


def search_recipe():
    results = session.query(Recipe.ingredients).all()

    if not results:
        print("***************************************************************")
        print("       There are no recipes in the database to search.         ")
        print("                 Please create a new recipe!                   ")
        print("***************************************************************\n")
        pause()
        return

    all_ingredients = set()
    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())

    print()
    print("=================================================================")
    print("           *** Search for a Recipe By Ingredient ***             ")
    print("=================================================================")
    print("Please enter a number to see all recipes that use that ingredient\n")

    sorted_ingredients = sorted(all_ingredients)
    for i, ingredient in enumerate(sorted_ingredients):
        print(f"{i+1}.) {ingredient.title()}")

    print()
    while True:
        try:
            choices = input("Enter ingredient numbers (separate multiple numbers with spaces): ").split()
            selected_indices = [int(choice) for choice in choices]
            if all(1 <= choice <= len(all_ingredients) for choice in selected_indices):
                break
            else:
                print("Please enter numbers within the list range.\n")
        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")

    search_ingredients = [sorted_ingredients[index - 1] for index in selected_indices]

    search_conditions = [Recipe.ingredients.ilike(f"%{ingredient}%") for ingredient in search_ingredients]
    search_results = session.query(Recipe).filter(or_(*search_conditions)).all()

    if len(search_ingredients) > 1:
        selected_ingredients_str = ", ".join(ingredient.title() for ingredient in search_ingredients[:-1])
        selected_ingredients_str += ", or " + search_ingredients[-1].title()
    else:
        selected_ingredients_str = search_ingredients[0].title()

    if search_results:
        recipe_count = len(search_results)
        recipe_word = "recipe" if recipe_count == 1 else "recipes"
        print(f"\n{recipe_count} {recipe_word} found containing '{selected_ingredients_str}'\n")
        
        for i, recipe in enumerate(search_results, start=1):
            print(f"Recipe #{i}\n----------")
            print(format_recipe_for_search(recipe))
            print()

        print()
        print("--------------------------------------------------")
        print("            Recipe search successful!             ")
        print("--------------------------------------------------\n")
    else:
        print(f"No recipes found containing '{selected_ingredients_str}'\n")

    pause()


def update_recipe():
    recipes = session.query(Recipe).all()

    if not recipes:
        print("***************************************************************")
        print("       There are no recipes in the database to update.         ")
        print("                Please create a new recipe!                    ")
        print("***************************************************************\n")
        pause()
        return
    
    print()
    print("=================================================================")
    print("             *** Update a Recipe By ID Number ***                ")
    print("=================================================================")
    print("Please enter an ID number to update that recipe\n")

    print("---- Avaiable Recipes ----\n")
    for recipe in recipes:
        print(format_recipe_for_update(recipe))
    print()

    while True:
        try:
            recipe_id = int(input("Enter the ID of the recipe to update: "))
            recipe_to_update = session.get(Recipe, recipe_id)
            if recipe_to_update:
                break
            else:
                print("No recipe found with the entered ID. Please try again.\n")
        except ValueError:
            print("Invalid input. Please enter a numeric value.\n")

    print(f"\nWhich field would you like to update for '{recipe_to_update.name}'?")
    print(" - Name")
    print(" - Cooking Time")
    print(" - Ingredients\n")

    field_updated = False
    while not field_updated:
        update_field = input("Enter your choice: ").lower()

        if update_field == "name":
            while True:
                new_value = input("\nEnter the new name (1-50 characters): ").strip()
                if 0 < len(new_value) <= 50:
                    recipe_to_update.name = new_value
                    field_updated = True
                    break
                else:
                    print("Invalid name. Please enter 1-50 characters.\n")
            break

        elif update_field == "cooking time":
            while True:
                try:
                    new_value = int(input("\nEnter the new cooking time (in minutes): "))
                    if new_value > 0:
                        recipe_to_update.cooking_time = new_value
                        recipe_to_update.calculate_difficulty()
                        field_updated = True
                        break
                    else:
                        print("Please enter a positive number for cooking time.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value for cooking time.")
            break
                    
        elif update_field == "ingredients":
            while True:
                new_value = input("\nEnter the new ingredients, separated by a comma: ").strip()
                if new_value:
                    recipe_to_update.ingredients = new_value
                    recipe_to_update.calculate_difficulty()
                    field_updated = True
                    break
                else:
                    print("Please enter at least one ingredient.") 
            break
        else:
            print("Invalid choice. Please choose 'name', 'cooking time', or 'ingredients'.")

    try:
        session.commit()
        print("\n--------------------------------------------------")
        print("           Recipe successfully updated!           ")
        print("--------------------------------------------------\n")
    except Exception as err:
        session.rollback()
        print(f"An error occurred: {err}")

    pause()


def delete_recipe():
    recipes = session.query(Recipe).all()

    if not recipes:
        print("***************************************************************")
        print("        There are no recipes in the database to delete.        ")
        print("                  Please create a new recipe!                  ")
        print("***************************************************************\n")
        pause()
        return
    
    print()
    print("=================================================================")
    print("             *** Delete a Recipe By ID Number ***                ")
    print("=================================================================")
    print("Please enter the ID number of the recipe to remove")
    print("** Note: This can NOT be undone **\n")

    print("---- Avaiable Recipes ----\n")
    for recipe in recipes:
        print(format_recipe_for_update(recipe))

    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe to delete: "))
            recipe_to_delete = session.get(Recipe, recipe_id)

            if recipe_to_delete:
                confirm = input(f"\nAre you sure you want to delete '{recipe_to_delete.name}'? (Yes/No): ").lower()
                if confirm == "yes":
                    break
                elif confirm == "no":
                    print("Deletion cancelled.\n")
                    pause()
                    return
                else:
                    print("Please answer with 'Yes' or 'No'.")
            else:
                print("No recipe found with the entered ID. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    try:
        session.delete(recipe_to_delete)
        session.commit()
        print()
        print("--------------------------------------------------")
        print("           Recipe successfully deleted!           ")
        print("--------------------------------------------------\n")
    except Exception as err:
        session.rollback()
        print(f"An error occured: {err}")

    pause()


def main_menu():
    choice = ""
    
    while choice != "quit":
        
        print("  _____           _                                   ")
        print(" |  __ \         (_)                /\                ")
        print(" | |__) |___  ___ _ _ __   ___     /  \   _ __  _ __  ")
        print(" |  _  // _ \/ __| | '_ \ / _ \   / /\ \ | '_ \| '_ \ ")
        print(" | | \ \  __/ (__| | |_) |  __/  / ____ \| |_) | |_) |")
        print(" |_|  \_\___|\___|_| .__/ \___| /_/    \_\ .__/| .__/ ")
        print("                   | |                   | |   | |    ")
        print("                   |_|                   |_|   |_|    ")
        print("======================================================")
        print("   What would you like to do? Pick a choice below!    ")
        print("======================================================\n")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Update an existing recipe")
        print("5. Delete a recipe\n")
        print("Type 'quit' to exit the program\n")
        
        choice = input("Your choice: ").strip().lower()

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_recipe()
        elif choice == "4":
            update_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            print("=============================================")
            print("      Thanks for using the Recipe App!       ")
            print("             See you next time               ")
            print("=============================================")
            break 
        else:
            print("---------------------------------------------------")
            print("Invalid choice! Please enter 1, 2, 3, 4, 5, or 'quit'.")
            print("---------------------------------------------------\n")
            
            pause()

    session.close()
    engine.dispose()


def format_recipe_for_search(recipe):
    formatted_ingredients = "\n  ".join(f"- {ingredient.title()}" for ingredient in recipe.ingredients.split(", "))
    
    return (f"Recipe Name: {recipe.name.title()}\n"
            f"  Cooking Time: {recipe.cooking_time} mins\n"
            f"  Ingredients:\n  {formatted_ingredients}\n"
            f"  Difficulty: {recipe.difficulty}")


def format_recipe_for_update(recipe):
    capitalized_ingredients = [ingredient.title() for ingredient in recipe.ingredients.split(", ")]
    
    capitalized_ingredients_str = ", ".join(capitalized_ingredients)
    
    return (f"ID: {recipe.id} | Name: {recipe.name}\n"
            f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {recipe.cooking_time} | Difficulty: {recipe.difficulty}\n")


def pause():
    print("Press ENTER to return to the main menu...", end="")
    input()
    
    print("\n\n\n\n")


if __name__ == "__main__":
    main_menu()
    