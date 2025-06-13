import pandas as pd
import sqlite3

cleaned_players = pd.read_csv('csv/cleaned_players.csv')
# Remove any duplicate rows from the DataFrame
unique_players = cleaned_players[[
    'Player_ID', 'Name', 'Team']].drop_duplicates()
annual_stats = cleaned_players[[
    'Player_ID', 'Statistic', 'Value', 'Year']].drop_duplicates()
unique_players = unique_players.rename(columns={
    "Player_ID": "player_id",
    "Name": "name",
    "Team": "team",
})
annual_stats = annual_stats.rename(columns={
    "Player_ID": "player_id",
    "Statistic": "statistic_type",
    "Value": "value",
    "Year": "year"
})
raw_stats_players = pd.read_csv('csv/players_stats.csv')
print(raw_stats_players)
clean_stats_data = raw_stats_players.copy()

# Drop some columns such as
# GRSL - Grand Slams,
# IBB - Intentional Walks,
# SH - Sacrifice Hits,
# SF - Sacrifice Flies,
# HBP - Hit By Pitch,
# GIDP - Ground Into Double Play
drop_columns = ['GRSL', 'IBB', 'SH', 'SF', 'HBP', 'GIDP']
players_stat_df_cleaned = clean_stats_data.drop(columns=drop_columns)
# Rename columns for clarity
stats_df = players_stat_df_cleaned.rename(columns={
    "Player_ID": "player_id",
    "Career_Length": "career_length",
    "G": "games_played",
    "AB": "at_bats",
    "R": "runs",
    "H": "hits",
    "2B": "doubles",
    "3B": "triples",
    "HR": "home_runs",
    "RBI": "runs_batted_in",
    "BB": "walks",
    "SO": "strikeouts",
    "AVG": "batting_average",
    "OBP": "on_base_percentage",
    "SLG": "slugging_percentage"
})


def add_player(cursor, row):
    try:
        cursor.execute(
            "INSERT INTO Players (player_id, name, team) VALUES (?, ?, ?)", (row['player_id'], row['name'], row['team']))
        print(f"Player {row['name']} added successfully.")
    except sqlite3.IntegrityError:
        print(f"{row['name']} is already in the database.")


def add_annual_stats(cursor, row):
    cursor.execute(
        "SELECT * FROM Players WHERE player_id = ?", (row['player_id'],))
    results = cursor.fetchone()
    if results is None:
        print(f"No player found with ID {row['player_id']}")
        return
    try:
        cursor.execute(
            "INSERT INTO PlayerStats (player_id, statistic_type, value, year) VALUES (?, ?, ?, ?)", (row['player_id'], row['statistic_type'], row['value'], row['year']))
        print(
            f"Annual stat for year {row['year']} added successfully for player ID {row['player_id']}.")
    except sqlite3.IntegrityError:
        print(
            f"Annual stat for {row['year']} already exists for player ID {row['player_id']}.")


def add_career_stats(cursor, row):
    cursor.execute(
        "SELECT * FROM Players WHERE player_id = ?", (row['player_id'],))
    results = cursor.fetchone()
    if results is None:
        print(f"No player found with ID {row['player_id']}")
        return
    try:
        cursor.execute(
            "INSERT INTO CareerStats (player_id, career_length, games_played, at_bats, runs, hits, doubles, triples, home_runs, runs_batted_in, walks, strikeouts, batting_average, on_base_percentage, slugging_percentage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                row['player_id'], row['career_length'], row['games_played'], row['at_bats'], row['runs'], row['hits'],
                row['doubles'], row['triples'], row['home_runs'], row['runs_batted_in'], row['walks'], row['strikeouts'],
                row['batting_average'], row['on_base_percentage'], row['slugging_percentage']
            ))
        print(
            f"Career stat added successfully for player ID {row['player_id']}.")
    except sqlite3.IntegrityError:
        print(
            f"Career stat already exists for player ID {row['player_id']}.")


try:
    with sqlite3.connect('./db/players.db') as conn:
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = 1")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Players(
            player_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            team TEXT NOT NULL
            )
        """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS PlayerStats (
                        player_id TEXT,
                        statistic_type TEXT,
                        value REAL,
                        year INTEGER,
                        FOREIGN KEY (player_id) REFERENCES Players(player_id),
                        UNIQUE (player_id, statistic_type, year)
                   )""")
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS CareerStats(
                       player_id TEXT,
                       career_length INTEGER,
                       games_played INTEGER,
                       at_bats INTEGER,
                       runs INTEGER,
                       hits INTEGER,
                       doubles INTEGER,
                       triples INTEGER,
                       home_runs INTEGER,
                       runs_batted_in INTEGER,
                       walks INTEGER,
                       strikeouts INTEGER,
                       batting_average REAL,
                       on_base_percentage REAL,
                       slugging_percentage REAL,
                       FOREIGN KEY (player_id) REFERENCES Players(player_id))
                       """)
        print('Tables created successfully.')

        for _, row in unique_players.iterrows():
            add_player(cursor, row)

        for _, row in annual_stats.iterrows():
            add_annual_stats(
                cursor, row)

        for _, row in stats_df.iterrows():
            add_career_stats(cursor, row)

        conn.commit()

except sqlite3.Error as e:
    print(f"SQL Error: {e}")
