import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urlparse
import datetime
import locale
import platform

# plugin constants
__plugin__ = "plugin.video.ilmeteo"
__author__ = "Nightflyer"

Addon = xbmcaddon.Addon(id=__plugin__)
Icon = os.path.join(Addon.getAddonInfo('path'), 'icon.png')

# plugin handle
handle = int(sys.argv[1])

# set italian locale
if  platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, 'ita_ita')
else:
    locale.setlocale(locale.LC_ALL, 'it_IT')
    
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
    for i in range(6):
        if i == 0:
            title = "Oggi"
        elif i == 1:
            title = "Domani"
        else:
            day = datetime.date.today() + datetime.timedelta(days=i)
            title = day.strftime("%A %d %B").capitalize()
        liStyle = xbmcgui.ListItem(title,  thumbnailImage=Icon)
        addLinkItem({"day": str(i)}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def play(day):
    meteo_day = datetime.date.today() + datetime.timedelta(days=int(day))
    
    if day == 0:
        title = "Meteo Oggi"
    elif day == 1:
        title = "Meteo Domani"
    else:
        title = "Meteo " + meteo_day.strftime("%d %B %Y")

    url = "http://media.ilmeteo.it/video/%s-tg.mp4" % meteo_day.strftime("%Y-%m-%d")  
    item=xbmcgui.ListItem(title, thumbnailImage=Icon)
    item.setInfo(type="Video", infoLabels={"Title": title})
    xbmc.Player().play(url, item)

# parameter values
params = parameters_string_to_dict(sys.argv[2])
day = str(params.get("day", ""))

if day != "":
    play(day)
else:
    show_root_menu()

