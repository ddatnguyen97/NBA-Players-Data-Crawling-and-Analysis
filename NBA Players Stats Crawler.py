from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

driver_path = "D:\chromedriver-win32\chromedriver-win32\chromedriver.exe"
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

url = "https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season&PerMode=Totals"
driver.get(url)

def scrape_headers():
    headers = []
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Crom_headers__mzI_m")))
    
    header_cells = table.find_elements(By.CSS_SELECTOR, "thead th")
    headers = [cell.text for cell in header_cells]
    return headers[:30]

def scrape_stats():
    player_stats = []
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Crom_body__UYOcU")))

    rows_data = table.find_elements(By.CSS_SELECTOR, "tr")
    for row in rows_data:
        data = row.find_elements(By.CSS_SELECTOR, "td")
        if data:
            data = [item.text for item in data]
            player_stats.append(data)
    return player_stats

def scrape_all_pages():
    all_player_stats = []

    while True:
        player_stats = scrape_stats()
        all_player_stats.extend(player_stats)

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Pagination_button__sqGoH[data-pos='next']"))
            )
            if next_page_button.is_enabled():
                driver.execute_script("arguments[0].click();", next_page_button)
            else:
                break  
        except NoSuchElementException:
            break  

    return all_player_stats

headers = scrape_headers()
all_player_stats = scrape_all_pages()

df = pd.DataFrame(all_player_stats, columns=headers)
print(df)

df.to_csv("NBA Players Season 23 - 24 Stats.csv", index=False)
driver.quit()