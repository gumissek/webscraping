import time

import pandas
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

URL = 'https://steamdb.info/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
table_most_played_games = driver.find_element(By.CLASS_NAME, value='table-products')
most_played = table_most_played_games.find_element(By.TAG_NAME, value='a')
most_played.click()

table_games = driver.find_element(By.CLASS_NAME, value='table-products')
first_game = table_games.find_elements(By.TAG_NAME, value='td')[1].find_element(By.TAG_NAME, value='a')
first_game.click()
time.sleep(1)

try:
    monthly_table = driver.find_element(By.XPATH,
                                        '/html/body/div[4]/div/div/div[2]/div/div[2]/div[4]/div[5]/div/div/table')
except selenium.common.exceptions.NoSuchElementException:
    print('Cant find an element.')
else:

    monthly_table_headers = monthly_table.find_elements(By.TAG_NAME, value='th')[:4]
    monthly_table_body = monthly_table.find_element(By.CLASS_NAME, value='tabular-nums')

    table_rows = monthly_table_body.find_elements(By.TAG_NAME, value='tr')

    columns = [header.text for header in monthly_table_headers]
    df = pandas.DataFrame(columns=columns)

    for row in table_rows:
        td_s = row.find_elements(By.TAG_NAME, value='td')
        time = td_s[0].text
        peak = td_s[1].text.replace(',', '')
        gain_dbd = td_s[2].text
        gain_dbd_proc = td_s[3].text
        data = [{monthly_table_headers[0].text: time, monthly_table_headers[1].text: int(peak),
                 monthly_table_headers[2].text: gain_dbd,
                 monthly_table_headers[3].text: gain_dbd_proc}]
        new_row = pandas.DataFrame(data)
        df = pandas.concat([df, new_row], ignore_index=True)
    df.to_csv('most_popular_game_stats.csv', index=False)

driver.quit()
