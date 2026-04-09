from Test_Fridge import ingredients
from Test_Recipes import meals

def dinner_dojo(ingredients, recipes):
    suggestion = ''
    score = 0
    for recipe in recipes:
        new_score = 0
        for ingredient in ingredients:
            if ingredient == recipe["strIngredient1"]:
                new_score += 200
        if new_score > score:
            suggestion = recipe["idMeal"]
    return suggestion

'''
    # Step 3: process
    can_make = []
    almost = []

    for recipe, ingredients in recipes.items():
        if ingredients.issubset(fridge):
            can_make.append(recipe)
        elif len(ingredients.intersection(fridge)) >= 2:
            almost.append((recipe, ingredients - fridge))

    # Step 4: output
    print("\nYou can make:")
    if can_make:
        for r in can_make:
            print("-", r)
    else:
        print("Nothing exact")

    print("\n Almost there:")
    if almost:
        for r, missing in almost:
            print(f"- {r} (missing: {', '.join(missing)})")
    else:
        print("No close matches")
'''
def user_ingredients():
 # Step 1: get user input
    user_input = input("Enter 3 ingredients (comma separated): ").lower()
    fridge = set(item.strip() for item in user_input.split(","))
    return fridge

def some_other_recipes():

    # Step 2: recipe database
    recipes = {
        "grilled cheese": {"bread", "cheese", "butter"},
        "omelet": {"eggs", "butter", "salt"},
        "pasta aglio e olio": {"pasta", "garlic", "oil"},
        "egg salad": {"eggs", "mayo", "salt"},
        "toast with cheese": {"bread", "cheese"}
    }


if __name__ == "__main__":
    dinner_dojo(ingredients,meals)


