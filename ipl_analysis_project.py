"""
Complete IPL Match Analysis Project
Dataset: matches(3).csv

How to run:
1. Install requirements:
   pip install pandas matplotlib openpyxl

2. Put matches(3).csv in the same folder as this file.
3. Run:
   python ipl_analysis_project.py

Output:
- Cleaned CSV
- Summary Excel file
- Charts in charts/ folder
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("matches(3).csv")
OUTPUT_DIR = Path("output")
CHARTS_DIR = OUTPUT_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)
CHARTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

# -----------------------------
# 1. Data Cleaning
# -----------------------------
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

for col in ["city", "winner", "player_of_match", "venue", "team1", "team2", "toss_winner", "toss_decision"]:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

df.to_csv(OUTPUT_DIR / "cleaned_ipl_matches.csv", index=False)

# -----------------------------
# 2. Basic Analysis
# -----------------------------
total_matches = df.shape[0]
total_columns = df.shape[1]
matches_per_season = df["season"].value_counts().sort_index()
top_winners = df["winner"].replace("Unknown", pd.NA).dropna().value_counts().head(10)
toss_decisions = df["toss_decision"].value_counts()
top_players = df["player_of_match"].replace("Unknown", pd.NA).dropna().value_counts().head(10)
top_venues = df["venue"].value_counts().head(10)

teams = pd.concat([df["team1"], df["team2"]])
matches_played = teams.value_counts()
wins = df["winner"].replace("Unknown", pd.NA).dropna().value_counts()
win_percentage = ((wins / matches_played) * 100).dropna().sort_values(ascending=False).head(10)

valid_toss = df[df["winner"] != "Unknown"]
toss_winner_match_winner_pct = round((valid_toss["toss_winner"] == valid_toss["winner"]).mean() * 100, 2)

summary = pd.DataFrame([
    ["Total Matches", total_matches],
    ["Total Columns", total_columns],
    ["Seasons", f"{df['season'].min()} to {df['season'].max()}"],
    ["Most Winning Team", top_winners.index[0]],
    ["Most Player of Match Awards", top_players.index[0]],
    ["Most Common Toss Decision", toss_decisions.index[0]],
    ["Toss Winner Also Match Winner %", toss_winner_match_winner_pct],
], columns=["Metric", "Value"])

# -----------------------------
# 3. Save Summary Tables
# -----------------------------
with pd.ExcelWriter(OUTPUT_DIR / "ipl_analysis_summary.xlsx", engine="openpyxl") as writer:
    summary.to_excel(writer, sheet_name="Summary", index=False)
    matches_per_season.reset_index().to_excel(writer, sheet_name="Matches per Season", index=False)
    top_winners.reset_index().to_excel(writer, sheet_name="Top Winners", index=False)
    toss_decisions.reset_index().to_excel(writer, sheet_name="Toss Decisions", index=False)
    top_players.reset_index().to_excel(writer, sheet_name="Top Players", index=False)
    top_venues.reset_index().to_excel(writer, sheet_name="Top Venues", index=False)
    win_percentage.reset_index().to_excel(writer, sheet_name="Win Percentage", index=False)

# -----------------------------
# 4. Chart Functions
# -----------------------------
def save_bar(series, title, xlabel, ylabel, filename, rotation=45):
    plt.figure(figsize=(11, 6))
    series.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / filename, dpi=160)
    plt.close()

def save_pie(series, title, filename):
    plt.figure(figsize=(8, 8))
    series.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title(title)
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / filename, dpi=160)
    plt.close()

# -----------------------------
# 5. Create Charts
# -----------------------------
save_bar(matches_per_season, "IPL Matches per Season", "Season", "Number of Matches", "01_matches_per_season.png", rotation=0)
save_bar(top_winners, "Top 10 Teams by Match Wins", "Team", "Wins", "02_top_teams_by_wins.png")
save_pie(toss_decisions, "Toss Decision Distribution", "03_toss_decision_distribution.png")
save_bar(top_players, "Top 10 Player of the Match Winners", "Player", "Awards", "04_top_players_of_match.png")
save_bar(top_venues, "Top 10 IPL Venues by Matches", "Venue", "Matches", "05_top_venues.png")
save_bar(win_percentage, "Top 10 Team Win Percentage", "Team", "Win %", "06_team_win_percentage.png")

print("\nIPL Analysis Completed Successfully!")
print(summary)
print("\nCharts saved in:", CHARTS_DIR)
print("Summary Excel saved in:", OUTPUT_DIR / "ipl_analysis_summary.xlsx")
