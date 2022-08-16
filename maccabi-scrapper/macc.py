from time import sleep
from pyquery import PyQuery as pq
import bs4
import cloudscraper

class MaccabiHaifaScrapper():



    def __init__(self) -> None:
        self.scraper = cloudscraper.create_scraper(
        browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
        self._ack = False
        self.setCookie= """QueueITAccepted-SDFrts345E-V3_generalmhaifafc=EventId%3dgeneralmhaifafc%26QueueId%3d2ba7ce9b-0722-44f5-a6d9-f416a30f0333
        %26RedirectType%3dqueue%26IssueTime%3d1660652712%26Hash%3d36e25b8c80c7b7de02a066991481a4e4845b27b750d3a59c92eb835bb20ea1b7;
         expires=Wed, 17-Aug-2022 12:25:12 GMT;
          path=/;
         secure; HttpOnly"""
        self.Cookie = """ASP.NET_SessionId_=xkz1dgw204lcbc14t505a4uk;_gid=GA1.2.57691699.1660660239; QueueITAccepted-SDFrts345E-V3_generalmhaifafc=EventId%3dgeneralmhaifafc%26QueueId%3d5526123e-9fd6-427f-82f8-5253f420479c%26RedirectType%3dsafetynet%26IssueTime%3d1660661597%26Hash%3dabe0006cc3df77c40894232e164178d752bdd92ff513974df49ec2bab3a7d6f9; """

    def siteScrapper(self):
        headers= {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7",
        "cache-control": "max-age=0",
        "cookie": self.Cookie,
        "referer": "https://tickets.mhaifafc.com/crmlogin.aspx?next=loader.aspx/?target=hall.aspx%3Fevent%3D1358",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36)"
        }
        page = self.scraper.get('https://tickets.mhaifafc.com/events/maccabi%20haifa%20fc%20-%20fk%20crvena%20zvezda/2022-8-17_22.00/sammy%20ofer%20stadium?hallmap',headers=headers)
        bs = bs4.BeautifulSoup(page.text, 'html.parser')
        if page.text.find("כל הכרטיסים לאירוע נמכרו. כדאי לנסות שוב במועד אחר") != -1:
            print("not found place")
            _pq = pq(page.text)
        elif page.text.find("דף שגיאה: חנות המועדון הרישמי"):
            print("shit")
            self._ack = False
        else:
            print("yay!!!!!")
        # print(bs)

    def interval(self):
        while True:
            if self._ack is True:
                self.siteScrapper()
                sleep(5);
            else:
                sleep(1);
                
    def setAck(self,ack):
        self._ack = ack
    




mhfcScrapper = MaccabiHaifaScrapper()
mhfcScrapper.setAck(True)
mhfcScrapper.interval()


 #"cookie": "os=true; _ga=GA1.2.813905843.1659264189; _fbp=fb.1.1659264188721.1682282264; _hjSessionUser_1103037=eyJpZCI6ImJmNTlkYTNmLTQ5ZDMtNTY2NC1hNWEyLTZiNWZmMzhkYjU5ZSIsImNyZWF0ZWQiOjE2NTkyNjQxODg2MTEsImV4aXN0aW5nIjp0cnVlfQ==; glassix-visitor-id-v2-be3e0798-9e18-4774-a3ae-45ee8fcfd497=c5bf712d-912b-4b94-8c55-9335654ea577; __adroll_fpc=24afbc8526edbb092425e0a90d2874a9-1659264196537; gid=kYNZ8IGm1Eeox1aKj+7vcQ==; af=X50PtnDAhmY%3d; ASP.NET_SessionId=22hjw2hn3zttkwn2fkiyqufa; os=true; inMobile=false; rm=/; _gid=GA1.2.1916270303.1660633442; _hjSession_1103037=eyJpZCI6IjdhNTgwODZlLTI2OGYtNGQ5MC1iYWE3LWNjM2ZkMGRmYWM4MiIsImNyZWF0ZWQiOjE2NjA2MzM0NDIxNjMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; __ar_v4=GD4Z3M74TZEQVPSIUBCO7T%3A20220730%3A3%7C2NAVGF4S7NEYLN3J6J3W3E%3A20220730%3A3%7C6ZJTYIIODNE6PDLR3WOXGV%3A20220730%3A3; ASP.NET_SessionId_=1zkvoefiscpfiogpmizcol2c; crmAuth=xQPGBq2onBx1Oky5vZDfMFfniy14klADFWhQgN/FOOM=; cs=VU3xLkw8MFB6Q1xsLs7ilpjl; QueueITAccepted-SDFrts345E-V3_generalmhaifafc=EventId%3dgeneralmhaifafc%26QueueId%3d08483ebc-47c3-478a-8c38-576e59f92731%26RedirectType%3dsafetynet%26IssueTime%3d1660633755%26Hash%3de8697578845bf36bae299c14d16999d4419bf3ba310a7069812246a976443fca; AWSALB=LFdoQsBK3frM9LWqaUkZvl0E13hqk64lIgVpzzzwDUfCNVohuhyeYJDycNENe1sDUOi/3TYcql+ZOGNcO/ezLnA3o9zKruNBqVwMQ/H0aJbLI05VNVERjBfwBBoO; AWSALBCORS=LFdoQsBK3frM9LWqaUkZvl0E13hqk64lIgVpzzzwDUfCNVohuhyeYJDycNENe1sDUOi/3TYcql+ZOGNcO/ezLnA3o9zKruNBqVwMQ/H0aJbLI05VNVERjBfwBBoO",
       

 #       "cookie": "os=true; _ga=GA1.2.813905843.1659264189;
 #  _fbp=fb.1.1659264188721.1682282264;
 #  _hjSessionUser_1103037=eyJpZCI6ImJmNTlkYTNmLTQ5ZDMtNTY2NC1hNWEyLTZiNWZmMzhkYjU5ZSIsImNyZWF0ZWQiOjE2NTkyNjQxODg2MTEsImV4aXN0aW5nIjp0cnVlfQ==; 
 # glassix-visitor-id-v2-be3e0798-9e18-4774-a3ae-45ee8fcfd497=c5bf712d-912b-4b94-8c55-9335654ea577;
 #  __adroll_fpc=24afbc8526edbb092425e0a90d2874a9-1659264196537; gid=kYNZ8IGm1Eeox1aKj+7vcQ==; 
 # af=X50PtnDAhmY%3d; ASP.NET_SessionId=22hjw2hn3zttkwn2fkiyqufa; os=true; inMobile=false; rm=/;
 #  _gid=GA1.2.1916270303.1660633442; 
 # _hjSession_1103037=eyJpZCI6IjdhNTgwODZlLTI2OGYtNGQ5MC1iYWE3LWNjM2ZkMGRmYWM4MiIsImNyZWF0ZWQiOjE2NjA2MzM0NDIxNjMsImluU2FtcGxlIjpmYWxzZX0=;
 #  _hjAbsoluteSessionInProgress=0; 
 # __ar_v4=GD4Z3M74TZEQVPSIUBCO7T%3A20220730%3A3%7C2NAVGF4S7NEYLN3J6J3W3E%3A20220730%3A3%7C6ZJTYIIODNE6PDLR3WOXGV%3A20220730%3A3; 
 # ASP.NET_SessionId_=1zkvoefiscpfiogpmizcol2c; crmAuth=xQPGBq2onBx1Oky5vZDfMFfniy14klADFWhQgN/FOOM=;
 #  cs=VU3xLkw8MFB6Q1xsLs7ilpjl;
 #  QueueITAccepted-SDFrts345E-V3_generalmhaifafc=EventId%3dgeneralmhaifafc%26QueueId%3d08483ebc-47c3-478a-8c38-576e59f92731%26RedirectType%3dsafetynet%26IssueTime%3d1660633755%26Hash%3de8697578845bf36bae299c14d16999d4419bf3ba310a7069812246a976443fca; 
 # AWSALB=LFdoQsBK3frM9LWqaUkZvl0E13hqk64lIgVpzzzwDUfCNVohuhyeYJDycNENe1sDUOi/3TYcql+ZOGNcO/ezLnA3o9zKruNBqVwMQ/H0aJbLI05VNVERjBfwBBoO;
 #  AWSALBCORS=LFdoQsBK3frM9LWqaUkZvl0E13hqk64lIgVpzzzwDUfCNVohuhyeYJDycNENe1sDUOi/3TYcql+ZOGNcO/ezLnA3o9zKruNBqVwMQ/H0aJbLI05VNVERjBfwBBoO",
