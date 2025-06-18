import pandas as pd
import unicodedata
import re

raw_players = pd.read_csv('../raw_data/players.csv')

duplicates = raw_players.groupby('player_id')['name'].nunique()
conflicts = duplicates[duplicates > 1]

if not conflicts.empty:
    print('Found conflicts of Player_ID:')
    conflict_ids = conflicts.index.to_list()
    print(raw_players[raw_players['player_id'].isin(
        conflict_ids)][['player_id', 'name']].drop_duplicates())

correct_players_name = {
    "Brett Gardner":"gardnbr01",
    "Josh Donaldson": "donaljo02"
}

# Clean names by adding spaces if there is none and remove any normalized characters if there are diacritics (é)
def clean_name(name):
    name = unicodedata.normalize('NFD', name)
    name = ''.join(char for char in name if unicodedata.category(char) != 'Mn')
    name = re.sub(r'\*$', '', name).strip()
    if not re.match(r'^[A-Z]{1,3}\b', name): 
        name = re.sub(r'(?<=[a-z])(?=[A-Z][a-z])', ' ', name)
    return name

def resolve_team_name(team, league):
    if team == 'New York':
        return 'New York Yankees' if league == 'American' else 'New York Mets'
    elif team == 'Los Angeles':
        return 'Los Angeles Angels' if league == 'American' else 'Los Angeles Dodgers'
    elif team == 'Chicago':
        return 'Chicago White Sox' if league == 'American' else 'Chicago Cubs'
    return team

team_name_mapping = {
    "Oakland": "Oakland Athletics",
    "Boston": "Boston Red Sox",
    "Toronto": "Toronto Blue Jays",
    "Anaheim": "Anaheim Angels",
    "Atlanta":"Atlanta Braves",
    "Arizona": "Arizona Diamondbacks",
    "Philadelphia": "Philadelphia Phillies",
    "Seattle": "Seattle Mariners",
    "Kansas City": "Kansas City Royals",
    "Minnesota": "Minnesota Twins",
    "Pittsburgh": "Pittsburgh Pirates",
    "Texas": "Texas Rangers",
    "Tampa Bay": "Tampa Bay Rays",
    "Baltimore": "Baltimore Orioles",
    "Detroit": "Detroit Tigers",
    "Houston": "Houston Astros",
    "Cleveland": "Cleveland Indians",
    "San Francisco": "San Francisco Giants",
    "San Diego": "San Diego Padres",
    "St. Louis": "St. Louis Cardinals",
    "Colorado": "Colorado Rockies",
    "Milwaukee": "Milwaukee Brewers",
    "Miami": "Miami Marlins",
    "Washington": "Washington Nationals",
    "Cincinnati": "Cincinnati Reds",
    "Florida": "Florida Marlins",
    "Montreal": "Montreal Expos"
}

raw_players['name'] = raw_players['name'].apply(clean_name)
print(raw_players['name'])
raw_players['team'] = raw_players['team'].str.split('/').str[0].str.strip()
raw_players['team'] = raw_players.apply(
    lambda row: resolve_team_name(row['team'], row['league']),
    axis=1
)


raw_players['player_id'].update(raw_players['name'].map(correct_players_name) )
raw_players['team'] = raw_players['team'].map(
    team_name_mapping).fillna(raw_players['team'])

unmapped = raw_players.loc[~raw_players['team'].isin(team_name_mapping.keys()), 'team'].unique()
print("Teams not in mapping:", unmapped)


raw_players.to_csv('../clean_data/players.csv', index=False)

