# -*- coding: utf-8 -*-
'''
    Torrenter v2 plugin for XBMC/Kodi
    Copyright (C) 2012-2015 Vadim Skorba v1 - DiMartino v2
    http://forum.kodi.tv/showthread.php?tid=214366

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

import urllib
import re
import sys
import xbmcaddon
import os
import socket

import SearcherABC

class KickAssSo(SearcherABC.SearcherABC):

    __torrenter_settings__ = xbmcaddon.Addon(id='plugin.video.torrenter')
    #__torrenter_language__ = __settings__.getLocalizedString
    #__torrenter_root__ = __torrenter_settings__.getAddonInfo('path')

    ROOT_PATH=os.path.dirname(__file__)
    addon_id=ROOT_PATH.replace('\\','/').rstrip('/').split('/')[-1]
    __settings__ = xbmcaddon.Addon(id=addon_id)
    __addonpath__ = __settings__.getAddonInfo('path')
    __version__ = __settings__.getAddonInfo('version')
    __plugin__ = __settings__.getAddonInfo('name') + " v." + __version__

    username = __settings__.getSetting("username")
    password = __settings__.getSetting("password")
    baseurl = 'kickass.cd' # TODO: change this!

    '''
    Setting the timeout
    '''
    torrenter_timeout_multi=int(sys.modules["__main__"].__settings__.getSetting("timeout"))
    timeout_multi=int(__settings__.getSetting("timeout"))

    '''
    Weight of source with this searcher provided. Will be multiplied on default weight.
    '''
    sourceWeight = 1

    '''
    Full path to image will shown as source image at result listing
    '''
    searchIcon = os.path.join(__addonpath__,'icon.png')

    '''
    Flag indicates is this source - magnet links source or not.
    '''

    @property
    def isMagnetLinkSource(self):
        return False

    '''
    Main method should be implemented for search process.
    Receives keyword and have to return dictionary of proper tuples:
    filesList.append((
        int(weight),# Calculated global weight of sources
        int(seeds),# Seeds count
        int(leechers),# Leechers count
        str(size),# Full torrent's content size (e.g. 3.04 GB)
        str(title),# Title (will be shown)
        str(link),# Link to the torrent/magnet
        str(image),# Path to image shown at the list
    ))
    '''

    def __init__(self):
        self.logout()

        if self.timeout_multi==0:
            socket.setdefaulttimeout(10+(10*self.torrenter_timeout_multi))
        else:
            socket.setdefaulttimeout(10+(10*(self.timeout_multi-1)))

        if self.__settings__.getSetting("usemirror")=='true':
            self.baseurl = self.__settings__.getSetting("baseurl")

        #self.debug = self.log

    def search(self, keyword):
        filesList = []
        url = "http://%s/usearch/%s/?field=seeders&sorder=desc" % (self.baseurl, urllib.quote_plus(keyword))
        headers = [('User-Agent',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 YaBrowser/14.10.2062.12061 Safari/537.36'),
           ('Referer', 'http://%s/' % self.baseurl), ('Accept-encoding', 'gzip'), ]

        response = self.makeRequest(url, headers=headers)

        if None != response and 0 < len(response):
            self.debug(response)
            good_forums=['TV','Anime','Movies','Video']

            regex = '''<tr class=".+?" id=.+?</tr>'''
            regex_tr = r'''title="Download torrent file" href="(.+?)" class=".+?"><i.+?<a.+?<a.+?<a href=".+?html" class=".+?">(.+?)</a>.+? in <span.+?"><strong>.+?">(.+?)</a>.+?<td class="nobr center">(.+?)</td>.+?<td class="green center">(\d+?)</td>.+?<td class="red lasttd center">(\d+?)</td>'''
            for tr in re.compile(regex, re.DOTALL).findall(response):
                result=re.compile(regex_tr, re.DOTALL).findall(tr)
                self.debug(tr+' -> '+str(result))
                if result:
                    (link, title, forum, size, seeds, leechers)=result[0]
                    if forum in good_forums:
                        torrentTitle = self.unescape(self.stripHtml(title))
                        size = self.unescape(self.stripHtml(size))
                        filesList.append((
                            int(int(self.sourceWeight) * int(seeds)),
                            int(seeds), int(leechers), size,
                            torrentTitle,
                            self.__class__.__name__ + '::' + link,
                            self.searchIcon,
                        ))
        return filesList

    def getTorrentFile(self, url):
        if url.startswith('//'):
            url = 'http:' + url
        referer = url.split('?')[0].replace('.torrent','/') + urllib.quote_plus(url.split('?')[1]+'.torrent')
        url = url.replace('https://','http://').split('?')[0]
        self.debug('[getTorrentFile]: url = %s; ref = %s' % (str(url), str(referer)))
        headers = [('User-Agent',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 YaBrowser/14.10.2062.12061 Safari/537.36'),
           ('Referer', referer), ('Accept-encoding', 'gzip'), ]
        content = self.makeRequest(url, headers=headers)
        return self.saveTorrentFile(url, content)