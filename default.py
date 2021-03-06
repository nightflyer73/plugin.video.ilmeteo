﻿# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urllib2
import urlparse
import hashlib
from datetime import datetime
from xml.dom import minidom

# plugin constants
__plugin__ = "plugin.video.ilmeteo"
__author__ = "Nightflyer"

Addon = xbmcaddon.Addon(id=__plugin__)

# plugin handle
handle = int(sys.argv[1])

# utility functions
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = dict(urlparse.parse_qsl(parameters[1:]))
    return paramDict
 
def addLinkItem(url, li):
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=False)

# UI builder functions
def show_root_menu():
    ''' Show the plugin root menu '''
    
    # Config
    wsBaseUrl = "http://iphone.ilmeteo.it/android-app.php?"
    wsVersion = "4.3"
    langId = "ita"
    appId = "com.ilmeteo.android.ilmeteo"
    userAgent = "Dalvik/2.1.0 (Linux; U; Android 8.1.0; Pixel 2 Build/OPM1.171019.013)"
    
    opener = urllib2.build_opener()
    # Use Android User-Agent
    opener.addheaders = [('User-Agent', userAgent)]
    urllib2.install_opener(opener)

    # Generate MD5 hash
    day = datetime.now().day
    hash = hashlib.md5("listVideos#AndroidApp#%02d" % day).hexdigest()

    # Get video list
    url = wsBaseUrl + "method=listVideos&x=%s&v=%s&lang=%s&app=%s" % (hash, wsVersion, langId, appId)
    xbmc.log(url)
    xmldata = urllib2.urlopen(url).read()
    dom = minidom.parseString(xmldata)
    
    # Parse video feed
    for videoNode in dom.getElementsByTagName('video'):
        link = videoNode.attributes["url"].value
        d = videoNode.attributes["date"].value
        imageUrl = "http://media.ilmeteo.it/video/img/%s-%s-%s-tg-300.jpg" % (d[:4], d[4:6], d[6:])
        title = videoNode.firstChild.nodeValue
        liStyle = xbmcgui.ListItem(title, thumbnailImage=imageUrl)
        addLinkItem(link, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

show_root_menu()
