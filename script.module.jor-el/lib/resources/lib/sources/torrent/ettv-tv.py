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
        self.domains = ["ettv.tv"]
        self.base_link = "https://www.ettv.tv"
        self.mv_link = "/torrents-search.php?c66=1&c65=1&c67=1&c1=1&c2=1&c76=1&c3=1&c47=1&c42=1&search=%s&sort=seeders&order=desc"
        self.tv_link = "/torrents-search.php?c79=1&c41=1&c77=1&c5=1&c50=1&c72=1&c89=1&search=%s&sort=seeders&order=desc"

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
                title = title.replace("-", "+")
                query = "%s+%s" % (title, year)
                url = self.base_link + self.mv_link % query
                return url
            except:
                return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if xbmc.getCondVisibility("System.HasAddon(script.realdebrid.mod)"):
            try:
                url = cleantitle.geturl(tvshowtitle)
                url = url.replace("-", "+")
                return url
            except:
                return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            season = "%02d" % int(season)
            episode = "%02d" % int(episode)
            query = "%s+s%se%s" % (url, str(season), str(episode))
            url = self.base_link + self.tv_link % query
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            try:  # Page 1
                r = client.request(url)
                match = re.compile(
                    "<td class='' nowrap='nowrap' style='white-space\: nowrap;'>&nbsp;<a title=\".+?\" href=\"(.+?)\"><b>(.+?)</b>"
                ).findall(r)
                for url, filename in match:
                    if (
                        "KORSUB" in filename
                        or "korsub" in filename
                        or "KorSub" in filename
                    ):
                        pass
                    else:
                        torrenturl = self.base_link + url
                        quality = torrent.qualityCheck(filename)

                        # Find infohash
                        r = client.request(torrenturl)
                        match = re.compile(
                            "<b>Info Hash:</b></td><td>(.+?)</td>"
                        ).findall(r)
                        for hash in match:
                            quality = quality
                            hash = hash
                            url = (
                                "https://api.real-debrid.com/rest/1.0/torrents/instantAvailability/%s?auth_token=%s"
                                % (hash, self.token)
                            )
                            torrenturl = torrenturl
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
                            match = re.compile(',"(.+?)": "filename": "(.+?)"').findall(
                                r
                            )
                            for id, filename in match:
                                quality = quality
                                hash = hash
                                torrenturl = torrenturl
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
            id = id
            filename = (
                filename.replace("[", "")
                .replace("]", "")
                .replace("(", "")
                .replace(")", "")
            )
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
