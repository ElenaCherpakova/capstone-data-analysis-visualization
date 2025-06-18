from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import traceback


options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Enable headless mode
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=options)

players_df = pd.read_csv('../clean_data/players.csv')
unique_player_ids = players_df['player_id'].unique()


def scrap_player_stats(player_id):
    url = f"https://www.baseball-almanac.com/players/player.php?p={player_id}"
    driver.get(url)
    title = driver.title
    print(f"Title: {title}")
    
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.ba-table")) >= 3)
        tables = driver.find_elements(By.CSS_SELECTOR, "div.ba-table")
        third_table = tables[2]
        rows = third_table.find_elements(By.TAG_NAME, "tr")
        if len(rows) < 2:
            print(f"Not enough rows found for player {player_id}")
            return None
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
            'player_id': player_id,
            "career_length": career_year
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
except Exception as e:
    print("could't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()

players_stat_df = pd.DataFrame(player_data)


try:
    players_stat_df.to_csv('../raw_data/players_career_stats.csv', index=False)
except Exception as e:
    print(f"An error occurred while saving as CSV: {e}")
    traceback.print_exc()
