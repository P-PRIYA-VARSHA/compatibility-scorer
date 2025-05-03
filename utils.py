import pandas as pd

def calculate_score(user, roommate):
    score = 0
    total = 4  # total criteria

    if user["Sleep Time"] == roommate["Sleep Time"]:
        score += 1
    if user["Cleanliness"] == roommate["Cleanliness"]:
        score += 1
    if user["Work Schedule"] == roommate["Work Schedule"]:
        score += 1
    if user["Food Habits"] == roommate["Food Habits"]:
        score += 1

    return int((score / total) * 100)

def find_best_matches(user, df):
    df["Score"] = df.apply(lambda row: calculate_score(user, row), axis=1)
    sorted_df = df.sort_values(by="Score", ascending=False)
    return sorted_df
