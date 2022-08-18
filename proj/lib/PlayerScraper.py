print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from time import sleep
import bs4
import re
import asyncio
from pyquery import PyQuery as pq
class PlayerScraper:
    def __init__(self):
        pass
    
    def _playerScraper(self,cardDetails):
        try:
           
            playerId = cardDetails.find('a')['href'].split('/')[3]
            clubs = cardDetails.find('span', 'players_club_nation').findAll('a')
            # Getting Clubs Information
            club = clubs[0]['data-original-title'].replace('Icons', 'unknown').strip()
            # Getting Nation Information
            nation = clubs[1]['data-original-title'].replace('Icons', 'unknown').strip()
            # Getting League Information
            league = clubs[2]['data-original-title'].strip()
            name = str(cardDetails.text).strip().replace('\n', ' ').split('           ')[0]
            cardDetails = str(cardDetails.text).strip().replace('\n', ' ').replace(' \\ ', '\\').replace(
                        ' | ', '|').split('       ')[1]
            # Getting Work Rate W/R
            workRate = re.search(r'\w\\\w', cardDetails,re.IGNORECASE).group(0)
            # Removing workRate From cardDetails
            cardDetails = re.sub(r'\w\\\w', '', cardDetails)
            # Getting Height CM|Feet'Inch"
            matchHeight = re.search(r'\w+\|\d\'\d+\"', cardDetails, re.IGNORECASE).group(0)
            # Removing matchHeight From cardDetails
            cardDetails = re.sub(r'\w+\|\d\'\d+\"', '', cardDetails)

            # Getting Player Preffered Position
            position = re.findall(r'\s(\D*\s\D+)',cardDetails, re.IGNORECASE)[1].split()[0]
            # Removing position From cardDetails
            cardDetails = re.sub(str(position), '', cardDetails)

            # Getting Player Card Revision
            revision = re.findall(
                r'\s(\D*\s\D+)', cardDetails, re.IGNORECASE)[1].split()
            # Some revision Have Differnt Dimention, Joining Those
            revision = (' '.join(revision))     # Now a String
            # Removing revision From cardDetails
            cardDetails = re.sub(revision, '', cardDetails)

            # Getting Body Type
            bodyType = re.search(r'\s{6}(\w.+?)\s{2}', cardDetails)
            # Some Data Missing, So Fail Safe
            if bodyType is None:
                bodyType = 'No Data'      # Continue Loop
            else:
                bodyType = bodyType.group(1)
            # Removing bodyType From cardDetails, Some Lines  Conatins Extra
            # Character. This '.+?' Used as Wild Card
            cardDetails = re.sub((bodyType + '.+?'), '', cardDetails)

            # Getting Weight
            weight = re.search(r'\((\w.+)\)', cardDetails)
            # Some Data Missing, So Fail Safe
            if weight is None:
                weight = 'No Data'      # Continue Loop
            else:
                weight = weight.group(1)
            # Removing weight Form cardDetails while adding '()'
            cardDetails = re.sub((r'\(' + weight + r'\)'), '', cardDetails)

            # Splitting Rest of Details
            cardDetails = cardDetails.split()
            # Insert Tables At Proper ID
            cardDetails.insert(0, playerId)
            cardDetails.insert(1, name)
            cardDetails.insert(3, position)
            cardDetails.insert(4, revision)
            cardDetails.insert(5, nation)
            cardDetails.insert(6, club)
            cardDetails.insert(7, league)
            cardDetails.insert(17, bodyType)
            cardDetails.insert(18, weight)
            cardDetails.insert(19, matchHeight)
            cardDetails.insert(20, workRate)
            return cardDetails;
        except Exception as e:
            print(f'error on player parsing: {e}')
            return []

    def pageParser(self,page):
        try:
            _pq = pq(page.text)
            bs = bs4.BeautifulSoup(page.text, 'html.parser')
            table = bs.find('table', {'id': 'repTb'})
            tbody = table.find('tbody')
            extracted = tbody.findAll('tr', {'class': re.compile('player_tr_\\d')})
            Card = []
            for cardDetails in extracted:
                cd=  self._playerScraper(cardDetails=cardDetails)
                if len(cd)>0:
                    Card.append(cd)
 #               print(cd)
            sleep(10)
            return Card
        except:
            sleep(60)
            return None