import streamlit_dash as st
import pandas as pd
import altair as alt

# Load and prepare data
players_fd = pd.read_csv('clean_data/players.csv')
career_fd = pd.read_csv('clean_data/players_career_stats.csv')

# Merge player names into career stats
player_ids = players_fd[['player_id', 'name']].drop_duplicates()
career_fd = career_fd.merge(player_ids, on="player_id", how="left")

year_range = st.slider(
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

st.title("⚾️ Explore The History of the Baseball League (2000-2024)")
st.markdown("")

leagues = sorted(players_fd['league'].dropna().unique())
league_selected = st.selectbox("🥎⚾️ **Choose a league**:", ["All Leagues"] + leagues)

if league_selected != "All Leagues":
    filtered_teams = sorted(players_by_year[players_by_year['league'] == league_selected]['team'].dropna().unique())
else: 
    filtered_teams = sorted(players_by_year['team'].dropna().unique())

team_selected = st.selectbox("⚾️ **Choose a team**:", ["All Teams"] + filtered_teams)

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

st.subheader("Batting Average Distribution")
bat_avg_hist = alt.Chart(career_filtered).mark_bar().encode(
    alt.X('batting_average', bin=alt.Bin(step=0.01), title='Batting Average'),
    y='count()'
).properties(width=600, height=300)
st.altair_chart(bat_avg_hist, use_container_width=True)

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
    st.markdown(f"**Filters:** Years from {year_range[0]} to {year_range[1]}, Leagues: {league_selected}")

step = 2
years = list(range(career_length_year['year'].min(), career_length_year['year'].max() + 1, step))

avg_career_per_year = career_length_year.groupby('year')['career_length'].mean().reset_index()

career_length_chart = alt.Chart(avg_career_per_year).mark_line(point=True).encode(
    x=alt.X('year:O', axis=alt.Axis(values=years, title='Year')),
    y=alt.Y('career_length', title='Average Career Length (years)')
).properties(width=700, height=300)
st.altair_chart(career_length_chart, use_container_width=True)
