import pandas as pd

raw_player_stats = pd.read_csv('csv/players_stats.csv')

# Rename columns for clarity
players_stat_df_cleaned = raw_player_stats.rename(columns={
    "G": "games_played",
    "AB": "at_bats",
    "R": "runs",
    "H": "hits",
    "2B": "doubles",
    "3B": "triples",
    "HR": "home_runs",
    "GRSL": "grand_slams",
    "RBI": "runs_batted_in",
    "BB": "walks",
    "IBB": "intentional_walks",
    "SO": "strikeouts",
    "SH": "sacrifice_hits",
    "SF": "sacrifice_flies",
    "HBP": "hit_by_pitch",
    "GIDP": "ground_into_double_play",
    "AVG": "batting_average",
    "OBP": "on_base_percentage",
    "SLG": "slugging_percentage"
})

players_stat_df_cleaned.to_csv('csv/cleaned_players_stats.csv', index=False)
