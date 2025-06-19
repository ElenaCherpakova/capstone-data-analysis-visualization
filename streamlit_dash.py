import streamlit as st
import pandas as pd
import altair as alt

# Load and prepare data
players_fd = pd.read_csv('clean_data/players.csv')
career_fd = pd.read_csv('clean_data/players_career_stats.csv')

# Merge player names into career stats
player_ids = players_fd[['player_id', 'name']].drop_duplicates()
career_fd = career_fd.merge(player_ids, on="player_id", how="left")

st.title("The History of the Baseball League")
st.markdown("⚾️ **Explore** career statistics, player performance trends, and league data from **2000–2024**")
st.sidebar.markdown("🔍 Use the sidebar filters to refine your view and dive deep into the numbers!")

year_range = st.sidebar.slider(
    "⏳ Select a year range:",
    int(players_fd['year'].min()),
    int(players_fd['year'].max()),
    (2006, 2020),
    1
)
# Filter players by year range
players_by_year = players_fd[
    (players_fd['year'] >= year_range[0]) &
    (players_fd['year'] <= year_range[1])
]
career_filtered = career_fd.copy()
players_filtered = players_by_year.copy()

leagues = sorted(players_fd['league'].dropna().unique())
league_selected = st.sidebar.selectbox("🥎⚾️ **Choose a league**:", ["All Leagues"] + leagues)

if league_selected != "All Leagues":
    filtered_teams = sorted(players_by_year[players_by_year['league'] == league_selected]['team'].dropna().unique())
else: 
    filtered_teams = sorted(players_by_year['team'].dropna().unique())

team_selected = st.sidebar.selectbox("⚾️ **Choose a team**:", ["All Teams"] + filtered_teams)

if league_selected != "All Leagues":
    players_filtered = players_filtered[players_filtered['league'] == league_selected]
    career_filtered = career_filtered[career_filtered['player_id'].isin(players_filtered['player_id'].unique())]

# Filter by team
if team_selected != "All Teams":
    players_filtered = players_filtered[players_filtered['team'] == team_selected]
    career_filtered = career_filtered[career_filtered['player_id'].isin(players_filtered['player_id'].unique())]

# Display section titles and filtered data
display_year = str(year_range[0]) if year_range[0] == year_range[1] else f"{year_range[0]}–{year_range[1]}"
league_label = league_selected if league_selected != "All Leagues" else "All"
st.subheader(f"**{display_year}** **{league_label}** League Player Review")

st.markdown("Hitting Statistics League Leaderboard")
leaderboard_columns = ['name', 'team', 'statistic', 'value', 'year']
df_leaderboard = players_filtered[leaderboard_columns].sort_values(by=['year', 'value'], ascending=[True, False])
st.dataframe(df_leaderboard, hide_index=True)

st.subheader("Distribution of Career Lengths")
chart_career_len = alt.Chart(career_filtered).mark_bar().encode(
    alt.X("career_length:Q", bin=alt.Bin(step=1), title="Career Length (years)", axis=alt.Axis(format="d")),
    y='count()'
)
st.altair_chart(chart_career_len, use_container_width=True)

avg_career_length = career_filtered['career_length'].mean()
st.metric("📊 Average Career Length", f"{avg_career_length:.1f} years")

top_3_career = career_filtered.sort_values('career_length', ascending=False).head(3)
st.subheader("🏆 Top 3 Players with the Longest Careers")
st.dataframe(top_3_career[['name', 'career_length']], hide_index=True)

st.subheader("Games Played vs Career Length")
scatter_games_career = alt.Chart(career_filtered).mark_circle(size=60, opacity=0.5).encode(
    x=alt.X('career_length', title='Career Length (Years)'),
    y=alt.Y('games_played', title='Total Games Played'),
    tooltip=['name', 'career_length', 'games_played']
).properties(width=600, height=400)
st.altair_chart(scatter_games_career, use_container_width=True)

st.subheader("Top 10 Players by Career Home Runs")
top_hr = career_filtered[['name', 'home_runs']].dropna().sort_values('home_runs', ascending=False).head(10)
hr_bar = alt.Chart(top_hr).mark_bar().encode(
    x=alt.X('home_runs:Q', title='Home Runs'),
    y=alt.Y('name:N', sort='-x', title=None)
).properties(width=600)
st.altair_chart(hr_bar, use_container_width=True)

st.subheader("Average Career Length Over Years")
career_length_year = players_fd.merge(career_fd[['player_id', 'career_length']], on='player_id')

# Filter merged data by year and league to keep consistent filtering on average career length over years
career_length_year = career_length_year[
    (career_length_year['year'] >= year_range[0]) & (career_length_year['year'] <= year_range[1])
]

if league_selected != "All Leagues":
    career_length_year = career_length_year[career_length_year['league'] == league_selected]


if career_length_year.empty:
    st.warning("🚨 No data.")
else:
    st.markdown(f"**Filters:** Years from {year_range[0]} to {year_range[1]}, League: {league_selected}")

step = 2
years = list(range(career_length_year['year'].min(), career_length_year['year'].max() + 1, step))

avg_career_per_year = career_length_year.groupby('year')['career_length'].mean().reset_index()

career_length_chart = alt.Chart(avg_career_per_year).mark_line(point=True).encode(
    x=alt.X('year:O', axis=alt.Axis(values=years, title='Year')),
    y=alt.Y('career_length', title='Average Career Length (years)')
).properties(width=700, height=300)
st.altair_chart(career_length_chart, use_container_width=True)


st.subheader("📈 Stat Tendency Over Years")

# Define available numeric stats
available_stats = [
    'at_bats', 'runs', 'hits',
    'doubles', 'triples', 'home_runs', 'grand_slams', 'runs_batted_in',
    'walks', 'intentional_walks', 'strikeouts', 'sacrifice_hits',
    'sacrifice_flies', 'hit_by_pitch', 'ground_into_double_play',
    'batting_average', 'on_base_percentage', 'slugging_percentage'
]

stat_options = {
    'at_bats': 'At Bats',
    'runs': 'Runs',
    'hits': 'Hits',
    'doubles': 'Doubles',
    'triples': 'Triples',
    'home_runs': 'Home Runs',
    'grand_slams': 'Grand Slams',
    'runs_batted_in': 'Runs Batted In',
    'walks': 'Walks',
    'intentional_walks': 'Intentional Walks',
    'strikeouts': 'Strikeouts',
    'sacrifice_hits': 'Sacrifice Hits',
    'sacrifice_flies': 'Sacrifice Flies',
    'hit_by_pitch': 'Hit By Pitch',
    'ground_into_double_play': 'Ground Into Double Play',
    'batting_average': 'Batting Average',
    'on_base_percentage': 'On-Base Percentage',
    'slugging_percentage': 'Slugging Percentage'
}


stat_pretty = st.sidebar.selectbox("📊 Choose a statistic to visualize trend over years:", list(stat_options.values()))
stat_selected = [key for key, val in stat_options.items() if val == stat_pretty][0]

# Prepare stat trend data
stat_data = players_fd[['player_id', 'year']].merge(
    career_fd[['player_id', stat_selected]],
    on='player_id',
    how='left'
)

# Filter by year range
stat_data = stat_data[
    (stat_data['year'] >= year_range[0]) &
    (stat_data['year'] <= year_range[1])
]

# Optional: filter by league
if league_selected != "All Leagues":
    stat_data = stat_data.merge(players_fd[['player_id', 'league']], on='player_id')
    stat_data = stat_data[stat_data['league'] == league_selected]

# Group by year and calculate average
stat_trend = stat_data.groupby('year')[stat_selected].mean().reset_index()

if stat_trend.empty:
    st.warning("🚨 No data available for this selection.")
else:
    trend_chart = alt.Chart(stat_trend).mark_line(point=True).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y(f'{stat_selected}:Q', title=f'Average {stat_options[stat_selected]}'),
        tooltip=['year', stat_selected]
    ).properties(width=700, height=300)
    
st.altair_chart(trend_chart, use_container_width=True)

st.sidebar.markdown(
    """[Source Data](https://www.baseball-almanac.com)<br>
    [GitHub Repo](https://github.com/ElenaCherpakova/capstone-data-analysis-visualization)<br>
    [Made By Elena Cherpakova](https://www.linkedin.com/in/elena-cherpakova/)""",
    unsafe_allow_html=True
)