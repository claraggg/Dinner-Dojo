import requests
#from Test_Recipes import meals


def get_recipe_ingredients(recipe):
    recipe_ingredients = []

    for i in range(1, 21):
        strIng = "strIngredient" + str(i)

        if recipe[strIng]:
            recipe_ingredients.append(recipe[strIng])

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


def dinner_dojo(user_ingredients, recipes):
    best_suggestion = ""
    best_score = 0
    best_missing = []

    can_make = []
    almost_there = []

    for recipe in recipes:
        points = 0
        possible_score = 0
        missing = []

        for i in range(1, 21):
            strIng = "strIngredient" + str(i)
            ingredient = recipe[strIng]

            if ingredient:
                weight = 10 * (21 - i)
                possible_score += weight

                if ingredient.lower() in user_ingredients:
                    points += weight
                else:
                    missing.append(ingredient)

        if possible_score > 0:
            score = points / possible_score
        else:
            score = 0

        if len(missing) == 0:
            can_make.append(recipe["strMeal"])

        elif (points > 0):  # at least something matched
            almost_there.append((recipe["strMeal"], missing))

        if score > best_score:
            best_score = score
            best_suggestion = recipe["strMeal"]
            best_missing = missing

    almost_there = [item for item in almost_there if item[0] != best_suggestion]

    return best_suggestion, best_missing, can_make, almost_there
🧠 What this does (quickly)
gives higher weight to earlier ingredients

calculates:

score = weighted_matches / total_possible_weight
still supports:
best suggestion ✅
can_make ✅
almost_there ✅
🎤 What you can say in your video

“I initially implemented a weighted scoring system that prioritized earlier ingredients in the recipe, but later simplified it to a ratio-based system for clarity and maintainability.”

🔥 This is very strong academically — shows iteration.

⚡ My honest advice

👉 Keep your current simple system in final code
👉 Mention the weighted one as a design iteration

That way you:

show complexity ✅
show improvement ✅
don’t risk bugs in demo 😌

If you want, I can also help you:
👉 quickly compare outputs (weighted vs simple) for your demo
👉 or decide which one looks better live (important lol)
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
    user_input = user_ingredients()
    print("Your ingredients:")
    print(user_input)
    print(f"\nFetching {category} recipes...\n")
    meals = get_meals_from_api(category)
    if not meals:
        print("No meals found for that category.")
        exit()
    suggestion, missing, can_make, almost_there = dinner_dojo(user_input, meals)

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
