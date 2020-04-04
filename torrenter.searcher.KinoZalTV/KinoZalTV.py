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

import re
import urllib
import sys
import xbmc
import xbmcaddon
import os
import socket

import SearcherABC


class KinoZalTV(SearcherABC.SearcherABC):

    __torrenter_settings__ = xbmcaddon.Addon(id='plugin.video.torrenter')
    #__torrenter_language__ = __settings__.getLocalizedString
    #__torrenter_root__ = __torrenter_settings__.getAddonInfo('path')

    ROOT_PATH=os.path.dirname(__file__)
    addon_id=ROOT_PATH.replace('\\','/').rstrip('/').split('/')[-1]
    __settings__ = xbmcaddon.Addon(id=addon_id)
    __addonpath__ = __settings__.getAddonInfo('path')
    __version__ = __settings__.getAddonInfo('version')
    __plugin__ = __settings__.getAddonInfo('name').replace('Torrenter Searcher: ','') + " v." + __version__

    username = __settings__.getSetting("username")
    password = __settings__.getSetting("password")
    baseurl = 'kinozal-tv.appspot.com'

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
        if self.__settings__.getSetting("usemirror")=='true':
            self.baseurl = self.__settings__.getSetting("baseurl")
            self.log('baseurl: '+str(self.baseurl))

        self.logout()

        if self.timeout_multi==0:
            socket.setdefaulttimeout(10+(10*self.torrenter_timeout_multi))
        else:
            socket.setdefaulttimeout(10+(10*(self.timeout_multi-1)))

        #self.debug = self.log

    def logout(self):
        old_username = self.__settings__.getSetting("old_username")
        if old_username in [None,''] or old_username!=self.username:
            self.__settings__.setSetting("old_username", self.username)
            self.clear_cookie(self.baseurl)
        self.login()

    def search(self, keyword):
        filesList = []
        url = 'http://%s/browse.php?s=%s&g=0&c=0&v=0&d=0&w=0&t=1&f=0' % (self.baseurl, urllib.quote_plus(
            keyword.decode('utf-8').encode('cp1251')))

        headers = [('Origin', 'http://%s' % self.baseurl),
                   ('User-Agent',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 YaBrowser/14.10.2062.12061 Safari/537.36'),
                   ('Referer', 'http://%s/' % self.baseurl)]

        response = self.makeRequest(url, headers=headers)
        if None != response and 0 < len(response):
            response = response.decode('cp1251').encode('utf-8')
            self.debug(response)
            bad_forums = [2, 1, 23, 32, 40, 41]
            regex = '''<tr class.+?<td class.+?</tr>'''
            regex_tr = '''onclick="cat\((\d+)\);".+?<a href="/details\.php.+?id=(\d+)".+?>(.+?)</a>.+?<td class='s'>(.+?)</td>.+?class='sl_s'>(\d+)</td>.+?class='sl_p'>(\d+)</td>'''
            for tr in re.compile(regex, re.DOTALL).findall(response):
                result=re.compile(regex_tr, re.DOTALL).findall(tr)
                self.debug(tr+' -> '+str(result))
                if result:
                    (forum, topic, title, size, seeds, leechers)=result[0]
                    if int(forum) not in bad_forums:
                        link = 'http://%s/download.php?id=%s' % (self.baseurl, topic)
                        filesList.append((
                            int(int(self.sourceWeight) * int(seeds)),
                            int(seeds), int(leechers), size,
                            self.unescape(self.stripHtml(title)),
                            self.__class__.__name__ + '::' + link,
                            self.searchIcon,
                        ))
        return filesList

    def check_login(self, response=None):
        if None != response and 0 < len(response):
            if re.compile('<html><head>').search(response):
                self.log('KinoZal Not logged!')
                self.login()
                return False
        return True

    def getTorrentFile(self, url):
        self.timeout(5)

        content = self.makeRequest(url)
        self.debug('getTorrentFile: '+content)
        if not self.check_login(content):
            content = self.makeRequest(url)

        if re.search("<html><head", content):
            content = content.decode('cp1251').encode('utf-8')

            msg = re.search("Вам доступно \d+ торрент-файлов в сутки для скачивания\.",
                            content)
            self.log(msg.group(0))
            if msg:
                self.showMessage('KinoZal Error', msg.group(0))
                xbmc.sleep(1000)
                self.debug('getTorrentFile2: '+content)
                sys.exit(1)

        else:
            return self.saveTorrentFile(url, content)

    def login(self):
        data = {
            'password': self.password,
            'username': self.username,
            'returnto:': ''
        }
        response = self.makeRequest(
            'https://%s/takelogin.php' % self.baseurl,
            data
        )
        self.debug(response)
        self.cookieJar.save(ignore_discard=True)
        for cookie in self.cookieJar:
            uid, passed = None, None
            if cookie.name == 'uid':
                uid = cookie.value
            if cookie.name == 'pass':
                passed = cookie.value
            if uid and passed:
                return 'uid=' + uid + '; pass=' + passed
        return False

    def showMessage(self, heading, message, times=10000):
        xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (
            heading.replace('"', "'"), message.replace('"', "'"), times, self.searchIcon))
        self.log(str((heading.replace('"', "'"), message.replace('"', "'"), times, self.searchIcon)))