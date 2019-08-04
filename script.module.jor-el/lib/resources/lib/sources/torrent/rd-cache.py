import xbmc
import xbmcgui
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
        self.domains = ["real-debrid.com"]
        self.base_link = "https://real-debrid.com"

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
                url = "%s (%s)" % (title, year)
                return url
            except:
                return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if xbmc.getCondVisibility("System.HasAddon(script.realdebrid.mod)"):
            try:
                url = tvshowtitle
                return url
            except:
                return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            season = "%02d" % int(season)
            episode = "%02d" % int(episode)
            url = "%s S%sE%s" % (url, str(season), str(episode))
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            q1 = url
            q2 = url.replace("(", "").replace(")", "")
            q3 = url.replace("(", "").replace(")", "").replace(" ", ".")

            try:
                import json

                url = (
                    "https://api.real-debrid.com/rest/1.0/torrents?auth_token=%s"
                    % self.token
                )
                r = client.request(url)
                data = json.loads(r)
                for i in data:
                    filename = i["filename"]
                    url = i["links"][0]
                    if q1 in filename or q2 in filename or q3 in filename:
                        url = (
                            "plugin://script.realdebrid.mod/?url=%s&mode=5&name=Real-Debrid&icon=none&fanart=none&poster=none"
                            % url
                        )
                        quality = torrent.qualityCheck(filename)

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
        return url
