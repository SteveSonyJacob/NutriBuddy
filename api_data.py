import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")

def fetch_from_api(food_name, grams=None):
    """
    Fetch nutrition info from Nutritionix API.
    grams: if provided, query API for this exact amount
    Returns: dict with calories, protein, carbs, fat
    """
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {"x-app-id": api_id,"x-app-key": api_key}

    if grams:
        query_text = f"{grams} g {food_name}"
    else:
        query_text = food_name

    data = {"query": query_text,"detailed": True}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if 'foods' not in result or not result['foods']:
            print(f"No nutrition data found for: {food_name}")
            return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

        food = result['foods'][0]

        # Nutrition already scaled by the amount in query
        return {
            "calories": food.get('nf_calories', 0),
            "protein": food.get('nf_protein', 0),
            "carbs": food.get('nf_total_carbohydrate', 0),
            "fat": food.get('nf_total_fat', 0)
        }

    except requests.exceptions.RequestException as e:
        print(f"API Request Error for {food_name}:", e)
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    except Exception as e:
        print(f"API Error for {food_name}:", e)
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
