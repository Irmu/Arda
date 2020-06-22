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

import re,requests
from resources.lib.modules import control, client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['newepisodes.co']
        self.base_link = 'https://newepisodes.co'
        self.headers = {'User-Agent': client.agent(), 'Referer': self.base_link}
        self.session = requests.Session()
        self.tm_user = control.setting('tm.user')

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvShowTitle = cleantitle.geturl(tvshowtitle)
            tmdburl = 'https://api.themoviedb.org/3/find/%s?external_source=tvdb_id&language=en-US&api_key=%s' % (tvdb, self.tm_user)
            tmdbresult = self.session.get(tmdburl, headers=self.headers).content
            tmdb_id = re.compile('"id":(.+?),',re.DOTALL).findall(tmdbresult)[0]
            url = '/watch-' + tvShowTitle + '-online-free/' + tmdb_id
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            episodeTitle = cleantitle.geturl(title)
            url = self.base_link + url + '/season-' + season + '-episode-' + episode + '-' + episodeTitle
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            url = url.replace(' ', '-')  # Probably overkill but better safe while high lol.
            r = self.session.get(url, headers=self.headers).content
            match = re.compile('<li class="playlist_entry " id="(.+?)"><a><div class="list_number">.+?</div>(.+?)<span>></span></a></li>',re.DOTALL).findall(r)
            for id, host in match:
                url = self.base_link + '/embed/' + id
                valid, host = source_utils.is_host_valid(host, hostDict)
                if valid:  # Make sure your craptcha setting is disabled when trying to test this valid check lmao. saves a hour.
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        r = self.session.get(url, headers=self.headers).content
        url = re.compile('<iframe.+?src="(.+?)"').findall(r)[0]
        return url
