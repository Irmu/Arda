# -*- coding: utf-8 -*-
import re
import unicodedata
import json
import xbmc
from resources.lib.modules import client

tmdb_api = '1e7b47249796f50c0b783fcdcbcfa8ba'

def tmdb_id(imdb):
	url = 'https://api.themoviedb.org/3/find/%s?api_key=%s&language=en-US&external_source=imdb_id' % (imdb, tmdb_api)
	r = client.request(url)
	match = re.compile('"id":(.+?),').findall(r)
	for tmdb in match:
		return tmdb

def imdb_mv(tmdb):
	import xbmcgui
	
	url = 'https://api.themoviedb.org/3/movie/%s/external_ids?api_key=%s' % (tmdb, tmdb_api)
	r = client.request(url)
	i = re.compile('"imdb_id":"(.+?)"').findall(r)
	for imdb in i:
		return imdb

def runtime_mv(tmdb):
	url = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=en-US' % (tmdb, tmdb_api)
	r = client.request(url)
	i = re.compile('"runtime":(.+?),').findall(r)
	for duration in i:
		return duration

def rating(imdb):
	url = 'https://www.imdb.com/title/%s/' % imdb
	r = client.request(url)
	i = re.compile('<span itemprop="ratingValue">(.+?)</span></strong>').findall(r)
	for rating in i:
		return rating

def votes(imdb):
	url = 'https://www.imdb.com/title/%s/' % imdb
	r = client.request(url)
	i = re.compile('<span class="small" itemprop="ratingCount">(.+?)</span>').findall(r)
	for votes in i:
		return votes

def director(imdb):
	url = 'https://www.imdb.com/title/%s/' % imdb
	r = client.request(url)
	try: director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', r)
	except: director = '0'
	director = client.parseDOM(director, 'a')
	director = ' / '.join(director)
	if director == '': director = '0'
	director = client.replaceHTMLCodes(director)
	director = director.encode('utf-8')
	return director

def age_mv(tmdb):
	url = 'https://api.themoviedb.org/3/movie/%s/release_dates?api_key=%s&language=en-US' % (tmdb, tmdb_api)
	r = client.request(url)
	i = re.compile('"iso_3166_1":"GB","release_dates":\[\{"certification":"(.+?)"').findall(r)
	for mpaa in i:
		return mpaa

def seasons(tmdb):
	url = 'https://api.themoviedb.org/3/tv/%s?api_key=%s&language=en-US' % (tmdb, tmdb_api)
	r = client.request(url)
	i = re.compile('"number_of_seasons":(.+?),').findall(r)
	for seasons in i:
		seasons = str(seasons)
		return seasons

def trailer(tmdb,content):
	if content == 'movie': url = 'https://api.themoviedb.org/3/movie/%s/videos?api_key=%s&language=en-US' % (tmdb, tmdb_api)
	else: url = 'https://api.themoviedb.org/3/tv/%s/videos?api_key=%s&language=en-US' % (tmdb, tmdb_api)

	r = client.request(url)
	data = json.loads(r)
	for i in data['results']:
		type = i['type']
		key = i['key']
		if type == 'Trailer':
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % key
			#return url
			xbmc.executebuiltin('PlayMedia(%s)' % url)

def poster(tmdb,content):
	if content == 'movie': url = 'https://api.themoviedb.org/3/movie/%s/videos?api_key=%s&language=en-US' % (tmdb, tmdb_api)
	else: url = 'https://api.themoviedb.org/3/tv/%s?api_key=%s&language=en-US' % (tmdb, tmdb_api)
	r = client.request(url)
	data = json.loads(r)
	for i in data:
		poster = i['poster_path']
		poster = 'https://image.tmdb.org/t/p/original' + poster