import re
import pandas as pd
import bs4
import cloudscraper
import time
import random
from lib.PlayerScraper import PlayerScraper

fifa = {'22': 'FIFA22'}     # Store Key

# CSV Headers
cardColumns = ['ID', 'Name', 'Rating', 'Position', 'Revision', 'Nation',
               'Club', 'League', 'Price | PS', 'WeakFoot', 'Skill Moves',
               'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
               'Phyiscality', 'Body Type', 'Weight', 'Height', 'WorkRate',
               'Popularity', 'BaseStats', 'InGameStats']

C = open('FutBin_Players_Stats_FIFA_22_FU.csv', 'w')
C.write(','.join(cardColumns) + '\n')
C.close()

scraper = cloudscraper.create_scraper(
    browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})

for key, value in fifa.items():
    id = 0
    ID = 0
    print('Doing ' + value)
    FutBin = scraper.get('https://www.futbin.com/' + key + '/players')
    bs = bs4.BeautifulSoup(FutBin.text, 'html.parser')
    try:
        TotalPages = str(bs.findAll(
            'li', {'class': 'page-item '})[-1].text).strip()
    except IndexError:
        TotalPages = str(bs.findAll(
            'li', {'class': 'page-item'})[-2].text).strip()
    print('Number of pages to be parsed for FIFA '
          + key + ' is ' + TotalPages + ' Pages')
    # Looping On All Pages
    for page in range(1, int(TotalPages) + 1):
        p = scraper.get('https://www.futbin.com/'
                             + key + '/players?page=' + str(page))
        # Random Number Between Range To Be Used As Delay
        delay = random.randint(15, 60)
        ps  = PlayerScraper()
        Card = ps.pageParser(page=p)
        #   id += 1

        df = pd.DataFrame(Card)
        df.to_csv('./output/FutBin_Players_Stats_FIFA_22.csv', mode='a',
                  header=False, sep=',', encoding='utf-8', index=False)

        # Adding Some Random Time Delay
        print("Sleeping for", delay, "Seconds")
        time.sleep(delay)
