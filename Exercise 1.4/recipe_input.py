import pickle

# def take_recipe ():
#   name = str(input('Enter the Recipe Name: '))
#   cooking_time = int(input('Enter the time it take to cook (minutes): '))
#   ingredients = [
#         ingredient.strip().capitalize()
#         for ingredient in input("Enter the ingredients separated by a comma: ").split(
#             ","
#         )
#     ]
#   difficulty = get_difficulty(cooking_time, ingredients)
#   recipe = {
#     'recipe_name': name,
#     'cooking_time': cooking_time,
#     'ingredients': ingredients,
#     'difficulty': difficulty,
#   }
#   return recipe
def take_recipe(recipe_num):
    print(f"\n---- Recipe #{recipe_num} ----")

    # Validate recipe name
    while True:
        name = input("Enter your recipe name: ").strip()
        if name:
            break
        print("\nPlease enter a valid recipe name.")

    # Validate cooking time
    while True:
        try:
            cooking_time = int(input("Enter the cooking time (in minutes): "))
            if cooking_time > 0:
                break
            print("\nPlease enter a positive number for the cooking time.")
        except ValueError:
            print("\nInvalid input! Please enter a number.")

    # Validate ingredients
    while True:
        ingredients_input = input("Enter your ingredients, seperated by a comma: ").strip()
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",") if ingredient.strip()]
        if ingredients:
            break
        print("\nPlease enter at least one ingredient.")
    
    difficulty = get_difficulty(cooking_time, len(ingredients))
    return {"name": name, "cooking_time": cooking_time, "ingredients": ingredients, "difficulty": difficulty}

def get_difficulty(cooking_time, num_ingredients):
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"
  
filename = input("Input a name for the file you want to save in: ")

try:
  file = open(filename, 'rb')
  data = pickle.load(file)
  print("File Loaded Successfully!")

except FileNotFoundError:
  print("File not found - Creating new file.")
  data = {"recipe_list": [], "all_ingredients": []}

except:
  print("Unexpected Error occured, Try again.")
  data = {"recipe_list": [], "all_ingredients": []}

else: 
  file.close()

finally:
    recipe_list = data["recipe_list"]
    all_ingredients = data["all_ingredients"]

n = int(input("\nHow many recipes would you like to enter?: "))
for i in range(1, n+1):
    recipe = take_recipe(i)
    recipe_list.append(recipe)
    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

data = {"recipe_list": recipe_list, "all_ingredients": all_ingredients}

updated_file = open(filename, "wb")
pickle.dump(data, updated_file)
updated_file.close()
print("Recipe file has been updated!")

