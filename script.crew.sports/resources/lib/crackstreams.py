import requests
from bs4 import BeautifulSoup
import re
game_list = []

def get_game():
    conn = requests.get(r"http://192.243.100.207/streams/crackstreams/crackstreams.xml")
    title = re.compile("<title>(.+?)</title>").findall(conn.text)
    link = re.compile("<link>(.+?)</link>").findall(conn.text)
    i = 0
    if title or link:
        while i < len(title):
            if 'nfl' in title[i].encode('ascii','ignore').lower():
                i += 1
                continue
                
            game_list.append({'title':title[i].encode('ascii','ignore'),'stream':link[i].encode('ascii','ignore').replace('Referer','referer')})
            i += 1
    else:
        pass

    return game_list


print(get_game())
    
