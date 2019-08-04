import xbmc
import xbmcaddon
import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import torrent


class source:
    def __init__(self):
        self.priority = 1
        self.language = ["en"]
        self.domains = ["qtorrent.in"]
        self.base_link = "https://torrent.fail/"
        self.search_link = "/search/%s/%s/99/0"

        privateToken = xbmcaddon.Addon("plugin.video.jor-el").getSetting(
            "private.rd.enable"
        )
        if privateToken == "true":
            self.token = xbmcaddon.Addon("plugin.video.jor-el").getSetting(
                "private.rd.api"
            )
        else:
            self.token = xbmcaddon.Addon("script.realdebrid.mod").getSetting(
                "rd_access"
            )

    def movie(self, imdb, title, localtitle, aliases, year):
        if xbmc.getCondVisibility("System.HasAddon(script.realdebrid.mod)"):
            try:
                title = cleantitle.geturl(title)
                title = title.replace("-", "%20")
                url = title + "%20" + year
                return url
            except:
                return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if xbmc.getCondVisibility("System.HasAddon(script.realdebrid.mod)"):
            try:
                url = cleantitle.geturl(tvshowtitle)
                url = url.replace("-", "%20")
                return url
            except:
                return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            season = "%02d" % int(season)
            episode = "%02d" % int(episode)
            url = url + "%20s" + str(season) + "e" + str(episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            q = url

            try:  # Page 1
                page = "1"
                url = self.base_link + self.search_link % (q, page)
                r = client.request(url)
                match = re.compile(
                    '>(.+?)</a>\n</div>\n<a href="magnet\:\?xt=urn\:btih\:(.+?)&'
                ).findall(r)
                for filename, hash in match:
                    quality = torrent.qualityCheck(filename)
                    # Find infohash
                    url = (
                        "https://api.real-debrid.com/rest/1.0/torrents/instantAvailability/%s?auth_token=%s"
                        % (hash, self.token)
                    )
                    # Check availability
                    r = client.request(url)
                    r = (
                        r.replace("	", "")
                        .replace("\n", "")
                        .replace("[", "")
                        .replace("]", "")
                        .replace("\/", "/")
                        .replace("{", "")
                    )
                    r = r.replace('"rd": ', ",")
                    match = re.compile(',"(.+?)": "filename": "(.+?)"').findall(r)
                    for id, filename in match:
                        quality = quality
                        hash = hash
                        # Check video isn't sample
                        for check in torrent.check_filename:
                            if check in filename:
                                if (
                                    ".mkv" in filename
                                    or ".mp4" in filename
                                    or ".flv" in filename
                                    or ".avi" in filename
                                ):
                                    url = 'url="%s"&filename="%s"&id="%s"' % (
                                        hash,
                                        filename,
                                        id,
                                    )
                                    sources.append(
                                        {
                                            "source": "Torrent",
                                            "info": filename,
                                            "quality": quality,
                                            "language": "en",
                                            "url": url,
                                            "direct": False,
                                            "debridonly": False,
                                        }
                                    )
            except:
                return

            try:  # Page 2
                page = "2"
                url = self.base_link + self.search_link % (q, page)
                r = client.request(url)
                match = re.compile(
                    '>(.+?)</a>\n</div>\n<a href="magnet\:\?xt=urn\:btih\:(.+?)&'
                ).findall(r)
                for filename, hash in match:
                    quality = torrent.qualityCheck(filename)
                    # Find infohash
                    url = (
                        "https://api.real-debrid.com/rest/1.0/torrents/instantAvailability/%s?auth_token=%s"
                        % (hash, self.token)
                    )
                    # Check availability
                    r = client.request(url)
                    r = (
                        r.replace("	", "")
                        .replace("\n", "")
                        .replace("[", "")
                        .replace("]", "")
                        .replace("\/", "/")
                        .replace("{", "")
                    )
                    r = r.replace('"rd": ', ",")
                    match = re.compile(',"(.+?)": "filename": "(.+?)"').findall(r)
                    for id, filename in match:
                        quality = quality
                        hash = hash
                        # Check video isn't sample
                        for check in torrent.check_filename:
                            if check in filename:
                                if (
                                    ".mkv" in filename
                                    or ".mp4" in filename
                                    or ".flv" in filename
                                    or ".avi" in filename
                                ):
                                    url = 'url="%s"&filename="%s"&id="%s"' % (
                                        hash,
                                        filename,
                                        id,
                                    )
                                    sources.append(
                                        {
                                            "source": "Torrent",
                                            "info": filename,
                                            "quality": quality,
                                            "language": "en",
                                            "url": url,
                                            "direct": False,
                                            "debridonly": False,
                                        }
                                    )
            except:
                return

        except Exception:
            return
        return sources

    def resolve(self, url):
        match = re.compile('url="(.+?)"&filename="(.+?)"&id="(.+?)"').findall(url)
        # Fetch magnet link
        for hash, filename, id in match:
            import xbmcgui

            id = id
            magnetLink = "magnet:?xt=urn:btih:%s" % hash
            magnetLink = urllib.quote_plus(magnetLink)

            # Pass on to script.realdebrid.mod...
            import xbmc

            if id == "1":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=4&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "2":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=14&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "3":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=15&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "4":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=16&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "5":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=17&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "6":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=18&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "7":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=19&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "8":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=20&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "9":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=21&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )
            if id == "10":
                xbmc.executebuiltin(
                    "RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=22&name=na&poster=na&link="
                    + magnetLink
                    + "&url)"
                )

            import time

            time.sleep(8)

            import json

            api = (
                "https://api.real-debrid.com/rest/1.0/torrents?auth_token=%s"
                % self.token
            )
            r = client.request(api)

            data = json.loads(r)
            for i in data:
                hash2 = i["hash"]
                url = i["links"][0]
                hash = hash.lower()
                if hash == hash2:
                    url = (
                        "plugin://script.realdebrid.mod/?url=%s&mode=5&name=Real-Debrid&icon=none&fanart=none&poster=none"
                        % url
                    )
                    return url
