import mysql.connector

conn = mysql.connector(
    host = "localhost",
    user = "cf-python",
    passwrd = "password"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
    choice = ""
    while (choice != 'quit'):
        print("--------------------")
        print("     Main Menu      ")
        print("--------------------")
        print("1. Create a new Recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update a Recipe")
        print("4. Delete a Recipe")
        print("5. View all Recipes")
        print("type 'quit' to exit")
        choice = input("What do you choose? : ").strip().lower()
        print()

    if choice == '1':
        create_recipe(conn, cursor)
    elif choice == '2':
        search_recipe(conn, cursor)
    elif choice == '3':
        update_recipe(conn, cursor)
    elif choice == '4':
        delete_recipe(conn, cursor)
    elif choice == '5':
        view_recipes(conn, cursor)

def display_recipe(recipe):
    print("\nID:", recipe[0])
    print("Name:", recipe[1])
    print("Ingredients:", recipe[2])
    print("Cooking Time (mins):", recipe[3])
    print("Difficulty:", recipe[4])
    print('')

def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if (cooking_time < 10 and num_ingredients < 4):
        return 'Easy'
    elif (cooking_time < 10 and num_ingredients >= 4):
        return 'Medium'
    elif (cooking_time >= 10 and num_ingredients < 4):
        return 'Intermediate'
    elif (cooking_time >= 10 and num_ingredients >= 4):
        return 'Hard'

def create_recipe(conn, cursor):
    name = str(input("Enter a name for the recipe: "))
    cooking_time = int(input("Enter the time it takes to cook in minutes: "))
    ingredients = [str(ingredients) for ingredients in input('\nEnter the ingredients (seperate with comma): ').split(', ')]
    ingredients_str = ', '.join(ingredients)
    difficulty = calculate_difficulty(cooking_time, ingredients)

    sql = f"INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ingredients_str, cooking_time, difficulty)

    cursor.execute(sql, val)
    conn.commit()

    print(f"Recipe for {name} has been added.")

def search_recipe(conn, cursor):
    all_ingredients = []

    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    for ingredients_list in results:
        for recipe_ingredients in ingredients_list:
            recipe_ingredients_list = recipe_ingredients.split(', ')
            all_ingredients.extend(recipe_ingredients_list)
    
    all_ingredients = list(dict.fromkeys(all_ingredients))

    all_ingredients_list = list(enumerate(all_ingredients))

    print("\nAll Ingredients: \n")
    print("---------------------")
    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0] + 1) + ". " + tup[1])

    try:
        ingredients_num = input("\nEnter the number corresponding to the ingredient you want to select: ")
        ingredient_index = int(ingredients_num) - 1
        ingredients_found = all_ingredients_list[ingredient_index][1]
        print('\nIngredient: ', ingredients_found)
    except:
        print('An unexpected error occured.')
    else:
        print("\nThe recipes below include the selected ingredient:\n")
        print("------------------------------------------------------")

        sql = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
        val = ('%' + ingredients_found + '%', )

        cursor.execute(sql, val)

        recipe_results = cursor.fetchall()

        for row in recipe_results:
            display_recipe(row)

def update_recipe(conn, cursor):
    view_recipes(conn, cursor)

    def update_difficulty(id):
        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (id, ))
        recipe_to_update = cursor.fetchall()

        name = recipe_to_update[0][1]
        ingredients = tuple(recipe_to_update[0][2].split(', '))
        cooking_time = recipe_to_update[0][3]

        updated_difficulty = calculate_difficulty(cooking_time, ingredients)
        print("Updated Difficulty: ", updated_difficulty)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id %s", (updated_difficulty, id))

    id_to_update = int((input("Enter the id of the Recipe you want to update: ")))

    column_to_update = str(input("\nEnter the section you would like to update: (name, cooking _time, ingredients): "))

    updated_value = (input(f"Enter the new value you would like for {column_to_update}"))
    print("Change: ", updated_value)

    if column_to_update == 'name':
        cursor.execute("UPDATE Recipes SET name = %s WHERE id %s", (column_to_update, id_to_update))
    elif column_to_update == 'cooking_time':
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id %s", (column_to_update, id_to_update))
        update_difficulty(id_to_update)
    elif column_to_update == 'ingredients':
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id %s", (column_to_update, id_to_update))
        update_difficulty(id_to_update)

    print("Recipe has been updated!")
    conn.commit()

def delete_recipe(conn, cursor):
    view_recipe(conn, cursor)

    id_to_delete = int((input("\nEnter the ID of the recipe you want to delete: ")))

    cursor.execute("DELETE FROM Recipes WHERE id = (%s)", (id_to_delete))

    conn.commit()
    print("\nRecipe has been deleted!")
    return

def view_recipe(conn, cursor):
    print("\nAll Recipes: \n")
    print("-----------------------------------")

    cursor.execute("SELECT * from Recipes")
    results = cursor.fetchall()

    if len(results) == 0:
        print("Sorry, No Recipes found.")
        return
    else:
        for row in results:
            display_recipe(row)

main_menu(conn, cursor)
print("Closing Program.")