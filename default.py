# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urllib2
import urlparse
import re
import datetime
from BeautifulSoup import BeautifulSoup

# plugin constants
__plugin__ = "plugin.video.ilmeteo"
__author__ = "Nightflyer"

Addon = xbmcaddon.Addon(id=__plugin__)
Icon = os.path.join(Addon.getAddonInfo('path'), 'icon.png')

# plugin handle
handle = int(sys.argv[1])

# utility functions
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = dict(urlparse.parse_qsl(parameters[1:]))
    return paramDict
 
def addLinkItem(parameters, li):
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=False)

# UI builder functions
def show_root_menu():
    ''' Show the plugin root menu '''
    pageUrl = "http://www.ilmeteo.it/video/"
    htmlData = urllib2.urlopen(pageUrl).read()
    
    # Grab video pages
    tree = BeautifulSoup(htmlData, convertEntities=BeautifulSoup.HTML_ENTITIES)
    links = tree.find("div", "giornale-video-homebox").findAll('a')
    for link in links:
        image = "http://media.ilmeteo.it/video/img/tg.jpg"
        liStyle = xbmcgui.ListItem(link["title"], thumbnailImage=image)
        addLinkItem({"pageurl": link["href"]}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def play(pageUrl):
    htmlData = urllib2.urlopen(pageUrl).read()
    
    # Grab title
    tree = BeautifulSoup(htmlData, convertEntities=BeautifulSoup.HTML_ENTITIES)
    title = tree.find("title").contents[0].strip()
    title = title.replace(" | IL METEO.IT", "")
    
    # Grab video URL
    match=re.compile('videoURL=(.+?)&').findall(htmlData)
    url = match[0]
    
    # Set thumbnail
    image = "http://media.ilmeteo.it/video/img/tg.jpg"
    
    # Play
    item=xbmcgui.ListItem(title, thumbnailImage=image)
    item.setInfo(type="Video", infoLabels={"Title": title})
    xbmc.Player().play(url, item)

# parameter values
params = parameters_string_to_dict(sys.argv[2])
pageurl = str(params.get("pageurl", ""))

if pageurl != "":
    play(pageurl)
else:
    show_root_menu()

