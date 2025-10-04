import streamlit as st
import json
from datetime import datetime
from daily_tracker import DailyTracker
from nutrition import estimate_grams, get_nutrition_for
from api_data import fetch_from_api  # Nutritionix API

# Load menu
try:
    with open("data/menu.json", "r") as f:
        MENU = json.load(f)
except FileNotFoundError:
    st.error("❌ Menu data file not found. Please ensure 'data/menu.json' exists.")
    st.stop()
except json.JSONDecodeError:
    st.error("❌ Invalid JSON in menu data file. Please check 'data/menu.json' format.")
    st.stop()

st.set_page_config(page_title="Mess Nutrition Tracker", layout="centered")
st.title("🍽️ Mess Nutrition Tracker")

# Initialize tracker
if "tracker" not in st.session_state:
    st.session_state.tracker = DailyTracker()

# Choose day
weekday = datetime.today().strftime('%A')
selected_day = st.selectbox(
    "Select day", list(MENU.keys()),
    index=list(MENU.keys()).index(weekday) if weekday in MENU else 0
)

st.markdown(f"### Menu for **{selected_day}**")

# Meal tracking with partial consumption
for meal_name, items in MENU[selected_day].items():
    st.subheader(meal_name)
    had_key = f"had_{selected_day}_{meal_name}"       # session_state key
    button_key = f"{had_key}_button"                  # widget key

    # Initialize session state safely
    if had_key not in st.session_state:
        st.session_state[had_key] = False

    # Button for marking meal eaten
    if st.button(f"Had {meal_name}?", key=button_key):
        st.session_state[had_key] = True

    if st.session_state[had_key]:
        st.write("Adjust quantities or deselect items you didn't eat:")
        for i, it in enumerate(items):
            col1, col2, col3 = st.columns([3, 1, 2])
            with col1:
                new_name = st.text_input(
                    f"Item {i+1}", value=it['name'], 
                    key=f"{selected_day}_{meal_name}_name_{i}"
                )
            with col2:
                qty = st.number_input(
                    "Qty", min_value=0.0, value=float(it.get('qty', 1.0)),
                    step=0.5, key=f"{selected_day}_{meal_name}_qty_{i}"
                )
            with col3:
                include = st.checkbox(
                    "Include?", value=True, 
                    key=f"include_{selected_day}_{meal_name}_{i}"
                )

            if include and qty > 0:
                grams_final = estimate_grams(new_name, qty)
                nutr = get_nutrition_for(new_name, grams_final)
                st.write(
                    f"{grams_final} g → "
                    f"{round(nutr['calories'],1)} kcal, "
                    f"P:{round(nutr['protein'],1)}g "
                    f"C:{round(nutr['carbs'],1)}g "
                    f"F:{round(nutr['fat'],1)}g"
                )
                if st.button(
                    f"Add {new_name} to today's intake", 
                    key=f"add_{selected_day}_{meal_name}_{i}"
                ):
                    st.session_state.tracker.add_item(new_name, grams_final, nutr)
                    st.success(f"Added {new_name} — {int(grams_final)}g")

st.markdown("---")

# Manual entry
st.header("What did you eat? (Manual entry)")
manual_name = st.text_input("Food name", value="", key="manual_name")
unit_choice = st.radio("Enter amount as", ("Grams", "Quantity (count)"), index=0, key="unit_choice")
manual_qty = None
manual_grams = None

if unit_choice == "Grams":
    manual_grams = st.number_input("Grams", min_value=0.0, value=100.0, key="manual_grams")
else:
    manual_qty = st.number_input("Quantity (count)", min_value=0.0, value=1.0, key="manual_qty")
    manual_grams = estimate_grams(manual_name, manual_qty)

if st.button("Add manual entry"):
    if not manual_name.strip():
        st.error("Enter a food name")
    else:
        # Check if in local DB
        nutr = get_nutrition_for(manual_name, manual_grams)
        if nutr == {"calories":0,"protein":0,"carbs":0,"fat":0}:
            # If not in DB, fetch from API
            nutr = fetch_from_api(manual_name, manual_grams)
        st.session_state.tracker.add_item(manual_name, manual_grams, nutr)
        st.success(f"Added {manual_name} ({int(manual_grams)} g)")

st.markdown("---")

# Today's summary
st.header("Today's Nutrition Summary")
summary = st.session_state.tracker.summary()

if summary["calories"] > 0:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Calories", f"{summary['calories']:.0f}")
    with col2:
        st.metric("Protein", f"{summary['protein']:.1f}g")
    with col3:
        st.metric("Carbs", f"{summary['carbs']:.1f}g")
    with col4:
        st.metric("Fat", f"{summary['fat']:.1f}g")
else:
    st.info("No items added to today's tracker yet.")

if st.button("Reset today's tracker"):
    st.session_state.tracker.reset()
    st.success("Tracker reset")
