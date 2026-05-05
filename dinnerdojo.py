import requests #import requests to help process the api

import webbrowser #import webbrowser to open thumbnail links

def choose_category():
    categories = [
        "Beef", "Chicken", "Dessert", "Lamb", "Miscellaneous",
        "Pasta", "Pork", "Seafood", "Side", "Starter",
        "Vegan", "Vegetarian", "Breakfast", "Goat"
    ]

    print("Choose a category:")
    for category in categories:
        print("-", category)

    user_category = input("\nEnter category: ").strip().title()
    return user_category

def get_meals_from_api(category): #get all the meals from the database for the user selected category
    url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=" + category

    try: #handle errors with a try except block, e.g. if the category doesn't exist
        response = requests.get(url)
        data = response.json()
    except:
        print("Could not connect to API.")
        return []

    if data["meals"] is None:
        return []

    meals = [] #list of

    for meal in data["meals"]: #get all information for each meal and add it to full_data
        full_url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + meal["idMeal"]
        full_response = requests.get(full_url)
        full_data = full_response.json() #use json to reproduce the data

        if full_data["meals"]:
            meals.append(full_data["meals"][0]) #list of meals with a dictionary for each entry

    return meals

def get_recipe_ingredients(recipe): #takes the recipe and outputs the ingredients and weighted score
    recipe_ingredients = {}

    for i in range(1, 21):
        strIng = "strIngredient" + str(i)

        if recipe[strIng]:
            recipe_ingredients[recipe[strIng].lower()] = i

    return recipe_ingredients

def user_ingredients(): #take in user ingredients
    user_input = input("Enter ingredients (comma separated): ")
    return [item.strip().lower() for item in user_input.split(",")]

def dinner_dojo(category,recipes): #evaluate best matches
    category_ingredients = set() #get all the ingredients of the category
    for recipe in recipes:
        recipe_ingredients = get_recipe_ingredients(recipe)
        for i in recipe_ingredients:
            if i not in category_ingredients:
                category_ingredients.add(i)
    print(f'Here are the ingredients for recipes in {category}.')
    for i in sorted(category_ingredients):
        print(i)

    ingredients = user_ingredients()
    recipe_scores = {}
    recipe_matched = {}
    recipe_missing = {}

    for recipe in recipes:
        recipe_ingredients = get_recipe_ingredients(recipe)

        possible_score = 0
        points = 0

        matched = [] #create a list of ingredients in the recipe the user has
        missing = [] #create a list of ingredients in the recipe the user doesn't have


        for ingredient in recipe_ingredients:
            if ingredient.lower() in ingredients:
                points += 10*(21-recipe_ingredients[ingredient])
                possible_score += 10*(21-recipe_ingredients[ingredient])
                matched.append(ingredient)
            else:
                possible_score += 10*(21-recipe_ingredients[ingredient])
                missing.append(ingredient)

        recipe_scores[recipe["strMeal"]]= (points/possible_score) #percentage math
        recipe_matched[recipe["strMeal"]] = matched
        recipe_missing[recipe["strMeal"]] = missing

    sorted_recipes= dict(sorted(recipe_scores.items(), key=lambda item: item[1], reverse=True)) #sort recipes by highest score

    matches = []
    for i in sorted_recipes:
        matches.append(i) #add reipes ot matches in order

    return matches, recipe_matched, recipe_missing


if __name__ == "__main__":

    category = choose_category()

    print(f"\nFetching {category} recipes...\n")
    meals = get_meals_from_api(category)

    if not meals:
        print("No meals found for that category.")
        exit()

    matches, recipe_matched, recipe_missing = dinner_dojo(category,meals)

    meal_name = matches[0]
    meal = next(m for m in meals if m["strMeal"] == meal_name) #get the full data for that meal name from meals data

    print(f"\nBest suggestion: {meal_name}")
    print("You have these ingredients: ",recipe_matched[matches[0]])
    print("You are missing these ingredients: ",recipe_missing[matches[0]])

    picture = input("Would you like to see a picture? Y/N ")
    if picture == 'Y':
        webbrowser.open(meal["strMealThumb"]) #open a picture of the meal

    recipe = 0 #inialize recipe variable

    while True:
        make = input('Do you want to make this? Y/N ')
        if make == 'N':
            recipe +=1
            try:
                meal_name = matches[recipe]
                print(f'\nNext best suggestion: {meal_name}')
                meal = next(m for m in meals if m["strMeal"] == meal_name) #get all data of the meal

                print(matches[recipe])
                print("You have these ingredients: ",recipe_matched[matches[recipe]])
                print("You are missing these ingredients: ",recipe_missing[matches[recipe]])

                picture = input("Would you like to see a picture? Y/N ")
                if picture == 'Y':
                    webbrowser.open(meal["strMealThumb"])

            except IndexError: #if user runs out of meals
                print(f'No more {category} recipes!')

        elif make == 'Y': #print instrutions
            print(f'{category} dish = {meal_name}')

            print('\nIngredients: ')
            for i in range(1,21):
                strIng = "strIngredient" + str(i)
                strMeas = "strMeasure" + str(i)
                if meal[strIng]:
                    print(f'{meal[strMeas]} {meal[strIng]}')

            print('\nInstructions')
            print(meal['strInstructions'])

            break

        else:
            print('Answer must be Y or N!')
