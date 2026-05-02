import requests
#from Test_Recipes import meals


def get_recipe_ingredients(recipe):
    recipe_ingredients = {}

    for i in range(1, 21):
        strIng = "strIngredient" + str(i)

        if recipe[strIng]:
            recipe_ingredients[recipe[strIng].lower()] = i

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
    ingredients = set()
    for recipe in recipes:
        recipe_ingredients = get_recipe_ingredients(recipe)
        for i in recipe_ingredients:
            if i not in ingredients:
                ingredients.add(i)
    print(f'Here are the ingredients for recipes in {category}.')
    for i in sorted(ingredients):
        print(i)
    ingredients = user_ingredients()
    recipe_scores = {}
    recipe_matched = {}
    recipe_missing = {}

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
        recipe_matched[recipe["strMeal"]] = matched
        recipe_missing[recipe["strMeal"]] = missing
    sorted_recipes= dict(sorted(recipe_scores.items(), key=lambda item: item[1], reverse=True))
    matches = []
    for i in sorted_recipes:
        matches.append(i)
    return matches, recipe_matched, recipe_missing

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
    matches, recipe_matched, recipe_missing = dinner_dojo(category,meals)

    meal_str = matches[0]
best_meal_name = matches[0]
best_meal = next(m for m in meals if m["strMeal"] == best_meal_name)

print("Thumbnail URL:", best_meal["strMealThumb"])
    print("\nBest suggestion:")
    print(matches[0])
    print("You have these ingredients: ",recipe_matched[matches[0]])
    print("You are missing these ingredients: ",recipe_missing[matches[0]])
    recipe = 0
    while True:
        make = input('Do you want to make this? Y/N ')
        if make == 'N':
            recipe +=1
            try:
                print(matches[recipe])
                print("You have these ingredients: ",recipe_matched[matches[recipe]])
                print("You are missing these ingredients: ",recipe_missing[matches[recipe]])
            except IndexError:
                print(f'No more {category} recipes!')
        elif make == 'Y':
            print(f'{category} dish = {matches[recipe]}')
            break
        else:
            print('Answer must be Y or N!')
