# Dinner Dojo
## Description
Dinner Dojo is a Python program that recommends recipes based on ingredients a user owns. The user selects a meal category (e.g., chicken, pasta, dessert) and inputs a list of available ingredients. The program retrieves recipes from TheMealDB API and compares each recipe’s ingredients with the user’s input. Each recipe is scored based on how many ingredients match, with higher weight given to more essential ingredients.
Based on this scoring system, the program provides:
- the best recipe suggestion
- a list of ingredients the user already has
- a list of missing ingredients
- additional recipe suggestions ranked by match quality
- the option to view an image of the dish
---
## How to Run
### 1. Prerequisites
Make sure you have:
- Python 3 installed
- Internet connection
### 2. Install required packages
This project requires the `requests` library:
pip install requests
### 3. Run the program
python3 dinner_dojo.py
### 4. Follow the prompts
- Choose a category
- Enter ingredients separated by commas
- Review suggested recipes
### Sources
TheMealDB API
