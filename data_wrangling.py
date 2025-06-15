import pandas as pd
import unicodedata
raw_players = pd.read_csv('csv/players.csv')

duplicates = raw_players.groupby('Player_ID')['Name'].nunique()
conflicts = duplicates[duplicates > 1]

if not conflicts.empty:
    print('Found conflicts of Player_ID:')
    conflict_ids = conflicts.index.to_list()
    print(raw_players[raw_players['Player_ID'].isin(
        conflict_ids)][['Player_ID', 'Name']].drop_duplicates())

correct_players_name = {
    "Brett Gardner":"gardnbr01",
    "Josh Donaldson": "donaljo02"
}

# Clean names by adding spaces if there is none and remove any normalized characters if there are diacritics (é)
def clean_name(name):
    name = name.strip()
    chars = []
    normalized_name = unicodedata.normalize('NFD', name)
    for char in normalized_name: 
        if unicodedata.category(char) != "Mn":
            chars.append(char)
    name = ''.join(chars)    
    res = name[0]
    for char in name[1:]:
        if char.isupper() and res[-1] != ' ':
            res += ' '
        res += char
    return ' '.join(res.split()).title()

team_name_mapping = {
    "Oakland": "Oakland Athletics",
    "Boston": "Boston Red Sox",
    "Toronto": "Toronto Blue Jays",
    "Anaheim": "Anaheim Angels",
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


raw_players['Name'] = raw_players['Name'].apply(clean_name)


for name, player_id in correct_players_name.items():
    raw_players.loc[raw_players['Name'] == name, 'Player_ID'] = player_id

raw_players['Team'] = raw_players['Team'].map(
    team_name_mapping).fillna(raw_players['Team'])

# print(raw_players.loc[raw_players['Name'] == "Brett Gardner", ['Player_ID', 'Name']])
# print(raw_players.loc[raw_players['Name'] == "Josh Donaldson", ['Player_ID', 'Name']])

raw_players.to_csv('csv/cleaned_players.csv', index=False)

