import streamlit as st
import pandas as pd

players_fd = pd.read_csv('csv/cleaned_players.csv')
player_ids = players_fd[['Player_ID', 'Name']].drop_duplicates()
team_ids = players_fd[['Player_ID', 'Team']].drop_duplicates()
player_ids_sorted = player_ids.sort_values('Player_ID')
player_dict = player_ids_sorted.set_index('Player_ID')['Name'].to_dict()

teams = sorted(players_fd['Team'].dropna().unique())


print(teams)

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
selected_columns_for_team = ['Name', 'Team', 'Year']
player_df = players_fd[players_fd['Player_ID'] == select_player_id][selected_columns]
year_df = players_fd[players_fd['Year'] == year_selected][selected_columns]
team_df = players_fd[players_fd['Team'] == team_selected][selected_columns_for_team].drop_duplicates().sort_values(by=['Name', 'Year'])
st.subheader(f"Year in review: **{year_selected}** American League", divider=True)
st.dataframe(year_df, hide_index=True)

player_name = player_dict.get(select_player_id)
st.subheader(f"Baseball Stats for **{player_name}**", divider=True)
st.dataframe(player_df, hide_index=True)
st.subheader(f"Team in review: **{team_selected}**", divider=True)
st.dataframe(team_df, hide_index=True)
