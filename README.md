# NutriBuddy 🍽️

A comprehensive nutrition tracking application for mess/canteen meal planning and daily nutrition monitoring.

## Features

- **Weekly Menu Planning**: Pre-loaded with comprehensive weekly meal menus
- **Nutrition Tracking**: Track calories, protein, carbs, and fat for each meal
- **Portion Control**: Adjust quantities and portions for accurate tracking
- **API Integration**: Uses Nutritionix API for detailed nutrition information
- **Local Database**: Custom nutrition database for common foods
- **Manual Entry**: Add custom foods not in the menu
- **Daily Summary**: View your complete daily nutrition intake

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Configuration**
   - Get API credentials from [Nutritionix](https://www.nutritionix.com/business/api)
   - Create a `.env` file in the project root:
   ```
   API_ID=your_api_id_here
   API_KEY=your_api_key_here
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select the day of the week to view the menu
2. Mark meals as consumed and adjust quantities
3. Add items to your daily nutrition tracker
4. Use manual entry for foods not in the menu
5. View your daily nutrition summary

## Project Structure

- `app.py` - Main Streamlit application
- `daily_tracker.py` - Daily nutrition tracking logic
- `nutrition.py` - Nutrition calculation and API integration
- `api_data.py` - Nutritionix API interface
- `data/` - JSON files containing menu and nutrition data
  - `menu.json` - Weekly meal menus
  - `custom_data.json` - Local nutrition database
  - `portion_to_grams.json` - Portion size mappings

## Requirements

- Python 3.7+
- Streamlit
- Requests
- python-dotenv