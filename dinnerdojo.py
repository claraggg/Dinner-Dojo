import requests
#from Test_Recipes import meals


def get_recipe_ingredients(recipe):
    recipe_ingredients = {}

    for i in range(1, 21):
        strIng = "strIngredient" + str(i)

        if recipe[strIng]:
            recipe_ingredients[recipe[strIng]] = i

    return recipe_ingredients

def get_meals_from_api(category):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=" + category

    try:
        response = requests.get(url)
        data = response.json()
    except:
        print("Could not connect to API.")
        return []

    if data["meals"] is None:
        return []

    meals = []

    for meal in data["meals"]:
        full_url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + meal["idMeal"]
        full_response = requests.get(full_url)
        full_data = full_response.json()

        if full_data["meals"]:
            meals.append(full_data["meals"][0])

    return meals


def dinner_dojo(category,recipes):
    best_suggestion = ""
    best_score = 0
    best_missing = []

    can_make = []
    almost_there = []
    ingredients = set()
    for recipe in recipes:
        recipe_ingredients = get_recipe_ingredients(recipe)
        for i in recipe_ingredients:
            if i not in ingredients:
                ingredients.add(i)
    print(f'Here are the ingredients for recipes in {category}.')
    print(ingredients)
    ingredients = user_ingredients()
    recipe_scores = {}

    for recipe in recipes:
        recipe_ingredients = get_recipe_ingredients(recipe)

        possible_score = 10*(21-len(recipe_ingredients))
        points = 0

        matched = []
        missing = []


        for ingredient in recipe_ingredients:
            if ingredient.lower() in ingredients:
                points += 10*(21-recipe_ingredients[ingredient])
                matched.append(ingredient)
            else:
                missing.append(ingredient)
        recipe_scores[recipe["strMeal"]]= (points/possible_score)
    sorted_recipes= dict(sorted(recipe_scores.items(), key=lambda item: item[1], reverse=True))
    matches = []
    for i in sorted_recipes:
        matches.append(i)
    return matches

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

def user_ingredients():
    user_input = input("Enter ingredients (comma separated): ")
    return [item.strip().lower() for item in user_input.split(",")]


if __name__ == "__main__":
    category = choose_category()
    print(f"\nFetching {category} recipes...\n")
    meals = get_meals_from_api(category)
    if not meals:
        print("No meals found for that category.")
        exit()
    matches = dinner_dojo(category,meals)

    print("\nBest suggestion:")
    print(matches[0])
