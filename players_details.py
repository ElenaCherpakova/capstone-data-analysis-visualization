from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd
import csv
import traceback
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Enable headless mode
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=options)

playes_df = pd.read_csv('csv/cleaned_players.csv')
unique_player_ids = playes_df['Player_ID'].unique()


def scrap_player_stats(player_id):
    url = f"https://www.baseball-almanac.com/players/player.php?p={player_id}"
    driver.get(url)
    time.sleep(2)
    title = driver.title
    print(f"Title: {title}")
    try:
        tables = driver.find_elements(By.CSS_SELECTOR, "div.ba-table")

        third_table = tables[2]
        rows = third_table.find_elements(By.TAG_NAME, "tr")
        second_last_row = rows[-2]

        year_data = second_last_row.find_element(
            By.CSS_SELECTOR, 'td.datacolBox.center span.colspan3')
        career_year = year_data.text.strip().split()[0]

        stat_cell = second_last_row.find_elements(
            By.CSS_SELECTOR, "td.datacolBox.right")
        stat_values = [cell.text.replace(',', '') for cell in stat_cell]

        stat_headers = [
            "G", "AB", "R", "H", "2B", "3B", "HR", "GRSL", "RBI",
            "BB", "IBB", "SO", "SH", "SF", "HBP", "GIDP", "AVG", "OBP", "SLG"
        ]

        if len(stat_values) != len(stat_headers):
            print(f"mismatch between stat and headers for player")
            return None
        player_state = {
            'Player_ID': player_id,
            "Career_Length": career_year
        }
        for stat, value in zip(stat_headers, stat_values):
            player_state[stat] = value

        return player_state

    except Exception as e:
        print(f"Error scraping with ID {player_id}: {e}")
        return None


player_data = []
print(player_data)
try:
    for player_id in unique_player_ids:
        stats = scrap_player_stats(player_id)
        if stats:
            player_data.append(stats)
        time.sleep(3)
except Exception as e:
    print("could't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()


players_stat_df = pd.DataFrame(player_data)
print(players_stat_df)


try:
    with open('csv/players_stats.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(players_stat_df.columns)
        for row in players_stat_df.itertuples(index=False):
            writer.writerow(row)
except Exception as e:
    print(f"An error occurred while saving as CSV: {e}")
    traceback.print_exc()
