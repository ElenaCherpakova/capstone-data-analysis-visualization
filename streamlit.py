import streamlit as st
import pandas as pd

players_fd = pd.read_csv('csv/cleaned_players.csv')
player_ids = players_fd[['Player_ID', 'Name']].drop_duplicates()
player_ids_sorted = player_ids.sort_values('Player_ID')
player_dict = player_ids_sorted.set_index('Player_ID')['Name'].to_dict()
print(player_dict)

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

selected_columns = ['Name', 'Team', 'Statistic', 'Value', 'Year']

player_data = players_fd[players_fd['Player_ID'] == select_player_id]
player_df_display = player_data[selected_columns]
year_df = players_fd[players_fd['Year'] == year_selected]
st.subheader(f"Year in review: **{year_selected}** American League", divider=True)
st.dataframe(year_df, hide_index=True)

player_name = player_dict.get(select_player_id)
st.subheader(f"Baseball Stats for **{player_name}**", divider=True)
st.dataframe(player_df_display, hide_index=True)