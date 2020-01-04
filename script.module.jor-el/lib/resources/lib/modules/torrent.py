# -*- coding: utf-8 -*-
import re
import unicodedata
import json
import xbmcaddon
from resources.lib.modules import client

dupes = []

check_filename = [
	'2160',
	'DVDSCR',
	'DVDScr',
	'HD-TS',
	'480',
	'720',
	'1080',
	'HDRip',
	'HDTV',
	'WebRip',
	'WEBRIP',
	'WEBRip',
	'BDRip'
	]
	
def qualityCheck(filename):
	if '2160' in filename: quality = '4K'
	elif 'DVDSCR' in filename: quality = 'SD'
	elif 'DVDScr' in filename: quality = 'SD'
	elif 'HD-TS' in filename: quality = 'SD'
	elif '480' in filename: quality = 'SD'
	elif '720' in filename: quality = 'HD'
	elif '1080' in filename: quality = '1080p'
	elif 'HDRip' in filename: quality = 'SD'
	elif 'HDTV' in filename: quality = 'SD'
	elif 'WebRip' in filename: quality = 'SD'
	elif 'WEBRIP' in filename: quality = 'SD'
	elif 'WEBRip' in filename: quality = 'SD'
	elif 'BDRip' in filename: quality = '1080p'
	else: quality = 'SD'
	return quality

def available(url):
	token = xbmcaddon.Addon('script.module.resolveurl').getSetting('RealDebridResolver_token')
	url   = 'https://api.real-debrid.com/rest/1.0/torrents/instantAvailability/%s?auth_token=%s' % (url,token)
	r     = client.request(url)
	r     = r.replace('	','').replace('\n','').replace('[','').replace(']','').replace('\/','/').replace('{','')
	r     = r.replace('"rd": ',',')
	match = re.compile('"filename": "(.+?)"').findall(r)
	for filename in match:
		return filename