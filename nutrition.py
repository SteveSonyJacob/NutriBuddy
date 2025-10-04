import os
import json
from api_data import fetch_from_api  # your API function

# Load local nutrition DB
try:
    with open(os.path.join("data", "custom_data.json"), "r") as f:
        CUSTOM_NUTRITION = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print("Warning: Could not load custom nutrition data. Using empty database.")
    CUSTOM_NUTRITION = {}

# Load portion mapping
try:
    with open(os.path.join("data", "portion_to_grams.json"), "r") as f:
        PORTION_MAP = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print("Warning: Could not load portion mapping. Using default 100g portions.")
    PORTION_MAP = {}

def estimate_grams(food_name, qty=1):
    """Return approximate grams for a food item"""
    return PORTION_MAP.get(food_name.lower().strip(), 100) * qty

def get_nutrition_for(food_name, grams):
    """
    Returns nutrition info for a food item and given grams.
    1. Checks local DB
    2. Scales nutrition from local DB if found
    3. Otherwise calls Nutritionix API with exact grams
    """
    key = food_name.lower().strip()
    if key in CUSTOM_NUTRITION:
        nutr_100g = CUSTOM_NUTRITION[key]
        factor = grams / 100
        return {k: v * factor for k,v in nutr_100g.items()}
    else:
        # Not in DB → fetch from Nutritionix API with exact amount
        return fetch_from_api(food_name, grams=grams)
