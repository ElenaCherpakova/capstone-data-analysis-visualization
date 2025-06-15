import streamlit as st
import pandas as pd
import altair as alt

players_fd = pd.read_csv('csv/cleaned_players.csv')
career_fd = pd.read_csv("csv/players_stats.csv")
players_fd["Year"] = players_fd["Year"].astype(int)
career_fd["Career_Length"] = career_fd["Career_Length"].astype(int)
player_ids = players_fd[['Player_ID', 'Name']].drop_duplicates()
career_fd = career_fd.merge(player_ids, on="Player_ID", how="left")

player_dict = player_ids.set_index('Player_ID')['Name'].to_dict()

teams = sorted(players_fd['Team'].dropna().unique())

st.title("""⚾️  Explore The History of the American Baseball League From 2000 to 2024""")
st.sidebar.title('Filter:')

year_selected = st.sidebar.slider("⏳ Select a year:",
                                  min_value=int(players_fd['Year'].min()),
                                  max_value=int(players_fd['Year'].max()),
                                  value=2012,
                                  step=1)



select_player_id = st.sidebar.selectbox("🧢 **Choose a player:** ",
                                        options=player_dict.keys(),
                                        format_func=lambda pid: player_dict[pid])

team_selected = st.sidebar.selectbox("⚾️⚾️ **Choose a team:**",
                                        options=teams)
selected_columns = ['Name', 'Team', 'Statistic', 'Value', 'Year']
selected_columns_for_team = ['Name', 'Year']
player_df = players_fd[players_fd['Player_ID'] == select_player_id][selected_columns]
year_df = players_fd[players_fd['Year'] == year_selected][selected_columns]
team_df = players_fd[players_fd['Team'] == team_selected][selected_columns_for_team]
team_data_df = team_df.drop_duplicates().sort_values(by=['Name', 'Year'])
st.subheader(f"Year in review: **{year_selected}** American League", divider=True)
st.dataframe(year_df, hide_index=True)

st.subheader(f"Baseball Stats for **{player_dict[select_player_id]}**", divider=True)
st.dataframe(player_df, hide_index=True)
st.subheader(f"Team in review: **{team_selected}**", divider=True)
st.dataframe(team_data_df, hide_index=True)

avg_career_length = career_fd['Career_Length'].mean()
col1, col2= st.columns(2)
with col1:
    st.subheader("Distribution of Career Lengths")
with col2:
    st.metric("📊 Average Career Length", f"{avg_career_length:.1f} years")
   
   
col1, col2 = st.columns(2, gap='large') 

with col1:
    chart = alt.Chart(career_fd).mark_bar().encode(
        alt.X("Career_Length:Q", bin=alt.Bin(step=1), title="Career Length (years)",  axis=alt.Axis(format="d")),
        y='count()',
    )
    st.altair_chart(chart)
with col2:
    top_3_career = career_fd.sort_values('Career_Length', ascending=False).head(3)
    st.subheader("🏆 Top 3 Players with the Longest Careers")
    st.dataframe(top_3_career[['Name', 'Career_Length']], hide_index=True)


