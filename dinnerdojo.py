import requests
from Test_Fridge import ingredients
from Test_Fridge import ingredients
#from Test_Recipes import meals


def get_recipe_ingredients(recipe):
    recipe_ingredients = []

    for i in range(1, 21):
        strIng = "strIngredient" + str(i)

        if recipe[strIng] != "":
            recipe_ingredients.append(recipe[strIng])

    return recipe_ingredients

def get_meals_from_api():
    url = "https://www.themealdb.com/api/json/v1/1/search.php?f=a"
    response = requests.get(url)
    data = response.json()

    if data["meals"] is None:
        return []

    return data["meals"]


def dinner_dojo(user_ingredients, recipes):
    best_suggestion = ""
    best_score = 0
    best_missing = []

    can_make = []
    almost_there = []

    for recipe in recipes:
        recipe_ingredients = get_recipe_ingredients(recipe)

        matched = []
        missing = []

        for ingredient in recipe_ingredients:
            if ingredient in user_ingredients:
                matched.append(ingredient)
            else:
                missing.append(ingredient)

        if len(recipe_ingredients) > 0:
            score = len(matched) / len(recipe_ingredients)
        else:
            score = 0

        if len(missing) == 0:
            can_make.append(recipe["strMeal"])

        elif len(matched) >= 2:
            almost_there.append((recipe["strMeal"], missing))

        if score > best_score:
            best_score = score
            best_suggestion = recipe["strMeal"]
            best_missing = missing

    return best_suggestion, best_missing, can_make, almost_there


if __name__ == "__main__":
    test = "test2"

    print("Your ingredients:")
    print(ingredients[test])

    meals = get_meals_from_api()
    suggestion, missing, can_make, almost_there = dinner_dojo(ingredients[test], meals)

    print("\nBest suggestion:")
    print(suggestion)

    print("\nMissing ingredients:")
    if missing:
        print(", ".join(missing))
    else:
        print("You have everything!")

    print("\nYou can make:")
    if can_make:
        for meal in can_make:
            print("-", meal)
    else:
        print("Nothing exact")

    print("\nAlmost there:")
    if almost_there:
        for meal, missing_items in almost_there:
            print(f"- {meal} (missing: {', '.join(missing_items)})")
    else:
        print("No close matches")
