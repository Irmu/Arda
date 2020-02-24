import requests
import re
from bs4 import BeautifulSoup
import sys
from resources.lib import cfscrape
#import xbmcgui

agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

game_list = []

def get_games():
    scraper = cfscrape.create_scraper()
    html = scraper.get('http://www.streameast.live/nhl-streams/',headers={'user-agent':agent}).content
    soup = BeautifulSoup(html,'html.parser')
    a = soup.find_all('div',class_={'col-md-3 col-xs-7 padding-null text-left'})
    for data in a:
        title = data.find('div',class_={'team'}).text
        game_list.append({'title':title.encode('ascii','ignore').decode('utf-8','ignore')})

    return game_list

#print(get_games())

stream = []

def get_stream(game):
    scraper = cfscrape.create_scraper()
    html = scraper.get('http://www.streameast.live/nhl-streams/',headers={'user-agent':agent}).content
    soup = BeautifulSoup(html,'html.parser')
    a = soup.find_all('div',class_={'col-md-3 col-xs-7 padding-null text-left'})
    for data in a:
        title = data.find('div',class_={'team'}).text
        href = data.a['href']
        #print(title,href)
        #xbmcgui.Dialog().textviewer('Error', str(data))
        if game in title:
            url = href
            html = scraper.get(url,headers={'user-agent':agent}).content
            soup = BeautifulSoup(html,'html.parser')
            frame = soup.find('iframe')
            if frame:
                frame = frame['src']
                master = scraper.get(frame,headers={'referer':url}).content
                soup = BeautifulSoup(master,'html.parser')
                m3u8 = re.compile('source: "(.+?)"',re.DOTALL).findall(str(soup.prettify))
                m3u8 = m3u8[0]
                m3u8 = m3u8 +  '|User-Agent=' + agent +'&Referer=' + frame
                stream.append({'title':title,'stream':m3u8})
                break
            else:
                break
        else:
            continue

    return stream


#print(get_stream('FINALLY'))
