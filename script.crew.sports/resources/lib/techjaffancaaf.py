import requests
import re
from bs4 import BeautifulSoup
import sys

game_list = []
def get_games():
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    html = requests.get('http://crackstreams.com/cfbstreams/',headers={'user-agent':agent})
    soup = BeautifulSoup(html.content,'html.parser')
    a = soup.find_all('a',class_={'btn btn-default btn-lg btn-block'})
    for data in a:
        title = data.find('h4',class_={'media-heading'}).text
        title = title.encode('ascii','ignore')
        title = title.decode('utf-8','ignore')
        game_list.append({'title':title})

    return game_list

#print(get_games())

stream = []

def get_stream(game):
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    html = requests.get('http://crackstreams.com/cfbstreams/',headers={'user-agent':agent})
    soup = BeautifulSoup(html.content,'html.parser')
    a = soup.find_all('a',class_={'btn btn-default btn-lg btn-block'})
    for data in a:
        title = data.find('h4',class_={'media-heading'}).text
        title = title.encode('ascii','ignore')
        title = title.decode('utf-8','ignore')
        if game in title:
            url = data['href']
            url = 'http://crackstreams.com' + url
            html = requests.get(url,headers={'user-agent':agent}).content
            soup = BeautifulSoup(html,'html.parser')
            frame = soup.find('iframe')
            if frame:
                frame = frame['src']
                source = url + frame
                master = requests.get(source,headers={'referer':url}).content
                soup = BeautifulSoup(master,'html.parser')
                m3u8 = re.compile('source: "(.+?)"',re.DOTALL).findall(str(soup.prettify))
                m3u8 = m3u8[0]
                m3u8 = m3u8 + '|referer=' + source
                stream.append({'title':title,'stream':m3u8})
                break
            else:
                break
        else:
            continue

    return stream


#print(get_stream('Rice at Army CFB streams live'))
