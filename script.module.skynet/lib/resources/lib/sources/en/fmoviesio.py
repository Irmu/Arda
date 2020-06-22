# -*- coding: UTF-8 -*-

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urlparse, re
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['fmoviesto.to']
        self.base_link = 'https://www4.fmovies2.io'
        self.search_link = '/search.html?keyword=%s'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search_id.replace(':', ' ').replace(' ', '+'))
            search_results = client.request(url, headers=self.headers)
            match = re.compile('<a href="/watch/(.+?)" title="(.+?)">').findall(search_results)
            for row_url, row_title in match:
                row_url = self.base_link + '/watch/%s' % row_url
                if cleantitle.get(title) in cleantitle.get(row_title):
                    return row_url
            return
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostDict + hostprDict
            if url is None:
                return sources
            html = client.request(url, headers=self.headers)
            quality = re.compile('<div>Quanlity: <span class="quanlity">(.+?)</span></div>').findall(html)
            for qual in quality:
                quality = source_utils.check_url(qual)
                info = qual
            links = re.compile('var link_.+? = "(.+?)"').findall(html)
            for url in links:
                if not url.startswith('http'):
                    url = "https:" + url
                if 'load.php' not in url:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
