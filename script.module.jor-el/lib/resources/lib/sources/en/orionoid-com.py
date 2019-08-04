import random
import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['orionoid.com']
		self.base_link = 'https://api.orionoid.com'
		self.movie_link = '/?keyuser=%s&keyapp=%s&mode=stream&action=retrieve&type=movie&idimdb=%s&limitcount=%s&videoquality=%s_%s&streamtype=hoster&access=%s'
		self.tv_link = '/?keyuser=%s&keyapp=%s&mode=stream&action=retrieve&type=show&idimdb=%s&numberseason=%s&numberepisode=%s&limitcount=%s&videoquality=%s_%s&streamtype=hoster&access=%s'
		
		self.api_app = 'G9MBNN5F7AV5ETNMLC7RERRKHKHEWJLF'
		self.api_user = control.setting('orionoid.api')
		self.setting_count = control.setting('orionoid.count')
		self.setting_min = control.setting('orionoid.min')
		self.setting_max = control.setting('orionoid.max')
		self.setting_debrid = control.setting('orionoid.debrid')
		
		if self.setting_debrid == 'false': self.access = 'indirect' #'direct'
		else: self.access = 'debrid'
		
		api_backup = [
			'2KL6SLGNTE7K7N2JTSKE6WTV8CHL7LPN',
			'K7SRDELBTKFLS7FSGBFNJJLGDD5CJNKG',
			'UU3DJ7GM3HPQMANVATK8XRPHFQNEFMC7',
			'QPHJMRVWVD9D4MLJKENK9TFDH8CXTXBG',
			'TCJKFBVVRB6BE4F7Q7KEGDP8BKG9PC6W',
			'SFECL9KAFFFMQKW7FGTKHDCD9PH9RJ9P',
			'QLFPACQERGCJ6ELPSHE7L9JQLQNKLDKH',
			'CAHK2C5QJURMC6VN46EMKJFNE77PEH9F',
			'X9SDKDPGMFL4KF5GFEMDDHNSRKBW66KE',
			'GM4H6KLBCXHDWLGWJTG9EVSDJJ7GEMG9',
			'AXHFRKEBQD6L8P6THVGF9FJDXF8NMQDY',
			'HPJSGSY7RFKCDMJNRMCK6K8FCQQU4JRE',
			#'',
			#'',
			#'',
			#'',
			#'',
			#'',
			#'',
			#'',
		]
		
		if self.api_user == '':
			self.api_user = random.choice(api_backup)
			self.setting_count = '5'
		else:
			api_check = self.base_link + '/?keyuser=%s&keyapp=%s&mode=user&action=retrieve' % (self.api_user,self.api_app)
			r = client.request(api_check)
			if '"remaining":0' in r:
				self.api_user = random.choice(api_backup)
				self.setting_count = '5'
			else:
				self.api_user = control.setting('orionoid.api')

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			imdb = imdb.replace('tt','')
			url = self.base_link + self.movie_link % (self.api_user,self.api_app,imdb,self.setting_count,self.setting_min,self.setting_max,self.access)
			return url
		except:
			return
			
	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = imdb.replace('tt','')
			return url
		except:
			return
 
	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url: return
			imdb = url
			url = self.base_link + self.tv_link % (self.api_user,self.api_app,imdb,season,episode,self.setting_count,self.setting_min,self.setting_max,self.access)
			return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			r = client.request(url)
			try:
				match = re.compile('"type":"hoster","link":"(.+?)","source":".+?","hoster":"(.+?)".+?"quality":"(.+?)"').findall(r)
				for url,host,quality in match: 
					if quality == 'hd4k': quality = '4K'
					if quality == 'hd2k': quality = '4K'
					if quality == 'hd1080': quality = '1080p'
					if quality == 'hd720': quality = 'HD'
					if quality == 'sd': quality = 'SD'
					url = url.replace("\/","/")
					sources.append({
						'source': host,
						'quality': quality,
						'language': 'en',
						'url': url,
						'direct': False,
						'debridonly': False
					})
			except:
				return
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url