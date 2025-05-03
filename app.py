import streamlit as st
import pandas as pd
from utils import find_best_matches, calculate_score  # Assuming this function exists

st.set_page_config(page_title="Roommate Compatibility", layout="wide")
st.markdown("<style>" + open("style.css").read() + "</style>", unsafe_allow_html=True)

st.title("🏠 Home Sweet Home – Roommate Compatibility Checker")

st.sidebar.header("🧑 Your Profile")

name = st.sidebar.text_input("Name")
sleep = st.sidebar.selectbox("Sleep Time", ["Early", "Late"])
clean = st.sidebar.selectbox("Cleanliness", ["Neat", "Flexible", "Messy"])
work = st.sidebar.selectbox("Work Schedule", ["Day", "Night", "Mixed"])
food = st.sidebar.selectbox("Food Habits", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])

# Function to check if the name already exists
def is_name_unique(name, df):
    return name not in df["Name"].values

if st.sidebar.button("🔍 Find Matches"):
    user_data = {
        "Name": name,
        "Sleep Time": sleep,
        "Cleanliness": clean,
        "Work Schedule": work,
        "Food Habits": food,
    }

    try:
        df = pd.read_csv("profiles.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Sleep Time", "Cleanliness", "Work Schedule", "Food Habits", "Score"])

    # Check if the name is unique
    if not is_name_unique(name, df):
        st.warning(f"Name '{name}' is already taken! Please choose a different name.")
    else:
        new_row = pd.DataFrame([user_data])

        # Calculate compatibility score for the user
        df["Score"] = df.apply(lambda row: calculate_score(user_data, row), axis=1)
        
        # Add the new user data and save to CSV
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("profiles.csv", index=False)

        st.subheader(f"🔗 Best Roommate Matches for {name}")
        matches = find_best_matches(user_data, df[df["Name"] != name])
        for _, row in matches.iterrows():
            st.markdown(f"""
            ### 🧍 {row['Name']}
            - 💤 Sleep Time: {row['Sleep Time']}
            - 🧼 Cleanliness: {row['Cleanliness']}
            - 💼 Work Schedule: {row['Work Schedule']}
            - 🍽️ Food Habits: {row['Food Habits']}
            - ❤️ Compatibility Score: **{row['Score']}%**
            """)
