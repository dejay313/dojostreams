# -*- coding: utf-8 -*-


'''
  
    Copyright (C) 2016 

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
'''
import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os
try:
    import json
except:
    import simplejson as json
import yt
import shutil
import re,base64
import extract
import downloader
import time

ADDON_NAME = 'Dojo Streams'
addon_id = 'plugin.video.dojostreams'
Base_Url = 'http://herovision.x10host.com/dojo/'# the url of your server where your main php is
Main_Menu_File_Name = 'main.php'# the name of you main php here
search_filenames = ['dojo','','']#enter the names of the php files you want to include in search here
########################################################################################
### FAVOURITES SECTION IS NOT THIS AUTHORS CODE, I COULD NOT GET IT TO REMOVE FAVOURITES SO ALL CREDIT DUE TO THEM, SORRY IM NOT SURE WHERE IT CAME FROM BUT GOOD WORK :) ###
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
ADDON = xbmcaddon.Addon(id=addon_id)
ADDON_PATH = xbmc.translatePath('special://home/addons/'+addon_id)
text_file_path = ADDON_PATH + '/resources/'
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
PATH = 'DojoStreams'
VERSION = '0.0.3'
Dialog = xbmcgui.Dialog()
addon_data = xbmc.translatePath('special://home/userdata/addon_data/'+addon_id+'/')
favorites = os.path.join(addon_data, 'favorites.txt')
watched = addon_data + 'watched.txt'
debug = ADDON.getSetting('debug')
if os.path.exists(addon_data)==False:
    os.makedirs(addon_data)
if not os.path.exists(watched):
    open(watched,'w+')
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else: FAV = []
watched_read = open(watched).read()

def Main_Menu():
    OPEN = Open_Url(Base_Url+Main_Menu_File_Name)
    Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
    for url,icon,desc,fanart,name in Regex:
        if name == '[COLORred]Favourites[/COLOR]':
            Menu(name,url,6,icon,fanart,desc)	
        elif 'php' in url:
            Menu(name,url,1,icon,fanart,desc)


        else:
            Play(name,url,2,icon,fanart,desc)
    else:
        Menu('[COLORred]Builds Section[/COLOR]','',7,icon,fanart,desc)
        Menu('[COLORred]Dojo Search[/COLOR]',url,3,icon,fanart,desc)

    setView('tvshows', 'Media Info 3')			
	
def Second_Menu(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
    for url,icon,desc,fanart,name in Regex:
        Watched = re.compile('item="(.+?)"\n').findall(str(watched_read))
        for item in Watched:
            if item == url:
                name = '[COLORred]* [/COLOR]'+(name).replace('[COLORred]* [/COLOR][COLORred]* [/COLOR]','[COLORred]* [/COLOR]')
                print_text_file = open(watched,"a")
                print_text_file.write('item="'+name+'"\n')
                print_text_file.close
        if 'php' in url:
            Menu(name,url,1,icon,fanart,desc)
        else:
            Play(name,url,2,icon,fanart,desc)
    setView('tvshows', 'Media Info 3')







def Search():
    Search_Name = Dialog.input('Search Dojo', type=xbmcgui.INPUT_ALPHANUM)
    Search_Title = Search_Name.lower()
    if Search_Title == '':
        pass
    else:
		for file_Name in search_filenames:
			search_URL = Base_Url + file_Name + '.php'
			OPEN = Open_Url(search_URL)
			if OPEN != 'Opened':			
				Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
				for url,icon,desc,fanart,name in Regex:
					if Search_Title in name.lower():
						Watched = re.compile('item="(.+?)"\n').findall(str(watched_read))
						for item in Watched:
							if item == url:
								name = '[COLORred]* [/COLOR]'+(name).replace('[COLORred]* [/COLOR][COLORred]* [/COLOR]','[COLORred]* [/COLOR]')
								print_text_file = open(watched,"a")
								print_text_file.write('item="'+name+'"\n')
								print_text_file.close
						if 'php' in url:
							Menu(name,url,1,icon,fanart,desc)
						else:
							Play(name,url,2,icon,fanart,desc)
						
			setView('tvshows', 'Media Info 3')
#################################################WIZARD####################################################
def CATEGORIES():
    py_complete_name = os.path.join(text_file_path,'wizard.txt')
    print_default_file = open(py_complete_name,)
    file = print_default_file.read()
    match = re.compile('name=<(.+?)>.+?url=<(.+?)>.+?img=<(.+?)>.+?fanart=<(.+?)>.+?description=<(.+?)>',re.DOTALL).findall(file)
    print_default_file.close()
    for name,url,iconimage,fanart,description in match:
        NAME = name
        URL = url
        IMAGE = iconimage
        FANART = fanart
        DESC = description
        addDir(NAME,URL,1,IMAGE,FANART,DESC)

def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("Your Build Is Downloading","This May Take Several Minutes","", "")
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Installing Your Build Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("Your Media Centre", "[COLORred]Please Force Close Kodi To Take Effect If Pc Exit Task In TaskManager[/COLOR]","[COLORblue]Wizard Brought To You By DojoStreams[/COLOR]")

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok


####################################################################PROCESSES###################################################
def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = ''
    link = ''
    try: 
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    except: pass
    if link != '':
        return link
    else:
        link = 'Opened'
        return link

def setView(content, viewType):
	if content:
	    xbmcplugin.setContent(int(sys.argv[1]), content)
		
def Menu(name,url,mode,iconimage,fanart,description,showcontext=True,allinfo={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(('Remove from '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=5&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=4&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

		
def Play(name,url,mode,iconimage,fanart,description,showcontext=True,allinfo={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(('Remove from '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=5&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=4&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        


def resolve(url):
	print_text_file = open(watched,"a")
	print_text_file.write('item="'+url+'"\n')
	print_text_file.close
	import urlresolver
	try:
		resolved_url = urlresolver.resolve(url)
		xbmc.Player().play(resolved_url, xbmcgui.ListItem(name))
	except:
		try:
			xbmc.Player().play(url, xbmcgui.ListItem(name))
		except:
			xbmcgui.Dialog().notification("Sanctuary", "unplayable stream")
			sys.exit()

def addon_log(string):
    if debug == 'true':
        xbmc.log("["+ADDON_NAME+"]: %s" %(addon_version, string))

def addFavorite(name,url,iconimage,fanart,mode,playlist=None,regexs=None):
        favList = []
        try:
            # seems that after
            name = name.encode('utf-8', 'ignore')
        except:
            pass
        if os.path.exists(favorites)==False:
            addon_log('Making Favorites File')
            favList.append((name,url,iconimage,fanart,mode,playlist,regexs))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            addon_log('Appending Favorites')
            a = open(favorites).read()
            data = json.loads(a)
            data.append((name,url,iconimage,fanart,mode))
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()
		

def getFavorites():
        if os.path.exists(favorites)==False:
            favList = []
            addon_log('Making Favorites File')
            favList.append(('[COLORred]Dojo Streams Favourites Section[/COLOR]','','','','','',''))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()        
        else:
			items = json.loads(open(favorites).read())
			total = len(items)
			for i in items:
				name = i[0]
				url = i[1]
				iconimage = i[2]
				try:
					fanArt = i[3]
					if fanArt == None:
						raise
				except:
					if ADDON.getSetting('use_thumb') == "true":
						fanArt = iconimage
					else:
						fanArt = fanart
				try: playlist = i[5]
				except: playlist = None
				try: regexs = i[6]
				except: regexs = None

				if i[4] == 0:
					Menu(name,url,'',iconimage,fanart,'','fav')
				else:
					Menu(name,url,i[4],iconimage,fanart,'','fav')

def rmFavorite(name):
        data = json.loads(open(favorites).read())
        for index in range(len(data)):
            if data[index][0]==name:
                del data[index]
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
                break
        xbmc.executebuiltin("XBMC.Container.Refresh")	
	
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2: 
                params=sys.argv[2] 
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}    
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
params=get_params()
url=None
name=None
iconimage=None
mode=None
fanart=None
description=None
fav_mode=None


try:
    fav_mode=int(params["fav_mode"])
except:
    pass

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
#####################################################END PROCESSES##############################################################		
		
if mode == None: Main_Menu()
elif mode == 1 : Second_Menu(url)
elif mode == 2 :     
    if 'youtube' in url:
        url = (url).replace('https://www.youtube.com/watch?v=','').replace('http://www.youtube.com/watch?v=','')
        yt.PlayVideo(url)
    else:
    	resolve(url)
elif mode == 3 : Search()
elif mode==4:
    addon_log("addFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,iconimage,fanart,fav_mode)
elif mode==5:
    addon_log("rmFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)
elif mode==6:
    addon_log("getFavorites")
    getFavorites()

if mode==7:
    CATEGORIES()

elif mode==8:
    wizard(name,url,description)


xbmcplugin.addSortMethod(int(sys.argv[1]), 1)
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
