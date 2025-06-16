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


def scraper_player(year):
    url = f"https://www.baseball-almanac.com/yearly/yr{year}a.shtml"
    driver.get(url)
    title = driver.title
    print(f"Title: {title}")

    first_table = driver.find_elements(
        By.CSS_SELECTOR, "table.boxed")[0]
    rows = first_table.find_elements(By.TAG_NAME, "tr")
    players = []
    last_stat_name = None
    last_stat_value = None
    for row in rows:
        try:
            stats_cells = row.find_elements(By.CSS_SELECTOR, "td.datacolBlue")
            data_cells = row.find_elements(
                By.XPATH, ".//td[contains(@class, 'datacolBox')]")

            if stats_cells:
                last_stat_name = stats_cells[0].text.strip()
                last_stat_value = data_cells[2].text.strip() if len(
                    data_cells) > 2 else ''
            if len(data_cells) >= 2:
                anchor_tag = data_cells[0].find_element(By.TAG_NAME, "a")
                href = anchor_tag.get_attribute("href")
                player_id = href.split("p=")[-1] if "p=" in href else None
                player_name = data_cells[0].text.strip()
                player_team = data_cells[1].text.strip()
                players.append({
                    "Player_ID": player_id,
                    "Name": player_name,
                    "Team": player_team,
                    "Statistic": last_stat_name,
                    "Value": last_stat_value,
                    "Year": year
                })

        except Exception as e:
            print(f"An error occurred while processing the list item: {e}")
            traceback.print_exc()
            continue
    return players


all_players = []
start_year = 2000
end_year = 2024
try:
    for year in range(start_year, end_year + 1):
        players = scraper_player(year)
        all_players.extend(players)
        time.sleep(3)
except Exception as e:
    print("could't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()


players_df = pd.DataFrame(all_players)
print(players_df)


try:
    players_df.to_csv('csv/players.csv', index=False)   
except Exception as e:
    print(f"An error occurred while saving as CSV: {e}")
    traceback.print_exc()
