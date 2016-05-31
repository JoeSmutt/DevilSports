import xbmc, xbmcaddon
import urllib, urllib2
import urlparse
import re
import xml.etree.ElementTree as ET

settings = xbmcaddon.Addon(id='plugin.video.DevilSports')

def addon_log(string):
    try:
        xbmc.log("[DevilSports Lists-%s]: %s" %('0.0.1', string))
    except:
        pass
    
def loadURL(url):
    try:
        sock = urllib.urlopen(url)
        htmlSource = sock.read().decode('utf-8')
        sock.close()
        return htmlSource
    except:
        addon_log('Page cannot be found:' + url)

def loadCFG(site, loc):
    cfgurl = settings.getSetting('mainurl') + loc + "/" + parseurl(site) + "/config.xml"
    addon_log(cfgurl)
    data = loadURL(cfgurl)
    return data

def FindPattern(text,pattern):
    result = ""
    try:    
        matches = re.compile(pattern, re.DOTALL).findall(text)
        result = matches
    except:
        result = ""
    return result

def parseurl(url):
    domain = url.replace('http://', '').split('.')
    if domain[0] == 'www':
        return domain[1]
    else:
        return domain[0]
