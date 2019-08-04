# written by me
# checked 2019-03-11

import re
import urllib
import urlparse
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['ffilms.org']
		self.base_link = 'https://ffilms.org'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = title + '-' + year
			return url
		except:
			return
			
	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			search = self.base_link + '/' + url + '/'
			scraper = cfscrape.create_scraper()
			r = scraper.get(search).content
			try:
				match = re.compile('src="//ok\.ru/videoembed/(.+?)"').findall(r)
				for vid in match: 
					url = 'https://ok.ru/videoembed/' + vid
				
					sources.append({
						'source': 'ok',
						'quality': 'HD',
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