import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os

season = '2015'
pbp = pd.read_csv('./data/pbp_info_2015-16.csv')

for i, row in pbp[pbp['event_number'] == 0].iterrows():
    if i > 10:
        break
    
    gid = str(row['game_id'])
    date = row['event_timestamp_utc'].split()[0]
    num_periods = pbp[pbp['game_id'] == int(gid)]['period'].max()
    month = date.split('-')[1]
    url = 'http://stats.inpredictable.com/nba/wpBox.php?season=' + season + '&month=' + month + '&date=' + date + '&gid=00' + gid
    
    print(url)

    browser = webdriver.Chrome('./chromedriver.exe')
    browser.get(url)
    html_source = browser.page_source  
    browser.quit()

    soup = BeautifulSoup(html_source, 'html.parser')

    team_name = soup.find('text', {'x': '54'}).text[-4:-1]
    # print(soup.find('td', {'onmouseover': 'tooltip.show(dMVP)'}).find_next_sibling('td').text)
    # print(soup.find('td', {'onmouseover': 'tooltip.show(dLVP)'}).find_next_sibling('td').text)

    # x range: 45.5 - 865.5
    # y range: 20.5 - 380.5
    x_max = 854.5
    x_min = 45.5
    y_max = 380.5
    y_min = 20.5
    total_seconds = (48 + (num_periods - 4) * 5) * 60

    chart_data = soup.find('path', {'fill-opacity': '1'})['d'][1:].split('L')
    chart_data = [(float(x.split(',')[0]), float(x.split(',')[1])) for x in chart_data]

    win_perct = []
    for x, y in chart_data:
        cur_win_perct = (y_max - y) / (y_max - y_min)
        cur_time = (x_max - x) / (x_max - x_min)
        cur_time = total_seconds - total_seconds * cur_time
        win_perct.append((cur_time, cur_win_perct))

    df = pd.DataFrame(win_perct)
    df.columns = ['time', 'win_prob']
    df.to_csv('./win_prob/' + season + '/' + gid + '_' + team_name + '.csv', index=False)
