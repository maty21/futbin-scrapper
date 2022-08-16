import re
import string
import pandas as pd
import bs4
import cloudscraper
import time
import random
from threading import Thread
from lib.PlayerScraper import PlayerScraper
from multiprocessing.dummy import Pool
import sqlite3



class MainFlow():
    def __init__(self):
      self._scraper = cloudscraper.create_scraper(
        browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
      self._THREAD_NUMBERS =8 
      self._pool = Pool(2) 
      self._fifaKey ={'22': {'name':'FIFA22','key':'22'}}   

    def _init(self):
        # CSV Headers
        cardColumns = ['ID', 'Name', 'Rating', 'Position', 'Revision', 'Nation',
                    'Club', 'League', 'Price | PS', 'WeakFoot', 'Skill Moves',
                    'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                    'Phyiscality', 'Body Type', 'Weight', 'Height', 'WorkRate',
                    'Popularity', 'BaseStats', 'InGameStats']

        C = open('FutBin_Players_Stats_FIFA_22_FU.csv', 'w')
        C.write(','.join(cardColumns) + '\n')
        C.close()


        for key, value in self._fifaKey.items():
            id = 0
            ID = 0
            print('Doing ' + value['name'])
            FutBin = self._scraper.get('https://www.futbin.com/' + key + '/players')
            bs = bs4.BeautifulSoup(FutBin.text, 'html.parser')
            try:
                TotalPages = str(bs.findAll(
                    'li', {'class': 'page-item '})[-1].text).strip()
            except IndexError:
                TotalPages = str(bs.findAll(
                    'li', {'class': 'page-item'})[-2].text).strip()
            print('Number of pages to be parsed for FIFA '
                + key + ' is ' + TotalPages + ' Pages')
            self._fifaKey[key]['totalPages'] = TotalPages

    def _scrappingWorker(self,pageNumber):
        key ='22'
        print(f'scrapping page: {pageNumber}')
        p = self._scraper.get('https://www.futbin.com/'
                                    + key + '/players?page=' + str(pageNumber))
                # Random Number Between Range To Be Used As Delay
        delay = random.randint(3, 10)
        ps  = PlayerScraper()
        Card = ps.pageParser(page=p)
        if not Card:
            self._scrappingWorker(pageNumber)    
        else:
        #Cards.append(Card)
            time.sleep(delay)
            return Card

    def _reconcile(self,pagesAmount=0,key=0):
           # Cards = []
            Cards = self._pool.map(self._scrappingWorker,range(int(pagesAmount)))
            # Looping On All Pages
            # while pagesAmount>0:
            
             #   threads = [Thread(target=self._scrapping,args=[tn,Cards]) for tn in range(self._THREAD_NUMBERS)]
              #  [t.start() for t in threads]
            #    [print(t.is_alive()) for t in threads]
            #    [t.join() for t in threads]
            df = pd.DataFrame(Cards)
            df.to_csv('./output/FutBin_Players_Stats_FIFA_22.csv', mode='a',
                        header=False, sep=',', encoding='utf-8', index=False)

    def Start(self):
        self._init();
        for fifaPages in self._fifaKey:
            self._reconcile(self._fifaKey[fifaPages]['totalPages'],self._fifaKey[fifaPages]['key'])
    
    def csvToObj(self):
        flatCards = []
        cardColumns = ['ID', 'Name', 'Rating', 'Position', 'Revision', 'Nation',
                    'Club', 'League', 'Price | PS', 'WeakFoot', 'Skill Moves',
                    'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                    'Phyiscality', 'Body Type', 'Weight', 'Height', 'WorkRate',
                    'Popularity', 'BaseStats', 'InGameStats']

        C = open('./output/FutBin_Players_Stats_FIFA_22_flat.csv', 'w')
        C.write(','.join(cardColumns) + '\n')
        C.close()
        df=  pd.read_csv('./output/FutBin_Players_Stats_FIFA_22_full.csv')
        cards = df.values.tolist()
        for c in cards:
            for r in c:
                if r==r: 
                    obj= list(r.replace("[","").replace("]", "").replace("\\", "").split(","))
                    flatCards.append(obj)
        df = pd.DataFrame(flatCards) 
        df.to_csv('./output/FutBin_Players_Stats_FIFA_22_flat.csv', mode='a',
                        header=False, sep=',', encoding='utf-8', index=False)
    
    def createDbFromCsv(self):
        conn = sqlite3.connect('./db/players.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE players (ID string,Name string,Rating string,Position string,Revision string,Nation string,
                  Club string,League string,PriceVsPS string,
                  WeakFoot string,SkillMoves string,Pace string,Shooting string,Passing string,Dribbling string,Defending string,Phyiscality string,
                  BodyType string,Weight string,Height string,WorkRate string,Popularity string,BaseStats string,InGameStats string)''')
        c = conn.cursor()
        players = pd.read_csv('./output/FutBin_Players_Stats_FIFA_22_flat.csv')
        players.to_sql('players', conn, if_exists='append', index = False)  
                 
       
       
mf = MainFlow()
#mf.Start()
mf.createDbFromCsv()