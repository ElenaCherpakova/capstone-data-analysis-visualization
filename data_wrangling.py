import pandas as pd

raw_players = pd.read_csv('csv/players.csv')

team_name_mapping = {
    "Oakland": "Oakland Athletics",
    "Boston": "Boston Red Sox",
    "Toronto": "Toronto Blue Jays",
    "Anaheim":"Anaheim Angels",
    "Seattle": "Seattle Mariners",
    "Kansas City": "Kansas City Royals",
    "Minnesota": "Minnesota Twins",
    "Texas": "Texas Rangers",
    "New York": "New York Yankees",
    "Tampa Bay": "Tampa Bay Rays",
    "Baltimore": "Baltimore Orioles",
    "Los Angeles": "Los Angeles Angels",
    "Detroit": "Detroit Tigers",
    "Chicago": "Chicago White Sox",
    "Houston": "Houston Astros",
    "Cleveland": "Cleveland Indians"
}

raw_players['Team'] = raw_players['Team'].map(team_name_mapping).fillna(raw_players['Team'])
raw_players.to_csv('csv/cleaned_players.csv', index=False)