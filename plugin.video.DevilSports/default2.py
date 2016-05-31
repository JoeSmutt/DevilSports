import sys
import urllib, urllib2
import urlparse
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os

import xml.etree.ElementTree as ET

from resources.lib import parser

base_url = sys.argv[0]
settings = xbmcaddon.Addon(id='plugin.video.DevilSports')
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'video')

################################
### Favorites / History Folders
################################
profile = xbmc.translatePath(settings.getAddonInfo('profile').decode('utf-8'))
favorites = os.path.join(profile, 'favorites')
history = os.path.join(profile, 'history')
if not os.path.exists(favorites): os.makedirs(favorites)
if not os.path.exists(history): os.makedirs(history)

def addon_log(string):
    try:
        xbmc.log("[DevilSports Lists-%s]: %s" %('0.0.1', string))
    except:
        pass

def addDir(name,url,mode,icon,fanart):
    addon_log('Adding Directories')
    url = base_url + '?' + urllib.urlencode({'mode': mode, 'foldername': name, 'url':url,'fanart':fanart})
    li = xbmcgui.ListItem(name, iconImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

def addLink(name,url,image,urlType,fanart):
    addon_log('Adding Links')
    li = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
    li.setInfo( type="Video", infoLabels={ "Title": name } )
    li.setProperty('IsPlayable','true')
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=li, isFolder=False)

def getRequest(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data
    except urllib2.URLError, e:
        addon_log('URL: '+url)
        if hasattr(e, 'code'):
            addon_log('We failed with error code - %s.' % e.code)
            xbmc.executebuiltin("XBMC.Notification(DevilSports,We failed with error code - "+str(e.code)+",10000,"+icon+")")
        elif hasattr(e, 'reason'):
            addon_log('We failed to reach a server.')
            addon_log('Reason: %s' %e.reason)
            xbmc.executebuiltin("XBMC.Notification(DevilSports,We failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")

def getXML(url):
    try:
        addon_log('Getting XML Data')
        req = getRequest(url)
        elems = ET.fromstring(req)
        for channels in elems.findall('channel'):
            nm = channels.findtext( "name" )
            ul = channels.findtext( "url" )
            thumb = channels.findtext( "thumbnail" )
            fan = channels.findtext( "fanart" )
            md = channels.findtext( "mode" )
            addDir(nm,ul,md,thumb,fan)
    except ET.ParseError, e:
        addon_log('We failed with error code - %s.' % e.code)

def getSite(url, loc):
    
    addon_log('Getting Site Data')
    site_data = getRequest(url)
      
    addon_log('Getting Site Configs')
    domain = parser.parseurl(url)
    cfg = parser.loadCFG(domain, loc)
    
    
    
    
    
    try:   
        configs = ET.fromstring(cfg)
               
        #go through all patterns and
        for pattern in configs.findall('item'):
            pat = pattern.findtext('item_pattern') # this is your pattern
            orde = pattern.findtext('item_order').split('|')
            
            match = parser.FindPattern(site_data, pat)
            
            for (orde) in match:
                addDir(orde[0],orde[1],'play','','')
        
        
        
        
    except:
        addon_log('Error')
        
        
def getFavorites():
    if not os.path.isfile(os.path.join(favorites, 'fav.xml')):
        tmp = open(os.path.join(favorites, 'fav.xml'), 'w')
        tmp.close
        
    addon_log('Getting Favorites list')
    try:
        tree = ET.parse(os.path.join(favorites, 'fav.xml'))
        root = tree.getroot()
        for favs in root.findall('favorite'):
                nm = favs.findtext( "name" )
                ul = favs.findtext( "url" )
                thumb = favs.findtext( "thumbnail" )
                fan = favs.findtext( "fanart" )
                md = favs.findtext( "mode" )
                addDir(nm,ul,md,thumb,fan)
    except:
        pass

def addFavorite(nme,urls,iconimage,fan,md,playlist=None,regexs=None):
    if not os.path.isfile(os.path.join(favorites, 'fav.xml')):
        tmp = open(os.path.join(favorites, 'fav.xml'), 'w')
        tmp.close
        
    addon_log('Adding Favorites list')
    try:
        tree = ET.parse(os.path.join(favorites, 'fav.xml'))
        root = tree.getroot()
        
        if not root.tag == "favorites":
            favs = ET.Element('favorates')
            fav = ET.SubElement(favs, 'favorite')
            name = ET.SubElement(fav, 'name')
            name.text = nme
            url = ET.SubElement(fav, 'url')
            url.text = urls
            thumbnail = ET.SubElement(fav,'thumbnail')
            thumbnail.text = iconimage
            fanart = ET.SubElement(fav,'fanart')
            fanart.text = fan
            mode = ET.SubElement(fav,'mode')
            mode.text = md

        else:
            fav = ET.Element('favorite')
            name = ET.SubElement(fav, nme)
            url = ET.SubElement(fav, urls)
            thumbnail = ET.SubElement(fav, iconimage)
            fanart = ET.SubElement(fav, fan)
            mode = ET.SubElement(fav, md)
            ET.dump(fav)
            
    except:
        pass
    




mode = args.get('mode', None)

if mode is None:
    addDir('Favorites','favorites','favorites','','FANART')
    getXML( settings.getSetting('mainurl') + settings.getSetting('mainxml') )
    
elif mode[0] == 'xml':
    getXML(args['url'][0])

elif mode[0] == 'site':
    getSite(args['url'][0], 'live')
    
elif mode[0] == 'site1':
    getSite(args['url'][0], 'custom')

elif  mode[0] == 'favorites':
    getFavorites()

elif mode[0] == 'addFavorite':
    addon_log("addFavorite")

else:
    addon_log("Error No Mode Given")
    
xbmcplugin.endOfDirectory(addon_handle)