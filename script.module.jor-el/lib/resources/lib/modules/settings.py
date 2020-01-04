# -*- coding: utf-8 -*-
import re
import unicodedata
import json
from resources.lib.modules import client

tmdb_api = '1e7b47249796f50c0b783fcdcbcfa8ba'

def toggleOff(content):
	if content == 'streams': find = '<category label="32345">'
	else: find = '<!-- FIND TORRENTS -->'
	
	file = xbmc.translatePath('special://userdata/addon_data/plugin.video.jor-el/settings.xml')
	data = open(file,'r')
	data = data.read()
	match = re.compile('').findall(r)