import pandas as pd
import sqlite3

cleaned_players = pd.read_csv('csv/cleaned_players.csv')
# Remove any duplicate rows from the DataFrame
unique_players = cleaned_players[[
    'player_id', 'name', 'team']].drop_duplicates()
annual_stats = cleaned_players[[
    'player_id', 'statistic', 'value', 'year']].drop_duplicates()

stats_df = pd.read_csv('csv/cleaned_players_stats.csv')
print(stats_df)


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
            "INSERT INTO PlayerStats (player_id, statistic, value, year) VALUES (?, ?, ?, ?)", (row['player_id'], row['statistic'], row['value'], row['year']))
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
            "INSERT INTO CareerStats (player_id, career_length, games_played, at_bats, runs, hits, doubles, triples, home_runs, grand_slams, runs_batted_in, walks, intentional_walks, strikeouts, sacrifice_hits, sacrifice_flies, hit_by_pitch, ground_into_double_play, batting_average, on_base_percentage, slugging_percentage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                row['player_id'], row['career_length'], row['games_played'], row['at_bats'], row['runs'], row['hits'],
                row['doubles'], row['triples'], row['home_runs'], row['grand_slams'], row['runs_batted_in'], row['walks'],
                row['intentional_walks'], row['strikeouts'], row['sacrifice_hits'], row['sacrifice_flies'],
                row['hit_by_pitch'], row['ground_into_double_play'], row['batting_average'],
                row['on_base_percentage'], row['slugging_percentage']
            )
        )
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
                        statistic TEXT,
                        value REAL,
                        year INTEGER,
                        FOREIGN KEY (player_id) REFERENCES Players(player_id),
                        UNIQUE (player_id, statistic, year)
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
                       grand_slams INTEGER,
                       runs_batted_in INTEGER,
                       walks INTEGER,
                       intentional_walks INTEGER,
                       strikeouts INTEGER,
                       sacrifice_hits INTEGER,
                       sacrifice_flies INTEGER,
                       hit_by_pitch INTEGER,
                       ground_into_double_play INTEGER,
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
