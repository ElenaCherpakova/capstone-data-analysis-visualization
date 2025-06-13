import streamlit as st
import pandas as pd

df_year = pd.read_csv('csv/players.csv')

st.title("""⚾️  Explore The History of the American Baseball League From 2000 to 2024""")
st.sidebar.title('Filter:')

year_selected = st.sidebar.slider("⏳ Select year:", 
                                  min_value=int(df_year['Year'].min()),
                                  max_value=int(df_year['Year'].max()),
                                  value=2012,
                                  step=1)

player_name = st.sidebar.selectbox("🧢 **Choose a player:** ",
                                   sorted(df_year['Name'].unique())
                                   )

year_df = df_year['Year'] == year_selected