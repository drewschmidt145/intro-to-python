import pickle

# def display_recipe(recipe):
#   print("")
#   print("Recipe: ", recipe["name"])
#   print("Cooking Time (mins): ", recipe["cooking_time"])
#   print("Ingredients: ")
#   for ele in recipe["ingredients"]:
#       print("- ", ele)
#   print("Difficulty: ", recipe["difficulty"])
#   print("")

# def search_ingredients(data):
#     available_ingredients = enumerate(data["all_ingredients"])
#     numbered_list = list(available_ingredients)
#     print("Ingredients List: ")

#     for ele in numbered_list:
#         print(ele[0], ele[1])
#     try:
#         num = int(input("Enter the number for ingredents you would like to search: "))
#         ingredient_searched = numbered_list[num][1]
#         print("Searching for recipes with", ingredient_searched, "...")
#     except ValueError:
#         print("Only numbers are allowed")
#     except:
#         print(
#             "Oops! Your input doesn't match any ingredients. Make sure you enter a number that matches the ingredients list."
#         )
#     else:
#         for ele in data["recipe_list"]:
#             if ingredient_searched in ele["ingredients"]:
#                 print(ele)

def search_ingredients(data):
    available_ingredients = enumerate(data["all_ingredients"])
    numbered_list = list(available_ingredients)
    print("Ingredients List: ")

    for ele in numbered_list:
        print(ele[0], ele[1])
    try:
        num = int(input("Enter the number for ingredients you would like to search: "))
        ingredient_searched = numbered_list[num][1]
        print("Searching for recipes with", ingredient_searched, "...")
    except ValueError:
        print("Only numbers are allowed")
    except:
        print(
            "Oops! Your input doesn't match any ingredients. Make sure you enter a number that matches the ingredients list."
        )
    else:
        matching_recipes = []
        for ele in data["recipe_list"]:
            if ingredient_searched in ele["ingredients"]:
                matching_recipes.append(ele)

        if len(matching_recipes) > 0:
            print("Recipes with", ingredient_searched, ":")
            for recipe in matching_recipes:
                print_recipe(recipe)
        else:
            print("No recipes found with", ingredient_searched)


def print_recipe(recipe):
    print("")
    print("Recipe: ", recipe["name"])
    print("Cooking Time (mins): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ele in recipe["ingredients"]:
        print("- ", ele)
    print("Difficulty: ", recipe["difficulty"])
    print("")



filename = input("Enter the filename of your Recipes: ")

try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File loaded successfully!")
except FileNotFoundError:
    print("No files match that name - please try again")
except:
    print("Oops, there was an unexpected error")
else:
    file.close()
    search_ingredients(data)