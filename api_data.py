import requests

def fetch_from_api(food_name, grams=None):
    """
    Fetch nutrition info from Nutritionix API.
    grams: if provided, query API for this exact amount
    Returns: dict with calories, protein, carbs, fat
    """
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {"x-app-id": "da6f14c2","x-app-key": "85cd39ae27628e550db21f698472d0e6", "Content-Type": "application/json"}

    if grams:
        query_text = f"{grams} g {food_name}"
    else:
        query_text = food_name

    data = {"query": query_text}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if 'foods' not in result or not result['foods']:
            print(f"No nutrition data found for: {food_name}")
            return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

        food = result['foods'][0]
        print(f"Nutrition data for: {food_name} fetched by API")
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
        print(f"Error for {food_name}:", e)
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}