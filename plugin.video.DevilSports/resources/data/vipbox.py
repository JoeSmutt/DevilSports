import xbmc, xbmcgui, xbmcplugin
import urllib, urllib2
import re
import requests

def addon_log(string):
    try:
        xbmc.log("[DevilSports Lists-%s]: %s" %('0.0.1', string))
    except:
        pass

def addDir(name,url,mode,icon,fanart, handle):
    addon_log('Adding Directories')
    url = base_url + '?' + urllib.urlencode({'mode': mode, 'foldername': name, 'url':url,'fanart':fanart})
    li = xbmcgui.ListItem(name, iconImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

def addLink(name,url,mode,icon,fanart, handle):
    addon_log('Adding Link')
    url = base_url + '?' + urllib.urlencode({'mode': mode, 'foldername': name, 'url':url,'fanart':fanart})
    li = xbmcgui.ListItem(name, iconImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
def getSportCategories(url, handle):
    r = requests.get(url)
    match = re.compile('<a class=.+? target=.+? href=(.+?) title=.+?><div class=.+?><div id=.+? class=.+?></div></div><span class=.+?>(.+?)</span></a>', re.DOTALL).findall(r.content)
    for href, name in match:
        addDir(name, href, 'page',name,name+'_fanart', handle)
        
def getSportLinks(url, handle):
    r = requests(url)
    match = re.compile('<a href=(.+?) .+? gday=(.+?) class="matchtime">(.+?)</span> (.+?)</a>', re.DOTALL).findall(r.content)
    for href,gameday,gametime,name in match:
        addLink('[%s - %s] %s'%(gameday,gametime,name), href, 'play',name,name+'_fanart', handle)
        
        match2 = re.compile('<div class=.+?>(.+?)</div><div class=(.+?)>: <a target="_blank" title=(.+?) href=(.+?)>(.+?)</a>&nbsp; </div>', re.DOTALL).findall(r.content)
        for defi,cls,title,href2,name2 in match2:
            if name == title:
                addLink('%s: %s'%(defi,name2), href2, 'play',name2,name2+'_fanart', handle)