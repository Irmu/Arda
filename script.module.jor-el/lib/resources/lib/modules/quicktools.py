# -*- coding: utf-8 -*-

"""
    Jor-El Add-on

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
"""

from resources.lib.modules import control
import sys
import xbmc
import xbmcgui

def tools():
	sysaddon = sys.argv[0]
	
	select = xbmcgui.Dialog().select('EverStream - Quick Tools Menu', [
		'Clear Providers...',
		'Clear Search History...',
		'Clear Cache...',
		'View Changelog',
		'Authorise Trakt'
	])
	
	if select == 0:
		xbmc.executebuiltin('XBMC.RunPlugin(%s?action=clearSources)' % sysaddon)
	if select == 1:
		xbmc.executebuiltin('XBMC.RunPlugin(%s?action=clearCacheSearch)' % sysaddon)
	if select == 2:
		xbmc.executebuiltin('XBMC.RunPlugin(%s?action=clearCache)' % sysaddon)
	if select == 3:
		xbmc.executebuiltin('XBMC.RunPlugin(%s?action=viewChangelog)' % sysaddon)
	if select == 4:
		xbmc.executebuiltin('XBMC.RunPlugin(%s?action=authTrakt)' % sysaddon)
	#if select == 5:
	#	xbmc.executebuiltin('XBMC.RunPlugin(%s?action=)' % sysaddon)
	