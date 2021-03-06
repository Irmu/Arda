
import requests,xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys,logging
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")
Addon = xbmcaddon.Addon()
from os import listdir
import string
from os.path import isfile, join
import time,random
import threading,json
global break_jump,silent,clicked,selected_index,clicked_id,po_watching,l_full_stats,all_w_global

all_w_global={}
l_full_stats=''
po_watching=''
clicked_id=''
selected_index=-1
clicked=False
silent=False
break_jump=0
global list_index,str_next,sources_searching
sources_searching=False
str_next=''
list_index=999

addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
lang=xbmc.getLanguage(0)
from resources.modules.public import addNolink,addDir3,addLink,lang,user_dataDir,pre_mode
from resources.modules.trakt import progress_trakt,get_trakt,get_trk_data,trakt_liked
from  resources.modules import cache
from resources.modules.general import fix_q,post_trakt,base_header,BASE_LOGO,clean_name
from resources.modules import real_debrid,premiumize,all_debrid
global playing_text
playing_text=''
ACTION_PLAYER_STOP = 13
ACTION_BACK          = 92
ACTION_NAV_BACK =  92## Backspace action
ACTION_PARENT_DIR    = 9
ACTION_PREVIOUS_MENU = 10
ACTION_CONTEXT_MENU  = 117
ACTION_C_KEY         = 122

ACTION_LEFT  = 1
ACTION_RIGHT = 2
ACTION_UP    = 3
ACTION_DOWN  = 4
domain_s='https://'
COLOR1         = 'gold'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
from resources.modules.tmdb import html_g_movie
def TrkBox_help(title, msg,img2="https://user-images.githubusercontent.com/19761269/63175338-6af03a80-c061-11e9-9ff3-009778fa0a9c.png"):
    class TextBoxes1(xbmcgui.WindowXMLDialog):
        def onInit(self):
            
            self.title      = 101
            self.msg        = 102
            self.scrollbar  = 103
            self.okbutton   = 201
            
            self.imagecontrol=202
            self.sync   = 203
            self.y=0
            self.showdialog()
            self.params=False
            
        def showdialog(self):
            import random
            self.getControl(self.title).setLabel(title)
            self.getControl(self.msg).setText(msg)
            self.getControl(self.imagecontrol).setImage(img2)
            self.setFocusId(self.scrollbar)
            
            xbmc.executebuiltin("Dialog.Close(busydialog)")
        def onClick(self, controlId):
            if (controlId == self.okbutton):
               
                self.close()
            if (controlId == self.sync):
                self.params=True
                self.close()
        def onAction(self, action):
            if   action == ACTION_PREVIOUS_MENU: 
               
                self.close()
            elif action == ACTION_NAV_BACK: 
                    
                    self.close()
            
            
    tb = TextBoxes1( "Trktbox.xml" , Addon.getAddonInfo('path'), 'DefaultSkin', title=title, msg=msg)
    tb.doModal()
    pr=tb.params
    del tb
    return pr
def stop_play():
    KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
    if KODI_VERSION>17:
        return 'forceexit'
    else:
        return 'return'
    
def contact(title='',msg=""):
	class MyWindow(xbmcgui.WindowXMLDialog):
		def __init__(self, *args, **kwargs):
			self.title = THEME3 % kwargs["title"]
			self.image = kwargs["image"]
			self.fanart = kwargs["fanart"]
			self.msg = THEME2 % kwargs["msg"]

		def onInit(self):
			self.fanartimage = 101
			self.titlebox = 102
			self.imagecontrol = 103
			self.textbox = 104
			self.scrollcontrol = 105
			self.button = 199
			self.showdialog()

		def showdialog(self):
			self.getControl(self.imagecontrol).setImage(self.image)
			self.getControl(self.fanartimage).setImage(self.fanart)
			self.getControl(self.fanartimage).setColorDiffuse('9FFFFFFF')
			self.getControl(self.textbox).setText(self.msg)
			self.getControl(self.titlebox).setLabel(self.title)
            
	
		
            
			self.setFocusId(self.button)
			
		def onAction(self,action):
			if   action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

	cw = MyWindow( "Contact.xml" , Addon.getAddonInfo('path'), 'DefaultSkin', title=title, fanart=' ', image='https://images4.alphacoders.com/292/292448.jpg', msg=msg)
	cw.doModal()
	del cw
def get_html(url):
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    html=requests.get(url,headers=headers)
    try:
        html=json.loads(html.content)
    except:
        html=html.content
    return html
class Chose_ep(xbmcgui.WindowXMLDialog):

    def __new__(cls, addonID, heb_name,name, id,season,episode,dates,original_title):
        FILENAME='chose_ep.xml'
        return super(Chose_ep, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID,heb_name,name, id,season,episode,dates,original_title):
        super(Chose_ep, self).__init__()
        
        self.labelcontrol1=1020
        self.labelcontrol2=1021
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.season=season
        self.original_title=original_title
        self.id=id
        self.episode=episode
        self.heb_name=heb_name
        self.name=name
        self.dates=dates
        self.imagess=[]
        self.plotss=[]
        self.labelss=[]
        self.labelss1=[]
    def onInit(self):
        url='https://api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(self.id,self.season)
        
        html=cache.get(get_html,24,url, table='posters')
        try:
            maste_image=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
        except:
            maste_image=''
        master_plot=html['overview']
       
        master_name=html['name']
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode)+1)))
     
        match = dbcur.fetchone()
        color_next='white'
        if match!=None:
           color_next='magenta'
        
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode))))
     
        match = dbcur.fetchone()
        color_current='white'
        
        if match!=None:
           color_current='magenta'
           
           
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode)-1)))
     
        match = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        color_prev='white'
        if match!=None:
           color_prev='magenta'
           
        height=1100
        self.getControl(5001).setHeight(height)
            
        self.list = self.getControl(3000)
        self.list.setHeight(height)

        newY = 360 - (height/2)

        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)

        self.params    = None
        self.paramList = []
        
        all_d=json.loads(urllib.unquote_plus(self.dates))
        
        if len(all_d)<2:
            all_d=['','','']
            
        if all_d[0]==0:
            #next ep
            if len(html['episodes'])>int(self.episode):
                items=html['episodes'][int(self.episode)]
                title='[COLOR %s]'%color_next+items['name']+'[/COLOR]'
                
                plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
                
                image=maste_image
                if items['still_path']!=None:
                    image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
                self.imagess.append(image)
                title=title+ '- Episode '+str(int(self.episode)+1)
                self.labelss.append(title)
                liz   = xbmcgui.ListItem(title)
                liz.setProperty('title_type', 'Play the next episode - '+all_d[2])
                self.labelss1.append('Play the next episode - '+all_d[2])
                
                liz.setProperty('image', image)
                liz.setProperty('description',plot)
                self.plotss.append(plot)
                

                
                self.list.addItem(liz)
            else:
                liz   = xbmcgui.ListItem(' Episode '+str(int(self.episode)+1))
                liz.setProperty('title_type', 'Play the next episode - '+all_d[2])
                self.labelss1.append('Play the next episode  - '+all_d[2])
                
                liz.setProperty('image', '')
                liz.setProperty('description','')
                self.plotss.append('')
                

                
                self.list.addItem(liz)
            #current ep
            items=html['episodes'][int(self.episode)-1]
            title='[COLOR %s]'%color_current+items['name']+'[/COLOR]'
            plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
            image=maste_image
            if items['still_path']!=None:
                image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
            self.imagess.append(image)
            title=title+ '- Episode '+self.episode
            self.labelss.append(title)
     
                
            
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play Current episode - '+all_d[1])
            self.labelss1.append('Play Current episode - '+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            

            self.list.addItem(liz)
            

            
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', "Open Season's episodes")
            self.labelss1.append("Open Season's episodes")
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            
            #season ep
            
            title=self.heb_name
            title.replace('%20',' ')
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Open season selection')
            self.labelss1.append('Open season selection')
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #choise=['Play next episode - '+all_d[2],'Play current episode - '+all_d[1],'Open season episodes','Open season selection']
        elif all_d[2]==0:
            
            
            #current ep
            items=html['episodes'][int(self.episode)-1]
            title='[COLOR %s]'%color_current+items['name']+'[/COLOR]'
            plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
            image=maste_image
            if items['still_path']!=None:
                image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
            self.imagess.append(image)
            title=title+ 'Episode - '+self.episode
                
            
                
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play current episode - '+all_d[1])
            self.labelss1.append('Play current episode - '+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            
            self.list.addItem(liz)
            
            #prev ep
            items=html['episodes'][int(self.episode)-2]
            title='[COLOR %s]'%color_prev+items['name']+'[/COLOR]'
            plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
            image=maste_image
            if items['still_path']!=None:
                image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
            self.imagess.append(image)
            title=title+ '- Episode '+str(int(self.episode)-1)
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play previous episode - '+all_d[0])
            self.labelss1.append( 'Play previous episode - '+all_d[0])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
          

            
            self.list.addItem(liz)
            
            
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', "Open Season's episodes")
            self.labelss1.append("Open Season's episodes")
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #season ep
            
            title=self.heb_name
            title.replace('%20',' ')
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Open season selection')
            self.labelss1.append('Open season selection')
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)
 

            self.list.addItem(liz)
            #choise=['Play current episode - '+all_d[1],'Play previous episode - '+all_d[0],'Open season episodes','Open season selection']
        else:
            #next ep
            if len(html['episodes'])>int(self.episode):
                items=html['episodes'][int(self.episode)]
                title='[COLOR %s]'%color_next+items['name']+'[/COLOR]'
                plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
                image=maste_image
                if items['still_path']!=None:
                    image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
                self.imagess.append(image)
                title=title+ '- Episode '+str(int(self.episode)+1)
                self.labelss.append(title)
                liz   = xbmcgui.ListItem(title)
                if 'magenta' not in all_d[2]:
                
                    liz.setProperty('title_type', 'Play next episode - '+all_d[2])
                    self.labelss1.append('Play next episode - '+all_d[2])
                else:
                    liz.setProperty('title_type', '[COLOR magenta]'+'Play next episode - '+'[/COLOR]'+all_d[2])
                    self.labelss1.append('[COLOR magenta]'+'Play next episode - '+'[/COLOR]'+all_d[2])
                liz.setProperty('image', image)
                liz.setProperty('description',plot)
                self.plotss.append(plot)
                

                
                self.list.addItem(liz)
            else:
                liz   = xbmcgui.ListItem(' Episode '+str(int(self.episode)+1))
                liz.setProperty('title_type', 'Play next episode - '+all_d[2])
                self.labelss1.append('Play next episode - '+all_d[2])
                
                liz.setProperty('image', '')
                liz.setProperty('description','')
                self.plotss.append('')
                
                
                self.list.addItem(liz)
            #current ep
            if len(html['episodes'])>(int(self.episode)-1):
                items=html['episodes'][int(self.episode)-1]
                title='[COLOR %s]'%color_current+items['name']+'[/COLOR]'
                plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
                image=maste_image
                if items['still_path']!=None:
                    image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
                self.imagess.append(image)
                title=title+ '- Episode '+str(int(self.episode))
                    
            else:
                title='- Episode '+self.episode
                plot=''
                image=maste_image
                

            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play current episode - '+all_d[1])
            self.labelss1.append('Play current episode - '+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            
            self.list.addItem(liz)
            
            #prev ep
            if len(html['episodes'])>(int(self.episode)-2):
                items=html['episodes'][int(self.episode)-2]
                title='[COLOR %s]'%color_prev+items['name']+'[/COLOR]'
                plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
                image=maste_image
                if items['still_path']!=None:
                    image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
                self.imagess.append(image)
                title=title+ '- Episode '+str(int(self.episode)-1)
                self.labelss.append(title)
            else:
                title='- Episode '+str(int(self.episode)-1)
                plot=''
                image=maste_image
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play previous episode - '+all_d[0])
            self.labelss1.append('Play previous episode - '+all_d[0])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
          

            
            self.list.addItem(liz)
                
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', "Open Season's episodes")
            self.labelss1.append("Open Season's episodes")
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #season ep
            
            title=self.heb_name
            title=title.replace('%20',' ')
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Open season selection')
            self.labelss1.append('Open season selection')
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            

           



        self.setFocus(self.list)
        self.getControl(self.imagecontrol).setImage(self.imagess[0])
        self.getControl(self.bimagecontrol).setImage(maste_image)
        self.getControl(self.txtcontrol).setText(self.plotss[0])
        
        self.getControl(self.labelcontrol1).setLabel (self.labelss1[0])
        self.getControl(self.labelcontrol2).setLabel (self.labelss[0])
           
    def onAction(self, action):  
        actionId = action.getId()
        try:
            self.getControl(self.imagecontrol).setImage(self.imagess[self.list.getSelectedPosition()])
            self.getControl(self.txtcontrol).setText(self.plotss[self.list.getSelectedPosition()])
            self.getControl(self.labelcontrol1).setLabel (self.labelss1[self.list.getSelectedPosition()])
            self.getControl(self.labelcontrol2).setLabel (self.labelss[self.list.getSelectedPosition()])
        except:
            pass
        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = -1
            xbmc.sleep(100)
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            self.params = -1
            return self.close()


    def onClick(self, controlId):
        
        if controlId != 3001:
        
            index = self.list.getSelectedPosition()        
            
           
            #self.getControl(self.txtcontrol).setText(self.plotss[index])
            try:    self.params = index
            except: self.params = None

        self.close()
        

    def onFocus(self, controlId):
        pass

def selection_time(title,choose_time):
    from  resources.modules import pyxbmct
    class selection_time(pyxbmct.AddonDialogWindow):
        
        def __init__(self, title='',item=''):
           
            super(selection_time, self).__init__(title)
            self.item=[item,'Start over']
            self.setGeometry(350, 150,1, 1,pos_x=700, pos_y=200)
            self.list_index=-1

            
            
            self.set_active_controls()
            self.set_navigation()
            # Connect a key action (Backspace) to close the window.
            self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
           

        
        def get_selection(self):
            """ get final selection """
            return self.list_index
        def click_list(self):
           
            self.list_index=self.list.getSelectedPosition()
           
            self.close()
        
        def set_active_controls(self):
         
          
            # List
            self.list = pyxbmct.List()
            self.placeControl(self.list, 0,0,  rowspan=2, columnspan=1)
            # Add items to the list
            
           
            self.list.addItems(self.item)
            
            # Connect the list to a function to display which list item is selected.
            self.connect(self.list, self.click_list)
            
           

        def set_navigation(self):
            
            self.setFocus(self.list)

        

        

        def setAnimation(self, control):
            # Set fade animation for all add-on window controls
            control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=50',),
                                    ('WindowClose', 'effect=fade start=100 end=0 time=50',)])
    window = selection_time(title,choose_time)
    window.doModal()
    selection = window.get_selection()
    del window
    return selection
class ContextMenu_new2(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID, menu,icon,fan,txt,results,po_watching,l_full_stats):
        #FILENAME='contextmenu_new2.xml'
        #if Addon.getSetting("new_window_type2")=='4':
        FILENAME='contextmenu_new3.xml'
        
        return super(ContextMenu_new2, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID, menu,icon,fan,txt,results,po_watching,l_full_stats):
        global playing_text,selected_index
        logging.warning('Init')
        super(ContextMenu_new2, self).__init__()
        self.menu = menu
        self.auto_play=0
        selected_index=-1
        self.po_watching=po_watching
        self.l_full_stats=l_full_stats
        self.results=results
        self.params    = 666666
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.tick_label=6001
        self.icon=icon
        self.fan=fan
        self.text=txt
        playing_text=''
        self.tick=60
        self.done=0
        self.story_gone=0
        self.count_p=0
        self.keep_play=''
        self.tick=60
        self.s_t_point=0
        self.start_time=time.time()
        logging.warning('dInit')
    def background_work(self):
        global playing_text,mag_start_time_new,now_playing_server,done1_1
        tick=0
        tick2=0
        changed=1
        vidtime=0
        while(1):
            
            all_t=[]
            for thread in threading.enumerate():
                if ('tick_time' in thread.getName()) or ('background_task' in thread.getName()) or ('get_similer' in thread.getName()) or ('MainThread' in thread.getName()) or ('sources_s' in thread.getName()):
                    continue
                
                if (thread.isAlive()):
                    all_t.append( thread.getName())
            self.getControl(606).setLabel(','.join(all_t))
            if  xbmc.getCondVisibility('Window.IsActive(busydialog)'):
                self.getControl(102).setVisible(True)
                if tick2==1:
                    self.getControl(505).setVisible(True)
                    tick2=0
                else:
                    self.getControl(505).setVisible(False)
                    tick2=1
            else:
                self.getControl(102).setVisible(False)
                self.getControl(505).setVisible(False)
            if len(playing_text)>0 or  self.story_gone==1 :
                changed=1
                vidtime=0
                if xbmc.Player().isPlaying():
                    vidtime = xbmc.Player().getTime()
                
                t=time.strftime("%H:%M:%S", time.gmtime(vidtime))
                
                if len(playing_text)==0:
                    playing_text=self.keep_play
                try:
                    self.keep_play=playing_text
                    self.getControl(self.txtcontrol).setText(t+'\n'+playing_text.split('$$$$')[0]+'\n'+now_playing_server.split('$$$$')[0]+'\n'+now_playing_server.split('$$$$')[1])
                    if vidtime == 0:
                        if tick==1:
                            self.getControl(303).setVisible(True)
                            tick=0
                        else:
                            self.getControl(303).setVisible(False)
                            tick=1
                except Exception as e:
                    logging.warning('Skin ERR:'+str(e))
                    self.params = 888
                    self.done=1
                    logging.warning('Close:4')
                    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                    done1_1=3
                    self.close()
                    pass
            
            elif changed==1:
                    changed=0
                
                    self.getControl(303).setVisible(False)
                    self.getControl(self.txtcontrol).setText(self.text)
            
            if self.done==1:
                break
            if xbmc.Player().isPlaying():
                self.tick=60
                self.count_p+=1
                self.st_time=0
                
                vidtime = xbmc.Player().getTime()
                if self.s_t_point==0:
                    
                    
                    if vidtime > 0:
                        self.getControl(3000).setVisible(False)
                        self.getControl(self.imagecontrol).setVisible(False)
                        self.getControl(505).setVisible(False)
                        self.getControl(909).setPosition(1310, 40)
                        self.getControl(2).setPosition(1310, 100)
                        self.s_t_point=1
                        self.getControl(303).setVisible(False)
                        self.story_gone=1
                        logging.warning('Change seek Time:'+str(mag_start_time_new))
                        try:
                            if int(float(mag_start_time_new))>0:
                                xbmc.Player().seekTime(int(float(mag_start_time_new)))
                        except:
                            pass
                
                if vidtime > 0:
                    playing_text=''
     
                try:
                    value_d=(vidtime-(int(float(mag_start_time_new)))) 
                except:
                    value_d=vidtime
                play_time=int(Addon.getSetting("play_full_time"))
                if value_d> play_time and self.s_t_point>0:
                    self.params = 888
                    self.done=1
                    logging.warning('Close:1')
                    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                    done1_1=3
                    self.close()
              
                if self.count_p>(play_time+30) :
                   if Addon.getSetting("play_first")!='true':
                   
                    self.params = 888
                    self.done=1
                    logging.warning('Close:3')
                    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                    done1_1=3
                    self.close()
            else:
                self.count_p=0
                self.s_t_point=0
                self.getControl(3000).setVisible(True)
         
                #self.getControl(505).setVisible(True)
                self.getControl(self.imagecontrol).setVisible(True)
                self.story_gone=0
                self.getControl(2).setPosition(1310, 700)
                self.getControl(909).setPosition(1310, 10)
            xbmc.sleep(1000)
    def tick_time(self):
        global done1_1
        while(self.tick)>0:
            self.getControl(self.tick_label).setLabel(str(self.tick))
            self.tick-=1
            
            if self.params == 888:
                break
            xbmc.sleep(1000)
        if self.params != 888:
            self.params = 888
            self.done=1
            logging.warning('Close:93')
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            done1_1=3
            self.close()
    def fill_table(self,all_his_links):
        logging.warning('Start Fill')
        count=0
        self.paramList = []
        all_liz_items=[]
        logging.warning('Fil table start')
        from resources.modules import PTN
        
        
        try:
            for item in self.menu:
                
                info=(PTN.parse(item[4].replace('[COLOR red][I]','').replace('[/I][/COLOR]','').replace('[COLOR lightblue][B]','').replace('[COLOR khaki][B]','').replace('[/B][/COLOR]\n','').replace('-','.')))
                
                add_d=[]
                
                
                counter_page=0
                nxt=0
                for key in info:
                    if type(info[key])==list:
                        info_key=','.join(info[key])
                    else:
                        info_key=str(info[key])
                    if key=='language':
                        color='pink'
                    else:
                        color='khaki'
                    nxt+=1
                    if 'Open filtered links' not in item[4]:
                        if nxt>2:
                            nxt=0
                            item[4]=item[4]+' - [COLOR lightblue]'+key+'[/COLOR]: [COLOR %s]'%color+info_key+'[/COLOR]\n'
                        else:
                            
                            item[4]=item[4]+' - [COLOR lightblue]'+key+'[/COLOR]: [COLOR %s]'%color+info_key+'[/COLOR]'
                    
               
                self.getControl(202).setLabel(str(((count*100)/len(self.menu))) + '% Please Wait ')
                count+=1
                self.paramList.append(item[6])
                '''
                info=(PTN.parse(item[0]))
                if 'excess' in info:
                    if len(info['excess'])>0:
                        item[0]='.'.join(info['excess'])
                '''
                golden=False
                if 'Cached ' in item[0]:
                    golden=True
                item[0]=item[0].replace('Cached ','')
                
                title ='[COLOR deepskyblue][B]'+item[0] +'[/B][/COLOR]'
                if len(item[1].strip())<2:
                    item[1]='--'
                if len(item[2].strip())<2:
                    item[2]='--'
                if len(item[3].strip())<2:
                    item[3]='--'
                if len(item[4])<2:
                    item[4]='--'
                if len(item[5])<2:
                    item[5]='--'
                server=item[1]
                pre_n='[COLOR khaki]'+item[2]+'[/COLOR]'
                q=item[3]
                supplay=item[4]
                size='[COLOR coral]'+item[5]+'[/COLOR]'
                link=item[6]
                
                
                
               
                
                if q=='2160':
                    q='4k'
                if q.lower()=='hd':
                    q='unk'
                liz   = xbmcgui.ListItem(title)
                liz.setProperty('server', '')#server
                liz.setProperty('pre',pre_n)
                logging.warning(q)
                liz.setProperty('Quality', q)
                liz.setProperty('supply', supplay)
                liz.setProperty('size', size)
                #if item[6].encode('base64') in all_his_links:
                #    liz.setProperty('history','100')
                
                liz.setProperty('server_v','100')
                #if item[7]==True or ('magnet' in server and allow_debrid):
                #    liz.setProperty('rd', '100')
                if golden:
                    liz.setProperty('magnet', '200')
                
                elif 'magnet' in server:
                    liz.setProperty('magnet', '100')
                all_liz_items.append(liz)
            logging.warning(' Done Loading')
            self.getControl(202).setLabel('')
            self.list.addItems(all_liz_items)

            self.setFocus(self.list)
            logging.warning('Fil table End')
        except Exception as e:
            logging.warning('Fill error:'+str(e))
            import linecache
            sources_searching=False
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logging.warning('Fill error:'+str(lineno))
            logging.warning('inline:'+line)
            logging.warning('Error:'+str(e))
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'inLine:'+str(lineno))))
            self.close()
           
    def onInit(self):
        logging.warning('Start')
        xbmc.Player().stop()
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        #dbcur.execute("SELECT * FROM historylinks")
        #all_his_links_pre = dbcur.fetchall()
        all_his_links=[]
        #for link,status,option in all_his_links_pre:
        #    all_his_links.append(link)
        thread=[]
        #thread.append(Thread(self.background_work))
        #thread[len(thread)-1].setName('background_task')
        #thread.append(Thread(self.tick_time))
        #thread[len(thread)-1].setName('tick_time')
        logging.warning('Fill table')
        
        thread.append(Thread(self.fill_table,all_his_links))
        thread[len(thread)-1].setName('fill_table')
        logging.warning('trd s')
        thread[0].start()
        #thread[1].start()
        #thread[2].start()
        line   = 38
        spacer = 20
        delta  = 0 
        logging.warning('1')
        nItem = len(self.menu)
        if nItem > 16:
            nItem = 16
            delta = 1
        logging.warning('2')
        self.getControl(self.imagecontrol).setImage(self.icon)
        self.getControl(self.bimagecontrol).setImage(self.fan)
        logging.warning('3')
        if len(playing_text)==0:
            self.getControl(self.txtcontrol).setText(self.text)
        height = (line+spacer) + (nItem*line)
        height=1100
        self.getControl(5001).setHeight(height)
        logging.warning('4')
        self.list = self.getControl(3000)
        self.list.setHeight(height)
        logging.warning('5')
        newY = 360 - (height/2)

        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)
        self.getControl(999).setLabel(self.results)
        self.getControl(888).setLabel(self.po_watching)
        logging.warning('self.l_full_stats:'+str(self.l_full_stats))
        self.getControl(777).setLabel(self.l_full_stats)
        
        logging.warning('Loading')
        
        
            
           
    def played(self):
        self.params =7777
    def onAction(self, action):  
        global done1_1,selected_index
        actionId = action.getId()
        #logging.warning('actionId:'+str(actionId))
        self.tick=60
        #logging.warning('ACtion:'+ str(actionId))
        
            
        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            logging.warning('Close:5')
            self.params = 888
            selected_index=-1
            
            self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK,ACTION_NAV_BACK]:
            self.params = 888
            selected_index=-1
            self.close()

    
    def onClick(self, controlId):
        global playing_text,done1_1,selected_index
        self.tick=60
        
        if controlId != 3001:
            '''
            self.getControl(3000).setVisible(False)
            self.getControl(102).setVisible(False)
            self.getControl(505).setVisible(False)
            self.getControl(909).setPosition(1310, 40)
            self.getControl(2).setPosition(1310, 100)
            self.getControl(self.imagecontrol).setVisible(False)
            self.getControl(303).setVisible(False)
            self.story_gone=1
            '''
            index = self.list.getSelectedPosition()        
            
            try:    
                self.params = index
                logging.warning('Clicked:'+str(controlId)+':'+str(index))
            except:
                self.params = None
            #playing_text=''
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            selected_index=self.params
            self.close()
            #return self.params
        else:
            logging.warning('Close:7')
            selected_index=-1
            self.close()
        
    def close_now(self):
        global done1_1
        logging.warning('Close:8')
        self.params = 888
        self.done=1
        xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
        xbmc.sleep(1000)
        logging.warning('Close now CLosing')
        done1_1=3
        self.close()
    def onFocus(self, controlId):
        pass
def show_updates(force=False):
    
    
    from shutil import copyfile
    version = Addon.getAddonInfo('version')
    ms=False
    if not os.path.exists(os.path.join(user_dataDir, 'version.txt')):
        ms=True
    else:
        file = open(os.path.join(user_dataDir, 'version.txt'), 'r') 
        file_data= file.readlines()
        file.close()
        if version not in file_data:
          ms=True
    if force==True:
        ms=True
    if ms:
        current_folder = os.path.dirname(os.path.realpath(__file__))
        change_log=os.path.join(current_folder,'changelog.txt')
        file = open(change_log, 'r') 
        news= file.read()
        file.close()
        
        
        contact(title='Welcome to version -'+version ,msg=news)
        file = open(os.path.join(user_dataDir, 'version.txt'), 'w') 
        file.write(version)
        file.close()
        ClearCache()
       
       
class fav_mv(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID,id):
        
        FILENAME='moviefavorite.xml'
        
        return super(fav_mv, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID,id):
        super(fav_mv, self).__init__()
        self.id=id
        self.all_d={}
        self.closenow=0
        try:
            self.time_c=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
        except:
            self.time_c=30
        
        #Thread(target=self.background_task).start()
        
        #Thread(target=self.get_similer).start()
    
    def onInit(self):
        a=1
        self.setFocus(self.getControl(201))
        x='http://api.themoviedb.org/3/movie/%s/recommendations?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(self.id,lang)
        html=requests.get(x).json()
        loc=random.randint(0,len(html['results'])-1)
        self.all_d={}
        self.all_d['title']=html['results'][loc]['title']
        if 'poster_path' in html['results'][loc]:
            if html['results'][loc]['poster_path']!=None:
                self.all_d['icon']='https://image.tmdb.org/t/p/original/'+html['results'][loc]['poster_path']
            else:
                self.all_d['icon']=' '
                
       
        if 'backdrop_path' in html['results'][loc]:
            if html['results'][loc]['backdrop_path']!=None:
                self.all_d['fan']='https://image.tmdb.org/t/p/original/'+html['results'][loc]['backdrop_path']
            else:
                self.all_d['fan']=' '
        self.all_d['original_title']=html['results'][loc]['original_title']
        self.all_d['plot']=html['results'][loc]['overview']
        self.all_d['n_id']=html['results'][loc]['id']
        html_g=html_g_movie
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                if i['name'] is not None])
        try:self.all_d['genere'] = u' / '.join([genres_list[x] for x in html['results'][loc]['genre_ids']])
        except:self.all_d['genere']=''
        self.all_d['rating']=str(html['results'][loc]['vote_average'])
        if 'release_date' in html['results'][loc]:
            self.all_d['year']=str(html['results'][loc]['release_date'].split("-")[0])
        else:
            self.all_d['year']='0'
        #self.getControl(101).setImage(self.all_d['icon'])
        self.getControl(103).setImage(self.all_d['fan'])
        self.getControl(102).setLabel('[COLOR blue][B]'+self.all_d['title']+' - '+self.all_d['year']+ ' - '+self.all_d['rating']+'[/B][/COLOR]')
        self.getControl(104).setText(self.all_d['plot'])
        self.getControl(105).setLabel(self.all_d['genere'])
        
        Thread(target=self.background_task).start()
    def onAction(self, action):
        global stop_window,once_fast_play
        
        actionId = action.getId()

        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            
            stop_window=True
            #self.close_tsk=1
            
            
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
           
            stop_window=True
          
            return self.close()
    def background_task(self):
            global list_index
            t=int(self.time_c)*10
            counter_close=0
            self.progressControl = self.getControl(3014)
            e_close=0
            before_end=int(Addon.getSetting("movie_window"))*10
            counter_close2=before_end
            while(t>30):
                try:
                    t=(xbmc.Player().getTotalTime()-xbmc.Player().getTime())*10
                except:
                    pass
                self.label=self.getControl(3015)
                self.label.setLabel(('%s')%str(int(counter_close2)/10))
                self.label=self.getControl(3016)
                self.label.setLabel(('Movie ends in %s')%str(int(t)/10))
                counter_close2-=1
                if counter_close2==0:
                    t=0
                    break
                if t<counter_close2:
                    sh_p=t
                else:
                    sh_p=counter_close2
                self.currentProgressPercent=int((sh_p*100)/before_end)
           
                self.progressControl.setPercent(self.currentProgressPercent)
                xbmc.sleep(100)
                
                if self.closenow==1:
                    break
             
            self.close()

    def onClick(self, controlId):
        
        stop_window=True
        self.closenow=1
        if controlId==201:
            settings=Addon.getSetting
            fav_search_f=settings("fav_search_f_tv")
            fav_servers_en=settings("fav_servers_en_tv")
            fav_servers=settings("fav_servers_tv")
            google_server= settings("google_server_tv")
            rapid_server=settings("rapid_server_tv")
            direct_server=settings("direct_server_tv")
            heb_server=settings("heb_server_tv")
            if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 or heb_server=='true' or google_server=='true' or rapid_server=='true' or direct_server=='true'):
                
                fav_status='true'
            else:
                fav_status='false'
            xbmc.Player().stop()
            str_next='ActivateWindow(10025,"plugin://plugin.video.shadow/?nextup=true&url=%s&no_subs=0&season=%s&episode=%s&mode=15&original_title=%s&id=%s&dd=%s&show_original_year=%s&fanart=%s&iconimage=%s&name=%s&description=%s",return)'%('www','%20','%20',self.all_d['original_title'],self.all_d['n_id'],' ',self.all_d['year'],urllib.quote_plus(self.all_d['fan']),urllib.quote_plus(self.all_d['icon']),self.all_d['title'],urllib.quote_plus(self.all_d['plot'].encode('utf-8')))
            xbmc.executebuiltin(str_next)
        
      
        self.close()
        
    
    def onFocus(self, controlId):
        pass 
class UpNext(xbmcgui.WindowXMLDialog):
    item = None
    cancel = False
    watchnow = False
    
    progressStepSize = 0
    currentProgressPercent = 100

    def __init__(self, *args, **kwargs):
        logging.warning('INIT UPNEXT')
        global clicked
        from platform import machine
        
        OS_MACHINE = machine()
        self.closenow=0
        clicked=False
        self.action_exitkeys_id = [10, 13]
        logging.warning('INIT UPNEXT0')
        self.progressControl = None
        if OS_MACHINE[0:5] == 'armv7':
            xbmcgui.WindowXMLDialog.__init__(self)
        else:
            xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
        logging.warning('INIT UPNEXT2')
        
        
   
    def background_task(self):
        global list_index,clicked_id
        t=int(self.time_c)*10
        counter_close=0
        self.progressControl = self.getControl(3014)
        e_close=0
        before_end=int(Addon.getSetting("before_end2"))*10
        counter_close2=t-before_end
        #logging.warning('counter_close2_t:'+str(t))
        while(t>30):
            self.label=self.getControl(3015)
            #self.label.setLabel(('%s seconds')%str(int(counter_close2)/10))
            self.label.setLabel(str(clicked_id))
            counter_close2-=1
            #logging.warning('counter_close2:'+str(counter_close2))
            
            if counter_close2==0:
                t=0
                break
            self.currentProgressPercent=int((counter_close2*100)/before_end)
       
            self.progressControl.setPercent(self.currentProgressPercent)
            xbmc.sleep(100)
            t-=1
            if self.closenow==1:
                break
        if self.closenow==0:
            list_index=self.list.getSelectedPosition()        
        self.close()
    def onInit(self):
        self.time_c=30
        try:
            self.time_c=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
        except:
            self.time_c=30
        
        
            
        self.list = self.getControl(3000)
        self.but = self.getControl(3012)
        if len(self.item['list'])==0:
                self.but.setVisible(False)
                
        for it in self.item['list']:
         
          
          liz   = xbmcgui.ListItem(it.split('$$$$$$$')[0])
          self.list.addItem(liz)
       
        
        self.setFocus(self.but)
        logging.warning('INIT UPNEXT1')
        Thread(target=self.background_task).start()
        self.setInfo()
        self.prepareProgressControl()

    def setInfo(self):
        logging.warning('INIT UPNEXT2')
       
        episodeInfo = str(self.item['season']) + 'x' + str(self.item['episode']) + '.'
        if self.item['rating'] is not None:
            rating = str(round(float(self.item['rating']), 1))
        else:
            rating = None
        
        if self.item is not None:
            self.setProperty(
                'fanart', self.item['art'].get('tvshow.fanart', ''))
            self.setProperty(
                'landscape', self.item['art'].get('tvshow.landscape', ''))
            self.setProperty(
                'clearart', self.item['art'].get('tvshow.clearart', ''))
            self.setProperty(
                'clearlogo', self.item['art'].get('tvshow.clearlogo', ''))
            self.setProperty(
                'poster', self.item['art'].get('tvshow.poster', ''))
            self.setProperty(
                'thumb', self.item['art'].get('thumb', ''))
            self.setProperty(
                'plot', self.item['plot'].replace("\n",'').strip())
            self.setProperty(
                'tvshowtitle', self.item['showtitle'])
            self.setProperty(
                'title', self.item['title'])
            self.setProperty(
                'season', str(self.item['season']))
            self.setProperty(
                'episode', str(self.item['episode']))
            self.setProperty(
                'seasonepisode', episodeInfo)
            self.setProperty(
                'year', str(self.item['firstaired']))
            self.setProperty(
                'rating', rating)
            self.setProperty(
                'playcount', str(self.item['playcount']))

    def prepareProgressControl(self):
        logging.warning('INIT UPNEXT3')
        # noinspection PyBroadException
        try:
            self.progressControl = self.getControl(3014)
            if self.progressControl is not None:
                self.progressControl.setPercent(self.currentProgressPercent)
        except Exception:
            pass

    def setItem(self, item):
        self.item = item

    def setProgressStepSize(self, progressStepSize):
        self.progressStepSize = progressStepSize

    def updateProgressControl(self):
        # noinspection PyBroadException
        try:
            self.currentProgressPercent = self.currentProgressPercent - self.progressStepSize
         
            self.progressControl = self.getControl(3014)
           
            if self.progressControl is not None:
                self.progressControl.setPercent(self.currentProgressPercent)
        except Exception:
            pass

    def setCancel(self, cancel):
        self.cancel = cancel

    def isCancel(self):
        return self.cancel

    def setWatchNow(self, watchnow):
        self.watchnow = watchnow

    def isWatchNow(self):
        return self.watchnow

    def onFocus(self, controlId):
        pass

    def doAction(self):
        pass

    def closeDialog(self):
        self.close()

    def onClick(self, control_id):
        global list_index,clicked,clicked_id
        clicked_id=str(control_id)
        logging.warning('clicked_id::'+str(clicked_id))
        if control_id == 3012:
            # watch now
            clicked=True
            list_index=0
            self.setWatchNow(True)
            self.closenow=1
            self.close()
            
        elif control_id == 3013:
            # cancel
            clicked=False
            list_index=888
            self.setCancel(True)
            self.closenow=1
            self.close()
        elif control_id == 3000:
            clicked=True
            index = self.list.getSelectedPosition()        
            list_index=index
            self.closenow=1
            self.close()
        pass

    def onAction(self, action):
        logging.warning('Action::'+str(action.getId()))
        if action == ACTION_PLAYER_STOP:
            self.closenow=1
            self.close()
class Thread(threading.Thread):
    def __init__(self, target, *args):
       
        self._target = target
        self._args = args
        
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        self._target(*self._args)
def get_params():
        param=[]
        if len(sys.argv)>=2:
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


def get_genere(link):
  
   images={}
   html=requests.get(link).json()
   aa=[]
   image='https://wordsfromjalynn.files.wordpress.com/2014/12/movie-genres-1.png'
   for data in html['genres']:
     if '/movie' in link:
       new_link='http://api.themoviedb.org/3/genre/%s/movies?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(str(data['id']),lang)
     else:
       new_link='http://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&sort_by=popularity.desc&with_genres=%s&language=%s&page=1'%(str(data['id']),lang)
     
     
     aa.append(addDir3(data['name'],new_link,14,image,image,data['name']))
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),aa,len(aa))
def read_site_html(url_link):
    import requests
    '''
    req = urllib2.Request(url_link)
    req.add_header('User-agent',__USERAGENT__)# 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    html = urllib2.urlopen(req).read()
    '''
    html=requests.get(url_link)
    return html
def tv_show_menu():
    all=[]
    import datetime
    now = datetime.datetime.now()
    #Popular
    aa=addDir3('Popular','http://api.themoviedb.org/3/tv/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,14,BASE_LOGO+'popular.png','https://image.businessinsider.com/5d5ea69fcd97841fea3d3b36?width=1100&format=jpeg&auto=webp','TMDB')
    all.append(aa)
    logging.warning(BASE_LOGO+'on_air.png')
    aa=addDir3('On the air','https://api.themoviedb.org/3/tv/on_the_air?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,14,BASE_LOGO+'on_air.png','https://i.pinimg.com/236x/1c/49/8f/1c498f196ef8818d3d01223b72678fc4--divergent-movie-poster-divergent-.jpg','TMDB')
    all.append(aa)
    
    
    aa=addDir3('New Tv shows','https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US&sort_by=popularity.desc&first_air_date_year='+str(now.year)+'&timezone=America%2FNew_York&include_null_first_air_ates=false&language={0}&page=1'.format(lang),14,BASE_LOGO+'new_s.png','https://lh5.ggpht.com/cr6L4oleXlecZQBbM1EfxtGggxpRK0Q1cQ8JBtLjJdeUrqDnXAeBHU30trRRnMUFfSo=w300','New Tv shows')
    all.append(aa)
    #new episodes
    aa=addDir3('New episodes','https://api.tvmaze.com/schedule',20,BASE_LOGO+'new_ep.png','https://img.buzzfeed.com/buzzfeed-static/static/2019-12/18/20/campaign_images/6a40bc4514fb/25-tv-episodes-from-this-decade-well-never-forget-2-88-1576702707-2_dblbig.jpg','New Episodes')
    all.append(aa)
    #Genre
    aa=addDir3('Genre','http://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,18,BASE_LOGO+'genre.png','https://consequenceofsound.net/wp-content/uploads/2019/11/CoS_2010sDecades-TVShows.jpg?quality=80','TMDB')
    all.append(aa)
    #Years
    aa=addDir3('Years','tv_years&page=1',14,BASE_LOGO+'years.png','https://d2yhzr6tx8qnba.cloudfront.net/images/db/9/b6/58e2db43d1b69.jpeg','TMDB')
    all.append(aa)
    aa=addDir3('Networks','tv_years&page=1',101,BASE_LOGO+'networks.png','https://images.pond5.com/tv-networks-logos-loop-footage-042898083_prevstill.jpeg','TMDB')
    all.append(aa)
    aa=addDir3('Advance Content selection','advance_tv',14,BASE_LOGO+'content_s.png','https://cdn0.tnwcdn.com/wp-content/blogs.dir/1/files/2010/03/movies.jpg','Advance Content selection')
    
    all.append(aa)
    #Search tv
    aa=addDir3('Search','http://api.themoviedb.org/3/search/tv?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language={0}&page=1'.format(lang),14,BASE_LOGO+'search.png','http://f.frogi.co.il/news/640x300/010170efc8f.jpg','TMDB')
    all.append(aa)
    aa=addDir3('Search History','tv',143,BASE_LOGO+'search.png','https://www.york.ac.uk/media/study/courses/postgraduate/centreforlifelonglearning/English-Building-History-banner-bought.jpg','TMDB')
    all.append(aa)
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    
    table_name='lastlinktv'
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""id TEXT);"%table_name)
    
    dbcur.execute("SELECT * FROM lastlinktv WHERE o_name='f_name'")

    match = dbcur.fetchone()
    dbcon.commit()
    
    dbcur.close()
    dbcon.close()
    
    if match!=None:
       f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match
       try:
           if url!=' ':
             if 'http' not  in url:
           
               url=url.decode('base64')
              
             aa=addLink('[I]Last Link played[/I]', url,6,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season=season,episode=episode,tmdb=id,year=show_original_year,place_control=True)
             all.append(aa)
       except  Exception as e:
         logging.warning(e)
         pass
         
    aa=addDir3('Series Tracker','tv',145,BASE_LOGO+'tracker.png','https://brewminate.com/wp-content/uploads/2020/02/GeorgeThompsonTeachingHistory01.png','History')
    
    all.append(aa)
   
    
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
def tv_neworks():
    all_d=[]
    if Addon.getSetting("order_networks")=='0':
        order_by='popularity.desc'
    elif Addon.getSetting("order_networks")=='2':
        order_by='vote_average.desc'
    elif Addon.getSetting("order_networks")=='1':
        order_by='first_air_date.desc'
    aa=addDir3('[COLOR lightblue]Disney+[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2739&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://lumiere-a.akamaihd.net/v1/images/image_308e48ed.png','https://allears.net/wp-content/uploads/2018/11/wonderful-world-of-animation-disneys-hollywood-studios.jpg','Disney'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR blue]Apple TV+[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2552&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://ksassets.timeincuk.net/wp/uploads/sites/55/2019/03/Apple-TV-screengrab-920x584.png','https://www.apple.com/newsroom/videos/apple-tv-plus-/posters/Apple-TV-app_571x321.jpg.large.jpg','Apple'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR red]NetFlix[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=213&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://art.pixilart.com/705ba833f935409.png','https://i.ytimg.com/vi/fJ8WffxB2Pg/maxresdefault.jpg','NetFlix'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR gray]HBO[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=49&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://filmschoolrejects.com/wp-content/uploads/2018/01/hbo-logo.jpg','https://www.hbo.com/content/dam/hbodata/brand/hbo-static-1920.jpg','HBO'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR lightblue]CBS[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=16&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://cdn.freebiesupply.com/logos/large/2x/cbs-logo-png-transparent.png','https://tvseriesfinale.com/wp-content/uploads/2014/10/cbs40-590x221.jpg','HBO'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR purple]SyFy[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=77&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'http://cdn.collider.com/wp-content/uploads/syfy-logo1.jpg','https://imagesvc.timeincapp.com/v3/mm/image?url=https%3A%2F%2Fewedit.files.wordpress.com%2F2017%2F05%2Fdefault.jpg&w=1100&c=sc&poi=face&q=85','SyFy'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR lightgreen]The CW[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=71&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://www.broadcastingcable.com/.image/t_share/MTU0Njg3Mjc5MDY1OTk5MzQy/tv-network-logo-cw-resized-bc.jpg','https://i2.wp.com/nerdbastards.com/wp-content/uploads/2016/02/The-CW-Banner.jpg','The CW'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR silver]ABC[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'http://logok.org/wp-content/uploads/2014/03/abc-gold-logo-880x660.png','https://i.ytimg.com/vi/xSOp4HJTxH4/maxresdefault.jpg','ABC'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]NBC[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=6&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://designobserver.com/media/images/mondrian/39684-NBC_logo_m.jpg','https://www.nbcstore.com/media/catalog/product/cache/1/image/1000x/040ec09b1e35df139433887a97daa66f/n/b/nbc_logo_black_totebagrollover.jpg','NBC'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR gold]AMAZON[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=1024&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'http://g-ec2.images-amazon.com/images/G/01/social/api-share/amazon_logo_500500._V323939215_.png','https://cdn.images.express.co.uk/img/dynamic/59/590x/Amazon-Fire-TV-Amazon-Fire-TV-users-Amazon-Fire-TV-stream-Amazon-Fire-TV-Free-Dive-TV-channel-Amazon-Fire-TV-news-Amazon-1010042.jpg?r=1535541629130','AMAZON'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR green]hulu[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=453&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://i1.wp.com/thetalkinggeek.com/wp-content/uploads/2012/03/hulu_logo_spiced-up.png?resize=300%2C225&ssl=1','https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwi677r77IbeAhURNhoKHeXyB-AQjRx6BAgBEAU&url=https%3A%2F%2Fwww.hulu.com%2F&psig=AOvVaw0xW2rhsh4UPsbe8wPjrul1&ust=1539638077261645','hulu'.decode('utf8'))
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def main_menu():
    show_updates()
    
    all_d=[]
    aa=addDir3('Movie World','www',2,BASE_LOGO+'movies.png','https://townsquare.media/site/295/files/2019/12/2020-movies-collage.jpg?w=980&q=75','Movies')
    all_d.append(aa)
    aa=addDir3('TV World','www',3,BASE_LOGO+'tv.png','https://cdn.mos.cms.futurecdn.net/qCD39X4DjbpgxD7ZFW63eG.jpg','TV')
    all_d.append(aa)
    aa=addDir3('Trakt World','www',21,BASE_LOGO+'trakt.png','https://cdn.mos.cms.futurecdn.net/qCD39X4DjbpgxD7ZFW63eG.jpg','No account needed)')
    all_d.append(aa)
    
    aa=addDir3('Trakt','www',114,BASE_LOGO+'trakt.png','https://bestdroidplayer.com/wp-content/uploads/2019/06/trakt-what-is-how-use-on-kodi.png','TV')
    all_d.append(aa)
    aa=addDir3('Search','www',5,BASE_LOGO+'search.png','https://searchengineland.com/figz/wp-content/seloads/2017/12/compare-seo-ss-1920-800x450.jpg','Search')
    all_d.append(aa)
    aa=addDir3('Search History','both',143,BASE_LOGO+'search.png','https://www.york.ac.uk/media/study/courses/postgraduate/centreforlifelonglearning/English-Building-History-banner-bought.jpg','TMDB')
    all_d.append(aa)
    aa=addDir3('[I]---Last link Played---[/I]','www',144,BASE_LOGO+'last.png','https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT5GMHNjPCi4oCp4PHArgKQ-SBzF4wYdyRKbf0hj0t2qQxqffmO&usqp=CAU','Last Played') 
    all_d.append(aa)
    aa=addNolink( '---Whats new---', id,149,False,fanart='https://i.ytimg.com/vi/tJD4Q0h9fL0/maxresdefault.jpg', iconimage=BASE_LOGO+'news.png',plot='Whats new',dont_place=True)
    all_d.append(aa)
    aa=addDir3('Resume watching','both',158,BASE_LOGO+'resume.png','https://www.york.ac.uk/media/study/courses/postgraduate/centreforlifelonglearning/English-Building-History-banner-bought.jpg','TMDB')
    all_d.append(aa)
    if Addon.getSetting('debrid_select')=='0':
        aa=addDir3('My RD history','1',168,BASE_LOGO+'rd.png','https://www.york.ac.uk/media/study/courses/postgraduate/centreforlifelonglearning/English-Building-History-banner-bought.jpg','TMDB')
        all_d.append(aa)
        aa=addDir3('RD Torrents','1',169,BASE_LOGO+'rd.png','https://www.york.ac.uk/media/study/courses/postgraduate/centreforlifelonglearning/English-Building-History-banner-bought.jpg','TMDB')
        all_d.append(aa)
        
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def movie_world():
    all_d=[]
    aa=addDir3('In Theaters','http://api.themoviedb.org/3/movie/now_playing?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,14,BASE_LOGO+'int.png','https://images.cdn1.stockunlimited.net/preview1300/cinema-background-with-movie-objects_1823387.jpg','Tmdb')
    all_d.append(aa)
    'Popular Movies'
    aa=addDir3('Popular Movies','http://api.themoviedb.org/3/movie/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,14,BASE_LOGO+'popular.png','https://www.newszii.com/wp-content/uploads/2018/08/Most-Popular-Action-Movies.png','Tmdb')
    all_d.append(aa)
    
    
    
    #Genre
    aa=addDir3('Genre','http://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,18,BASE_LOGO+'genre.png','https://s.studiobinder.com/wp-content/uploads/2019/09/Movie-Genres-Types-of-Movies-List-of-Genres-and-Categories-Header-StudioBinder.jpg','Tmdb')
    all_d.append(aa)
    #Years
    aa=addDir3('Years','movie_years&page=1',14,BASE_LOGO+'years.png','https://i.pinimg.com/originals/e4/03/91/e4039182cd17c48c8f9cead44cda7df3.jpg','Tmdb')
    all_d.append(aa)
    aa=addDir3('Studio','movie_years&page=1',112,BASE_LOGO+'studio.png','https://cdn-static.denofgeek.com/sites/denofgeek/files/styles/main_wide/public/2016/04/movlic_studios_1.jpg?itok=ih8Z7wOk','Tmdb')
    all_d.append(aa)
    aa=addDir3('Advance Content selection','advance_movie',14,BASE_LOGO+'content_s.png','https://cdn0.tnwcdn.com/wp-content/blogs.dir/1/files/2010/03/movies.jpg','Advance Content selection')
    all_d.append(aa)
    #Search movie
    aa=addDir3('Search movie','http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language={0}&append_to_response=origin_country&page=1'.format(lang),14,BASE_LOGO+'search_m.png','http://www.videomotion.co.il/wp-content/uploads/whatwedo-Pic-small.jpg','Tmdb')
    all_d.append(aa)
    aa=addDir3('Search History','movie',143,BASE_LOGO+'search.png','https://www.york.ac.uk/media/study/courses/postgraduate/centreforlifelonglearning/English-Building-History-banner-bought.jpg','TMDB')
    all_d.append(aa)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    
    table_name='lastlinkmovie'
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""id TEXT);"%table_name)
    
    dbcur.execute("SELECT * FROM lastlinkmovie WHERE o_name='f_name'")

    match = dbcur.fetchone()
    dbcon.commit()
    
    dbcur.close()
    dbcon.close()
    
    if match!=None:
       f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match
       try:
           if url!=' ':
             if 'http' not  in url:
           
               url=url.decode('base64')
              
             aa=addLink('[I]Last Link played[/I]', url,6,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season=season,episode=episode,tmdb=id,year=show_original_year,place_control=True)
             all_d.append(aa)
       except  Exception as e:
         logging.warning(e)
         pass
    aa=addDir3('History','movie',145,BASE_LOGO+'history.png','https://brewminate.com/wp-content/uploads/2020/02/GeorgeThompsonTeachingHistory01.png','History')
    
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

def movie_prodiction():
    all_d=[]
    if Addon.getSetting("order_networks")=='0':
        order_by='popularity.desc'
    elif Addon.getSetting("order_networks")=='2':
        order_by='vote_average.desc'
    elif Addon.getSetting("order_networks")=='1':
        order_by='first_air_date.desc'
    
    
    aa=addDir3('[COLOR red]Marvel[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=7505&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://yt3.ggpht.com/a-/AN66SAwQlZAow0EBMi2-tFht-HvmozkqAXlkejVc4A=s900-mo-c-c0xffffffff-rj-k-no','https://images-na.ssl-images-amazon.com/images/I/91YWN2-mI6L._SL1500_.jpg','Marvel'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR lightblue]DC Studios[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=9993&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://pmcvariety.files.wordpress.com/2013/09/dc-comics-logo.jpg?w=1000&h=563&crop=1','http://www.goldenspiralmedia.com/wp-content/uploads/2016/03/DC_Comics.jpg','DC Studios'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR lightgreen]Lucasfilm[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=1&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://fontmeme.com/images/lucasfilm-logo.png','https://i.ytimg.com/vi/wdYaG3o3bgE/maxresdefault.jpg','Lucasfilm'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]Warner Bros.[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=174&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'http://looking.la/wp-content/uploads/2017/10/warner-bros.png','https://cdn.arstechnica.net/wp-content/uploads/2016/09/warner.jpg','SyFy'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR blue]Walt Disney Pictures[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=2&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://i.ytimg.com/vi/9wDrIrdMh6o/hqdefault.jpg','https://vignette.wikia.nocookie.net/logopedia/images/7/78/Walt_Disney_Pictures_2008_logo.jpg/revision/latest?cb=20160720144950','Walt Disney Pictures'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR skyblue]Pixar[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=3&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://elestoque.org/wp-content/uploads/2017/12/Pixar-lamp.png','https://wallpapercave.com/wp/GysuwJ2.jpg','Pixar'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR deepskyblue]Paramount[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=4&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://upload.wikimedia.org/wikipedia/en/thumb/4/4d/Paramount_Pictures_2010.svg/1200px-Paramount_Pictures_2010.svg.png','https://vignette.wikia.nocookie.net/logopedia/images/a/a1/Paramount_Pictures_logo_with_new_Viacom_byline.jpg/revision/latest?cb=20120311200405&format=original','Paramount'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR burlywood]Columbia Pictures[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=5&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://static.tvtropes.org/pmwiki/pub/images/lady_columbia.jpg','https://vignette.wikia.nocookie.net/marveldatabase/images/1/1c/Columbia_Pictures_%28logo%29.jpg/revision/latest/scale-to-width-down/1000?cb=20141130063022','Columbia Pictures'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR powderblue]DreamWorks[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=7&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://www.dreamworksanimation.com/share.jpg','https://www.verdict.co.uk/wp-content/uploads/2017/11/DA-hero-final-final.jpg','DreamWorks'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR lightsaltegray]Miramax[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=14&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://vignette.wikia.nocookie.net/disney/images/8/8b/1000px-Miramax_1987_Print_Logo.png/revision/latest?cb=20140902041428','https://i.ytimg.com/vi/4keXxB94PJ0/maxresdefault.jpg','Miramax'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR gold]20th Century Fox[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=25&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://pmcdeadline2.files.wordpress.com/2017/03/20th-century-fox-cinemacon1.jpg?w=446&h=299&crop=1','https://vignette.wikia.nocookie.net/simpsons/images/8/80/TCFTV_logo_%282013-%3F%29.jpg/revision/latest?cb=20140730182820','20th Century Fox'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR bisque]Sony Pictures[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=34&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Sony_Pictures_Television_logo.svg/1200px-Sony_Pictures_Television_logo.svg.png','https://vignette.wikia.nocookie.net/logopedia/images/2/20/Sony_Pictures_Digital.png/revision/latest?cb=20140813002921','Sony Pictures'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR navy]Lions Gate Films[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=35&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'http://image.wikifoundry.com/image/1/QXHyOWmjvPRXhjC98B9Lpw53003/GW217H162','https://vignette.wikia.nocookie.net/fanon/images/f/fe/Lionsgate.jpg/revision/latest?cb=20141102103150','Lions Gate Films'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR beige]Orion Pictures[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=41&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://i.ytimg.com/vi/43OehM_rz8o/hqdefault.jpg','https://i.ytimg.com/vi/g58B0aSIB2Y/maxresdefault.jpg','Lions Gate Films'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]MGM[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=21&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://pbs.twimg.com/profile_images/958755066789294080/L9BklGz__400x400.jpg','https://assets.entrepreneur.com/content/3x2/2000/20150818171949-metro-goldwun-mayer-trade-mark.jpeg','MGM'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR gray]New Line Cinema[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=12&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://upload.wikimedia.org/wikipedia/en/thumb/0/04/New_Line_Cinema.svg/1200px-New_Line_Cinema.svg.png','https://vignette.wikia.nocookie.net/theideas/images/a/aa/New_Line_Cinema_logo.png/revision/latest?cb=20180210122847','New Line Cinema'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR darkblue]Gracie Films[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=18&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://i.ytimg.com/vi/q_slAJmZBeQ/hqdefault.jpg','https://i.ytimg.com/vi/yGofbuJTb4g/maxresdefault.jpg','Gracie Films'.decode('utf8'))
    all_d.append(aa)
    aa=addDir3('[COLOR goldenrod]Imagine Entertainment[/COLOR]'.decode('utf8'),'https://'+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=23&language={0}&sort_by={1}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(lang,order_by),14,'https://s3.amazonaws.com/fs.goanimate.com/files/thumbnails/movie/2813/1661813/9297975L.jpg','https://www.24spoilers.com/wp-content/uploads/2004/06/Imagine-Entertainment-logo.jpg','Imagine Entertainment'.decode('utf8'))
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def main_trakt():
   all_d=[]
   aa=addDir3('Movie Lists','movie',116,BASE_LOGO+'lists.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Lists')
   all_d.append(aa)
   aa=addDir3('Tv Lists','tv',116,BASE_LOGO+'lists.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Lists')
   all_d.append(aa)
   
   aa=addDir3('Progress','users/me/watched/shows?extended=full',115,BASE_LOGO+'progress.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Progress')
   all_d.append(aa)
   aa=addDir3('Episodes watchlist','sync/watchlist/episodes?extended=full',115,BASE_LOGO+'ep_watch.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Episodes')
   all_d.append(aa)
   aa=addDir3('Series watchlist','users/me/watchlist/episodes?extended=full',117,BASE_LOGO+'series_w.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Series')
   all_d.append(aa)
   aa=addDir3('TV Collection','users/me/collection/shows',117,BASE_LOGO+'tv_col.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','TV')
   all_d.append(aa)
   aa=addDir3('Shows watchlist','users/me/watchlist/shows',117,BASE_LOGO+'show_w.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Shows')
   all_d.append(aa)
   aa=addDir3('Shows recommendations','recommendations/shows?ignore_collected=true',166,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
   all_d.append(aa)
   
   aa=addDir3('Movies watchlist','users/me/watchlist/movies',117,BASE_LOGO+'movie_wl.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
   all_d.append(aa)
   aa=addDir3('Movies recommendations','recommendations/movies?ignore_collected=true',166,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
   all_d.append(aa)
   
   aa=addDir3('Watched movies','users/me/watched/movies',117,BASE_LOGO+'movie_w.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Watched')
   all_d.append(aa)
   aa=addDir3('Watched shows','users/me/watched/shows',117,BASE_LOGO+'series_wa.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Watched shows')
   all_d.append(aa)
   aa=addDir3('Movies Collection','users/me/collection/movies',117,BASE_LOGO+'movie_c.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','collection')
   all_d.append(aa)
   aa=addDir3('Liked lists','users/likes/lists',118,BASE_LOGO+'liked_l.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Liked lists')
   all_d.append(aa)
   aa=addDir3('Resume watching Movies','sync/playback/movies',117,BASE_LOGO+'liked_l.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Liked lists')
   all_d.append(aa)
   
   aa=addDir3('Resume watching Episodes','sync/playback/episodes',164,BASE_LOGO+'liked_l.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Liked lists')
   all_d.append(aa)
   
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

def check_cached(magnet,rd):
    
    
    check=False
    if Addon.getSetting('debrid_select')=='0':
        try:
        
            hash = str(re.findall(r'btih:(.*?)&', magnet)[0].lower())
            hashCheck = rd.checkHash(hash)
            if hash in hashCheck:
                    if 'rd' in hashCheck[hash]:
                        if len(hashCheck[hash]['rd'])>0:
                          if  '.mkv' in str(hashCheck[hash]['rd']) or '.avi' in str(hashCheck[hash]['rd'])  or '.mp4' in str(hashCheck[hash]['rd']) :
                            check=True
        except:
            logging.warning(magnet)
            pass
        return check
    elif Addon.getSetting('debrid_select')=='1':
        hash = [str(re.findall(r'btih:(.*?)&', magnet)[0].lower())]
        hashCheck=rd.hash_check(hash)
        if hashCheck['transcoded'][0]==True:
            check=True
        return check
    else:
        hash = [str(re.findall(r'btih:(.*?)&', magnet)[0].lower())]
        hashCheck=rd.check_hash(hash)['data']
        logging.warning('hashCheck::')
        logging.warning(hashCheck)
        if hashCheck[0]['instant']==True:
            check=True
        return check
def get_po_watching(original_title,show_original_year,tv_movie):
    global po_watching,full_stats
    from resources.modules.general import call_trakt
    try:
        if tv_movie=='movie':
            user_watching=call_trakt('movies/%s/watching'%(clean_name(original_title,1).lower().replace(' ','-').replace(':','').replace("'","")+'-'+show_original_year),with_auth=False)
            stats=call_trakt('movies/%s/stats'%(clean_name(original_title,1).lower().replace(' ','-')+'-'+show_original_year),with_auth=False)
        else:
            user_watching=call_trakt('shows/%s/watching'%(clean_name(original_title,1).lower().replace(' ','-').replace("'","").replace(':','')),with_auth=False)
            stats=call_trakt('shows/%s/stats'%(clean_name(original_title,1).lower().replace(' ','-')+'-'+show_original_year),with_auth=False)
            
        po_watching=('People watching This %s now: '%tv_movie.replace('tv','show')+'[COLOR lightblue]'+str(len(user_watching))+'[/COLOR]')
        full_stats='Watchers: [COLOR lightblue]'+str(stats['watchers'])+'[/COLOR],Plays: [COLOR lightblue]'+str(stats['plays'])+'[/COLOR]\nVotes: [COLOR lightblue]'+str(stats['votes'])+'[/COLOR]'
        
        
    
    except Exception as e:
        logging.warning('Po watching err:'+str(e))
        po_watching=''
        full_stats=''
    return po_watching,full_stats
def c_get_sources(name,data,original_title,id,season,episode,show_original_year):
   try:
   
    
    global silent,sources_searching,po_watching,full_stats
    full_stats=''
    po_watching=''
    dd=[]
    dd.append((name,data,original_title,id,season,episode,show_original_year))
    logging.warning('dd search')
    logging.warning(dd)
    sources_searching=True
    all_ok=[]
    if Addon.getSetting('debrid_select')=='0':
       rd = real_debrid.RealDebrid()
    elif Addon.getSetting('debrid_select')=='1':
        pr= premiumize.Premiumize()
    else:
        ad=all_debrid.AllDebrid()
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    source_dir = os.path.join(addonPath, 'resources', 'sources')
    if not silent:
        dp = xbmcgui . DialogProgress ( )
        dp.create('Please wait','Searching', '','')
        dp.update(0, 'Please wait','Searching', '' )
    sys.path.append( source_dir)
    onlyfiles = [f for f in listdir(source_dir) if isfile(join(source_dir, f))]
    start_time = time.time()
    if season!=None and season!="%20":
          tv_movie='tv'
    else:
          tv_movie='movie'
          
    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode
    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
    all_sources=[]
    thread=[]
    for items in onlyfiles:
        
       if Addon.getSetting(items.replace('.py',''))=='false':
          continue
       if 'pyo' not in items and 'init' not in items:
       
        impmodule = __import__(items.replace('.py',''))
        
        all_sources.append((items,impmodule))
        impmodule.stop_all=0
        impmodule.global_var=[]
        thread.append(Thread(impmodule.get_links,tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id))
        thread[len(thread)-1].setName(items.replace('.py',''))
        thread[len(thread)-1].start()
    
    thread.append(Thread(get_po_watching,original_title,show_original_year,tv_movie))
    thread[len(thread)-1].setName(items.replace('Po.watching',''))
    thread[len(thread)-1].start()
    tt={}
    for i in range (0,(len(thread)+50)): 
      tt[i]="red"
    max_table=[2160,1080,720,9999]
    min_table=[2160,1080,720,0]
    if tv_movie=='movie':
        se='one_click'
        mq="max_quality"
        minq="min_quality"
    else:
        se='one_click_tv'
        mq="max_quality_tv"
        minq="min_quality_tv"
    one_click=Addon.getSetting(se)=='true'
    
    max_q=max_table[int(Addon.getSetting(mq))]
    min_q=min_table[int(Addon.getSetting(minq))]
    once=0
    all_lks=[]
    max_time=int(Addon.getSetting("time_s"))
    stop_all=0
    if len(thread)>0:
      while 1:
        num_live=0
         
          
         
        elapsed_time = time.time() - start_time
        
            
         
              
        num_live=0
        string_dp=''
        string_dp2=''
        still_alive=0
        count_2160=0
        count_1080=0
        count_720=0
        count_480=0
        count_rest=0
        count_alive=0
        all_alive={}
        for yy in range(0,len(thread)):
            all_alive[thread[yy].name]=thread[yy].is_alive()
            
            #logging.warning(thread[yy].name+' Alive: '+str(thread[yy].is_alive()))
            if not thread[yy].is_alive():
              num_live=num_live+1
              tt[yy]="lightgreen"
              
              #logging.warning('Dead:'+thread[yy].name)
              #string_dp2=string_dp2+',[COLOR red]O:'+thread[yy].name+'[/COLOR]'
            else:
              
              
              if string_dp2=='':
                string_dp2=thread[yy].name
              else:
                count_alive+=1
                string_dp2=string_dp2+','+thread[yy].name
              still_alive=1
              tt[yy]="red"
        f_result={}
        for name1,items in all_sources:
            f_result[name1]={}
            f_result[name1]['links']=items.global_var
        living=[]
        for items in all_alive:
             if all_alive[items]:
               living.append(items)
        if count_alive>10:
            
            string_dp2='Remaining: '+str(count_alive)+' - '+random.choice (living)
        count_found=0
        for data in f_result:
            #logging.warning(f_result)
            if len (f_result[data]['links'])>0:
                   count_found+=1
                   
            if 'links' in f_result[data] and len (f_result[data]['links'])>0:
                 
                for links_in in f_result[data]['links']:
                    
                     
                     
                     name1,links,server,res=links_in
                     new_res=0
                     if '2160' in res:
                       count_2160+=1
                       new_res=2160
                     if '1080' in res:
                       count_1080+=1
                       new_res=1080
                     elif '720' in res:
                       count_720+=1
                       new_res=720
                     elif '480' in res:
                       count_480+=1
                       new_res=480
                     else:
                       count_rest+=1
                     try:
                        res_c=int(res)
                     except:
                        res_c=480
                     
                     if not silent and (once==0) and int(res_c)>=min_q and int(res_c)<=max_q and links not in all_lks and one_click:
                        check_one_click=False
                        if tv_movie=='tv':
                            
                            if 's%se%s'%(season_n,episode_n) in name1.lower():
                                check_one_click=True
                        else:
                            check_one_click=True
                        if check_one_click:
                            all_lks.append(links)
                            if Addon.getSetting('debrid_select')=='0':
                                run_lk=check_cached(links,rd)
                            elif  Addon.getSetting('debrid_select')=='1':
                                run_lk=check_cached(links,pr)
                            else:
                                run_lk=check_cached(links,ad)
                            if run_lk:
                                once=1
                                stop_all=1
                                dp.close()
                                silent=True
                                logging.warning('Playing Auto Now:'+str(once))
                                if not xbmc.Player().isPlaying():
                                    dd=[]
                                    dd.append((name1,data,original_title,id,season,episode,show_original_year))
                                    play_link(name1,links,' ',' ',description,data,original_title,id,season,episode,show_original_year,json.dumps(dd),nextup='true')
                                break
                            
                all_s_in=(f_result,int(((num_live* 100.0)/(len(thread))) ),string_dp2.replace('Remaining: ',''),2,string_dp)
            
                global_result="4K: [COLOR yellow]%s[/COLOR] 1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]"%(count_2160,count_1080,count_720,count_480,count_rest)
            
                total=count_1080+count_720+count_480+count_rest
                string_dp="4K: [COLOR yellow]%s[/COLOR] 1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]  T: [COLOR darksalmon]%s[/COLOR] "%(count_2160,count_1080,count_720,count_480,count_rest,total)
                
                  
                     
                  
            if stop_all==1:
                break
                  
        if not silent:
                    dp.update(int(((num_live* 100.0)/(len(thread))) ), ' Please Wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),string_dp, string_dp2)
                  
            
        if not silent:
            check=dp.iscanceled()
        else:
            check=False
        
        if check or still_alive==0 or elapsed_time>max_time or stop_all==1:
          logging.warning('Braking')
          logging.warning(check)
          logging.warning(elapsed_time)
          logging.warning(stop_all)
          
          for name1,items in all_sources:
                items.stop_all=1
          num_live2=0
          for threads in thread:
            all_s_in=(f_result,int(((num_live2* 100.0)/(len(thread))) ),'Closing',2,threads.name)
            
            elapsed_time = time.time() - start_time
            if not silent:
                dp.update(int(((num_live2* 100.0)/(len(thread))) ), ' Please Wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Closing', threads.name)
            if threads.is_alive():
                 
                 
                 threads._Thread__stop()
            num_live2+=1
           
          break
        xbmc.sleep(100)
    all_lk2=[]
    all_mag={}
    hash_index={}
    all_q={}
    all_names={}
    page_index=0
    all_mag[0]=[]
    counter_hash=0
    
    
    statistics={}
    statistics['magnet']=0
    statistics['non_magnet']=0
    statistics['unique']=0
    statistics['d_unique']=0
    statistics['c_hash']=0
    statistics['rd']=0
    statistics['non_rd']=0
    statistics['check_this']=0
    if once==0 or not silent:
        all_lk_in=[]
        all_unique=[]
        for name_f in f_result:
          for name,link,server,quality in f_result[name_f]['links']:
            if 'magnet' in link:
                statistics['magnet']+=1
                try:
                    #hash = str(re.findall(r'btih:(.*?)&', link)[0].lower())
                    hash=link.split('btih:')[1]
                    if '&' in hash:
                        hash=hash.split('&')[0]
                except:
                    hash =link.split('btih:')[1]
                if hash.lower() in all_lk_in:
                    statistics['d_unique']+=1
                    continue
                    
                
                statistics['unique']+=1
                all_lk_in.append(hash.lower())
                all_unique.append((name,link,server,quality))
            else:
                statistics['non_magnet']+=1
                logging.warning('Not magnet:'+link)
            
            
        
                 
        for name,link,server,quality in all_unique:
                        if not silent:
                            dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Updating links , check cached', name)
                        if link not in all_lk2:
                            all_lk2.append(link)
                            if 'magnet' in link:
                                try:
                                    #hash = str(re.findall(r'btih:(.*?)&', link)[0].lower())
                                    hash=link.split('btih:')[1]
                                    if '&' in hash:
                                        hash=hash.split('&')[0]
                                except:
                                    hash =link.split('btih:')[1]
                                #logging.warning(link)
                                #logging.warning(hash)
                                statistics['check_this']+=1
                                all_mag[page_index].append(hash.lower())
                                hash_index[hash.lower()]=link
                                all_names[hash.lower()]=name
                                all_q[hash.lower()]=quality.lower().replace('hd','720')
                                counter_hash+=1
                                if counter_hash>150:
                                    page_index+=1
                                    all_mag[page_index]=[]
                                    counter_hash=0
                
        all_hased=[]
                
                
    
        for items in all_mag:

                    if len(all_mag[items])>0 :
                        if Addon.getSetting('debrid_select')=='0':
                           hashCheck = rd.checkHash(all_mag[items])
                        elif Addon.getSetting('debrid_select')=='1':
                            hashCheck=pr.hash_check(all_mag[items])['transcoded']
                        else:
                            hashCheck=ad.check_hash(all_mag[items])['data']
                            
                        count_hash=0
                       
                        for hash in hashCheck:
                            statistics['c_hash']+=1
                            elapsed_time = time.time() - start_time
                            if not silent:
                                dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Updating links , check cached', str(hash))
                            if Addon.getSetting('debrid_select')=='0':
                                ok=False
                                try:
                                    if 'rd' in hashCheck[hash]:
                                        ok=True
                                except Exception as e: 
                                    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'In RD %s:'%str(e))))
                                    ok=False
                                if ok:
                                   if len(hashCheck[hash]['rd'])>0:
                                        found_c_h=False
                                        if tv_movie=='tv':
                                            for storage_variant in hashCheck[hash]['rd']:
                                                key_list = storage_variant.keys()
                                                if found_c_h:
                                                    break
                                                for items_t in hashCheck[hash]['rd']:
                                                   for itt in items_t:
                                                    
                                                    if itt in key_list and ('s%se%s.'%(season_n,episode_n) in items_t[itt]['filename'].lower() or 's%se%s '%(season_n,episode_n) in items_t[itt]['filename'].lower()):
                                                        
                                                        found_c_h=True
                                                        
                                                        break
                                        else:
                                            found_c_h=True
                                            
                                        if found_c_h and '.mkv' in str(hashCheck[hash]['rd']) or '.avi' in str(hashCheck[hash]['rd'])  or '.mp4' in str(hashCheck[hash]['rd']) :
                                            all_hased.append(hash)
                                        
                                   else:
                                      
                                      statistics['non_rd']+=1
                                
                            elif Addon.getSetting('debrid_select')=='1':
                                if hash==True:
                                    all_hased.append(all_mag[items][count_hash])
                                count_hash+=1
                            else:
                                if hash['instant']==True:
                                  all_hased.append(hash['hash'])
                                        
        
        for items in all_hased:
            
                
            all_ok.append(hash_index[items.lower()])
   
    if not silent:
        dp.close()
    sources_searching=False
    l_po_watching=po_watching
    l_full_stats=full_stats
    logging.warning(full_stats)
    return f_result,all_ok,once,tv_movie,l_po_watching,l_full_stats
   except Exception as e:
    import linecache
    sources_searching=False
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    logging.warning('ERROR IN NEXTUP IN:'+str(lineno))
    logging.warning('inline:'+line)
    logging.warning('Error:'+str(e))
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'inLine:'+str(lineno))))
    dp.close()
    sys.exit()
    pass
def get_title(title):
    text3=None
    text =title.strip()
    text2= re.search('(.*?)(dvdrip|xvid| cd[0-9]|dvdscr|brrip|divx|[\{\(\[]?[0-9]{4}).*',text)
    if text2:
        text =text2.group(1)
        text3= re.search('(.*?)\(.*\)(.*)',text)
    if text3:
        text =text3.group(1)
    logging.warning('text:'+text)
    return text.replace("."," ").strip()
def clean_marks(title):
    regex='\[(.+?)\]'
    m=re.compile(regex).findall(title)
    
    for items in m:
        title=title.replace('[%s]'%items,'')
    
    return title
def get_trakt_resume(tv_movie,id,season,episode):
            global all_w_global
            all_w={}
            if tv_movie=='movie':
                from resources.modules.general import call_trakt
                result=call_trakt('sync/playback/movies')
                
                for items in result:
                    progress=None
              
                    
                    t_id=items['movie']['ids']['tmdb']    
                    if id==str(t_id):
                        if 'progress' in items:
                            progress=items['progress']
                        all_w={}
                        all_w[id]={}
                        all_w[id]['precentage']=str(progress)
                        all_w=json.dumps(all_w)
                        logging.warning('Found progress')
                        logging.warning(all_w)
                        break
            else:
                from resources.modules.general import call_trakt
                result=call_trakt('sync/playback/episodes')
      
                for items in result:
                    t_id=items['show']['ids']['tmdb']
                    season_t=items['episode']['season']
                    episode_t=items['episode']['number']
                    
                    
                    if id==str(t_id) and season==str(season_t) and episode==str(episode_t):
                        if 'progress' in items:
                            progress=items['progress']
                        all_w={}
                        all_w[id]={}
                        all_w[id]['precentage']=str(progress)
                        all_w=json.dumps(all_w)
                        break
            all_w_global=all_w
            logging.warning('Done progress')
            logging.warning(all_w_global)
def clean_title(title, broken=None):
    title = title.lower()
    # title = tools.deaccentString(title)
    
    title = ''.join(char for char in title if char in string.printable)
    title= title.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
    if broken == 1:
        apostrophe_replacement = ''
    elif broken == 2:
        apostrophe_replacement = ' s'
    else:
        apostrophe_replacement = 's'
    title = title.replace("\\'s", apostrophe_replacement)
    title = title.replace("'s", apostrophe_replacement)
    title = title.replace("&#039;s", apostrophe_replacement)
    title = title.replace(" 039 s", apostrophe_replacement)

    title = re.sub(r'\:|\\|\/|\,|\!|\?|\(|\)|\'|\"|\\|\[|\]|\-|\_|\.', ' ', title)
    title = re.sub(r'\s+', ' ', title)
    title = re.sub(r'\&', 'and', title)

    return title.strip()
    
def getInfo(release_title):
    info = []
    release_title=clean_title(release_title)
    #release_title=release_title.lower().replace('.',' ')
    
    if any(i in release_title for i in ['x265', 'x 265', 'h265', 'h 265', 'hevc','hdr']):
        info.append('HEVC')

    

    

    if any(i in release_title for i in [' cam ', 'camrip', 'hdcam', 'hd cam', ' ts ', 'hd ts', 'hdts', 'telesync', ' tc ', 'hd tc', 'hdtc', 'telecine', 'xbet']):
        info.append('CAM')
    if any(i in release_title for i in [' 3d']):
        info.append('3D')
        
    return info
    
def get_sources(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,video_data_exp={},all_w={},use_filter='true'):
    global silent,selected_index,po_watching,all_w_global
    all_p_data=[]
    
    all_p_data.append((name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,video_data_exp,all_w,'false'))
    if Addon.getSetting("trakt_access_token")!='':
        try:
            s=int(season)
            tv_movie='tv'
            
        except:
            tv_movie='movie'
        all_w_global={}
        thread=[]
                
        thread.append(Thread(get_trakt_resume,tv_movie,id,season,episode))
            
        
        thread[0].start()
    
    episode=episode.replace('+','%20')
    if 'None' not in id:
        if 'tvdb' in id :
            url2=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=tvdb_id&language=%s'%(id.replace('tvdb',''),lang)
            pre_id=requests.get(url2).json()['tv_results']
            
            if len(pre_id)>0:
                id=str(pre_id[0]['id'])
        elif 'imdb' in id:
            url2=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=%s'%(id.replace('imdb',''),lang)
           
            pre_id=requests.get(url2).json()['tv_results']
            
            if len(pre_id)>0:
                id=str(pre_id[0]['id'])
    
    silent=False
    time_to_save=int(Addon.getSetting("save_time"))
    try:
        c=int(season)
        tv=True
    except:
       tv=False
       season='%20'
    if tv==False:
        se='one_click'
        
    else:
        se='one_click_tv'
    one_click=Addon.getSetting(se)=='true'
    
    original_title=original_title.replace(':',' ')
    if one_click:
    
        match_a,all_ok,once,tv_movie,po_watching,l_full_stats= c_get_sources( original_title,data,original_title,id,season,episode,show_original_year)
    else:
        match_a,all_ok,once,tv_movie,po_watching,l_full_stats= cache.get(c_get_sources, time_to_save, original_title,data,original_title,id,season,episode,show_original_year,table='pages')
    dd=[]
    dd.append((name,data,original_title,id,season,episode,show_original_year))
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
    
    dbcur.execute("DELETE FROM nextup")
    
    try:
       dbcur.execute("INSERT INTO nextup Values ('%s')"%(json.dumps(dd).encode('base64')))
    except:
        dbcur.execute("DROP TABLE IF EXISTS nextup;")
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
        dbcur.execute("INSERT INTO nextup Values ('%s')"%(json.dumps(dd).encode('base64')))
    dbcon.commit()
    
    dbcur.close()
    dbcon.close()
    menu=[]
    better_look=Addon.getSetting('better_look')=='true'
    links_data={}
    links_data['cached']=0
    links_data['un_cached']=0
    links_data['all']=0
    links_data['duplicated']=0
    
    all_lk=[]
    from resources.modules import PTN
    max_q_t=[720,1080,2160]
    min_q_t=[0,720,1080,2160]
    
    if tv_movie=='movie':
        added=''
    else:
        added='_tv'
    max_q=max_q_t[int(Addon.getSetting('max_q'+added))]
    min_q=min_q_t[int(Addon.getSetting('min_q'+added))]
    
    disable_3d=Addon.getSetting('3d'+added)=='false'
    disable_hdvc=Addon.getSetting('hdvc'+added)=='false'
    disable_low=Addon.getSetting('low_q'+added)=='false'
    encoding_filter=Addon.getSetting('encoding_filter'+added)=='true'
   
    if once==0:
        all_data=[]
        all_rejected=[]
        all_filted=[]
        all_filted_rejected=[]
        for items in match_a:
            for name,lk,data,quality in match_a[items]['links']:
               continue_next=False
               
               try:
                   int_q=int(quality)
                   if int_q<min_q or int_q>max_q:
                    continue_next=True
               except:
                   if min_q>0:
                      continue_next=True
                   pass
               if encoding_filter:
                   data_name=getInfo(name)
                 
                   if 'CAM' in data_name and disable_low:
                     continue_next=True
                   if 'HEVC' in data_name and disable_hdvc:
                     continue_next=True
                   if '3D' in data_name and disable_3d:
                     continue_next=True
               
               links_data['all']+=1
               if lk in all_lk:
                links_data['duplicated']+=1
                continue
               all_lk.append(lk)
               if lk in all_ok:
               
                
                info=(PTN.parse(clean_marks(name)))
                
                try:
                    info['title'] = re.findall("[a-zA-Z0-9. -_]+",info['title'])[0]
                except:
                    pass
                
                #info['title']=get_title(name)
                
                
                
                links_data['cached']+=1
                reject=False
                if tv_movie=='movie':
                    if 'year' in info:
                        if str(info['year'])!=show_original_year:
                            reject=True
                else:
                    if 'season' in info and 'episode' in info:
                        if str(info['season'])!=season or str(info['episode'])!=episode:
                            reject=True
         
                
                if clean_name(original_title,1).lower().replace('(',' ').replace(')',' ').replace('.',' ').replace('  ',' ').strip() != (info['title'].lower().replace('[I]','').replace('.',' ').replace('(',' ').replace(')',' ').replace('  ',' ')).strip() or reject:
                    if 0:
                        logging.warning(clean_name(original_title,1).lower())
                        logging.warning(info['title'].lower())
                        logging.warning(reject)
                        if 'year' in info:
                            logging.warning(info['year'])
                            logging.warning(show_original_year)
                    if continue_next:
                        all_filted_rejected.append(('[COLOR red][I]'+name+'[/I][/COLOR]',lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
                        continue
                    all_rejected.append(('[COLOR red][I]'+name+'[/I][/COLOR]',lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
                else:
                    if continue_next:
                        all_filted.append((name,lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
                        continue
                    all_data.append((name,lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
               else:
                links_data['un_cached']+=1
        if use_filter=='false':
            all_data=all_filted
            all_rejected=all_rejected
        all_data=sorted(all_data, key=lambda x: x[3], reverse=False)
        
        all_rejected=sorted(all_rejected, key=lambda x: x[3], reverse=False)
        
        all_2160=[]
        all_1080=[]
        all_720=[]
        all_rest=[]
        for name,lk,data,fix,quality,source in all_data:
            if fix==1:
                all_2160.append((name,lk,float(data),fix,quality,source))
            elif fix==2:
                all_1080.append((name,lk,float(data),fix,quality,source))
            elif fix==3:
                all_720.append((name,lk,float(data),fix,quality,source))
            else:
                all_rest.append((name,lk,float(data),fix,quality,source))
        
        all_2160=sorted(all_2160, key=lambda x: x[2], reverse=True)
        all_1080=sorted(all_1080, key=lambda x: x[2], reverse=True)
        all_720=sorted(all_720, key=lambda x: x[2], reverse=True)
        all_rest=sorted(all_rest, key=lambda x: x[2], reverse=True)
        
        all_data=all_2160+all_1080+all_720+all_rest+all_rejected
        all_dd=[]
        choise=[]
        for name,lk,data,fix,quality,source in all_data:
                color='white'
                if '2160' in quality or '4k' in quality.lower():
                    color='yellow'
                elif '1080' in quality:
                    color='lightblue'
                elif '720' in quality:
                    color='lightgreen'
                if '5.1' in name:
                    sound='-[COLOR khaki]5.1[/COLOR]-'
                elif '7.1' in name:
                    sound='-[COLOR khaki]7.1[/COLOR]-'
                else:
                    sound=''
                data=str(round(float(data), 2))
                try:
                    nm='[COLOR lightblue][B]'+name.encode('ascii','ignore')+'[/B][/COLOR]\n'
                except:
                  try:
                    nm='[COLOR lightblue][B]'+name+'[/B][/COLOR]\n'
                  except:
                    nm=name
                menu.append([source, source,sound,quality,nm,data+'GB',lk,''])
        
                all_dd.append(('[COLOR %s]%s-[/COLOR]%s[COLOR bisque][I]%s[/I][/COLOR]-%s'%(color,quality,sound,data+'GB',source,), lk, iconimage,fanart,nm+description,data,id,season,episode,original_title,show_original_year,json.dumps(dd)))
                choise.append(('[COLOR %s]%s-[/COLOR]%s[COLOR bisque][I]%s[/I][/COLOR]-%s'%(color,quality,sound,data+'GB',source,)))
                if not better_look:
                    addLink('[COLOR %s]%s-[/COLOR]%s[COLOR bisque][I]%s[/I][/COLOR]-%s'%(color,quality,sound,data+'GB',source,), lk,6,False, iconimage,fanart,nm+description,data=data,tmdb=id,season=season,episode=episode,original_title=original_title,year=show_original_year,dd=json.dumps(dd))
        
        if tv_movie=='movie':
            se='one_click'
            
        else:
            se='one_click_tv'
        if use_filter=='true' and len(all_filted)>0:
            menu.append(['', '','','','[COLOR red][I][B]--Open filtered links (%s)--[/I][/B][/COLOR]'%str(len(all_filted)),'','open_filtered',''])
            all_dd.append(('open_filtered', 'open_filtered', iconimage,fanart,description,data,id,season,episode,original_title,show_original_year,json.dumps(dd)))
        logging.warning('all_results:')
        logging.warning(links_data)
        result_string='All: '+str(links_data['all'])+', Dup.: '+str(links_data['duplicated'])+'[COLOR yellow] Cached: '+str(links_data['cached'])+'[/COLOR]'
        logging.warning('Start TRL')
        
        logging.warning('End TRl')
        one_click=Addon.getSetting(se)=='true'
        if len(menu)==0:
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'No links found')))
        if (one_click or better_look) and len(menu)>0:
            if better_look:
                
                menu2 = ContextMenu_new2('plugin.video.shadow', menu,iconimage,fanart,description,str(result_string),po_watching,l_full_stats)
                menu2.doModal()
                del menu2
                
                ret=selected_index
            else:
                ret = xbmcgui.Dialog().select("Choose link", choise)
            if ret!=-1:
                name,url,iconimage,fanart,description,data,id,season,episode,original_title,show_original_year,dd=all_dd[ret]
                #xbmc.executebuiltin("Dialog.Open(busydialog)")
                
                if name=='open_filtered':
                    name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,video_data_exp,all_w,use_filter=all_p_data[0]
                    str_next='XBMC.RunPlugin("plugin://plugin.video.shadow/?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&episode=%s&show_original_year=%s&video_data_exp=%s&all_w=%s&use_filter=false&mode=15")'%(urllib.quote_plus(name),'www',iconimage,fanart,urllib.quote_plus(description),data,urllib.quote_plus(original_title),id,season,episode,show_original_year,urllib.quote_plus(video_data_exp),urllib.quote_plus(all_w))
                    #xbmc.executebuiltin("Dialog.Close(busydialog)")
                    logging.warning(str_next)
                    xbmc.executebuiltin(str_next.encode('utf-8'))
                    
                    return 0
                xbmc.executebuiltin("ActivateWindow(10138)")
               
                play_link(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,dd,nextup='true',video_data_exp=video_data_exp,all_dd=all_dd,start_index=ret,all_w=all_w)
                xbmc.executebuiltin("Dialog.Close(busydialog)")
            else:
                
                s=stop_play()
                if s=='forceexit':
                    sys.exit(1)
                else:
                    return 0
    logging.warning('Show menu')
   
    logging.warning('Selected index:'+str(selected_index))
def ClearCache():
  
    logging.warning('Clear')
    cache.clear(['cookies', 'pages','posters'])
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'Cleared')))
def post_trk(id,season,episode,progress=False,len_progress='',type_progress=''):
    if len(id)>1 and id!='%20':
         if season!=None and season!="%20":
           '''
           logging.warning('tv')
           logging.warning(imdb_id)
           url_pre='http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s&language=en'%imdb_id.replace('tt','')
           html2=requests.get(url_pre).content
           pre_tvdb = str(html2).split('<seriesid>')
           if len(pre_tvdb) > 1:
                tvdb = str(pre_tvdb[1]).split('</seriesid>')
           logging.warning(tvdb)
           '''
           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
           if progress:
            ur='https://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d'%(id,season,episode)
            yy=requests.get(ur).json()['id']
            ddata={"progress": int(len_progress), "episode": {"ids": {"tmdb": yy}}}
            logging.warning(ddata)
            i = (post_trakt('/scrobble/'+type_progress, data=ddata))
           else:
               i = (post_trakt('/sync/history', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
           logging.warning('TRK')
           logging.warning(i)
         else:
           if progress:
               i = (post_trakt('/scrobble/'+type_progress,data= {'movie': {'ids': {'tmdb': id}}, 'progress': int(len_progress)}))
           else:
                i = (post_trakt('/sync/history',data= {"movies": [{"ids": {"tmdb": id}}]}))
         logging.warning('Watched Resoponce:')
         logging.warning(i)
def jump_seek(name,id,season,episode,jump_time,precentage):
    global break_jump,str_next
    
    time_to_save_trk=int(Addon.getSetting("time_to_save"))
    logging.warning('Waiting for jump')
    logging.warning(xbmc.Player().isPlaying())
    timeout=0
    break_jump=1
    done=0
    time_to_window=int(Addon.getSetting("window"))
    time_left=999999
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
       
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
    dbcon.commit()
    dbcur.execute("SELECT * FROM playback")
    match = dbcur.fetchall()
    dbcur.close()
    dbcon.close()
    all_d_nm=[]
    for nm,tm,se,ep,pl,to,fr in match:
        all_d_nm.append(nm+'$$$'+tm+'$$$'+se+'$$$'+ep)
    while timeout<200:
        timeout+=1
        if break_jump==0:
            break
        if xbmc.Player().isPlaying():
            break
        xbmc.sleep(100)
    mark_once=0
    counter_stop=0
   
    while xbmc.Player().isPlaying():
        
        if break_jump==0:
            break
        try:
        
            vidtime = xbmc.Player().getTime()
        except Exception as e:
            vidtime=0
            pass
        #logging.warning('Waiting for Vid2:'+str(vidtime))
        
        if vidtime>0.2:
            
            if precentage:
                
                g_item_total_time=xbmc.Player().getTotalTime()
                
                jump_time=((float(jump_time)*g_item_total_time)/100)
                
                precentage=False
            if round(float(jump_time))>round(float(vidtime)):
                
                logging.warning('jumping ahead:')
                logging.warning(jump_time)
                xbmc.Player().seekTime(int(float(jump_time)))
                jump_time=0
                
                
            
            try:
               if done==0:
                
                g_timer=xbmc.Player().getTime()
                g_item_total_time=xbmc.Player().getTotalTime()
                time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
                avg=(g_timer*100)/g_item_total_time
                if mark_once==0:
                    mark_once=1
                    post_trk(id,season,episode,progress=True,len_progress=int(avg),type_progress='start')
                    
                if (avg>time_to_save_trk):
                    logging.warning('Got precentage')
                    post_trk(id,season,episode)
                    done=1
            except Exception as e:
                logging.warning('Takt Err:'+str(e))
                pass
            
        xbmc.sleep(100)
    logging.warning('Saving')
    logging.warning(xbmc.Player().isPlaying())
    logging.warning(name+'$$$'+id+'$$$'+season+'$$$'+episode)
    logging.warning(g_timer)
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    if name+'$$$'+id+'$$$'+season+'$$$'+episode not in all_d_nm and g_timer>10 and g_item_total_time>300:
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s')"%(name.replace("'","%27"),id,season,episode,str(g_timer),str(g_item_total_time),''))
        dbcon.commit()
    else:
        dbcur.execute("UPDATE playback SET playtime='%s',total='%s' WHERE tmdb = '%s'"%(str(g_timer),str(g_item_total_time),id))
        dbcon.commit()
    post_trk(id,season,episode,progress=True,len_progress=int(avg),type_progress='pause')
    dbcur.close()
    dbcon.close()
    logging.warning('Waiting for Vid3:'+str(xbmc.Player().isPlaying()))
def load_test_data(title,icon,fanart,plot,s_title,season,episode,list):
    test_episode = {"episodeid": 0, "tvshowid": 0, "title": title, "art": {}}
    test_episode["art"]["tvshow.poster"] = icon
    test_episode["art"]["thumb"] = icon
    test_episode["art"]["tvshow.fanart"] = fanart
    test_episode["art"]["tvshow.landscape"] =fanart
    test_episode["art"]["tvshow.clearart"] = fanart
    test_episode["art"]["tvshow.clearlogo"] = icon
    test_episode["plot"] = plot
    test_episode["showtitle"] =s_title+' S%sE%s'%(season,episode)
    test_episode["playcount"] = 1
    test_episode["season"] =int( season)
    test_episode["episode"] = int(episode)
    test_episode["seasonepisode"] = "%sx%s"%(season,episode)
    test_episode["rating"] = None
    test_episode["firstaired"] = ""
    test_episode["list"]=list
    return test_episode
def calculate_progress_steps(period):
                    return (100.0 / int(period)) / 10
def search_next(dd,tv_movie,id):
   global silent,list_index,str_next,break_jump,sources_searching,clicked
   try:
    
    if len(str(id))==0:
        return 0
    if str(id)=='%20':
        return 0
    
    list_index=999
    count_timeout_sources=0
    while sources_searching:
        xbmc.sleep(100)
        count_timeout_sources+=1
        if count_timeout_sources>600:
            logging.warning('Timeout Search Sources')
            return 0
    logging.warning('Done Sources Searching')
    if tv_movie=='tv':
        str_next=''
        silent=True
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        
       
        dbcur.execute("SELECT * FROM nextup")
        match = dbcur.fetchall()
        dbcur.close()
        dbcon.close()
        
        for dd in match:
            dd_a=dd
        
        name,data,original_title,id,season,episode,show_original_year=json.loads(dd_a[0].decode('base64'))[0]
        episode=str(int(episode)+1)
        from resources.modules.tmdb import get_episode_data
     
        name_n,plot_n,image_n,season,episode=get_episode_data(id,season,str(int(episode)),o_name=original_title)
        
        time_to_save=int(Addon.getSetting("save_time"))
        
            
            
        match_a,all_ok,once,tv_movie,po_watching,l_full_stats= cache.get(c_get_sources, time_to_save,original_title,data,original_title,id,season,episode,show_original_year ,table='pages')
        logging.warning('Sources Ready:'+str(len(match_a)))
        dd=[]
        dd.append((original_title,data,original_title,id,season,episode,show_original_year))
        all_data=[]
        all_rejected=[]
        
                
        from resources.modules import PTN
        for items in match_a:
            for name,lk,data,quality in match_a[items]['links']:
               if lk in all_ok:
                    info=(PTN.parse(clean_marks(name)))
                    
                    try:
                        info['title'] = re.findall("[a-zA-Z0-9. -_]+",info['title'])[0]
                    except:
                        pass

                    reject=False
                    
                    if 'season' in info and 'episode' in info:
                            if str(info['season'])!=season or str(info['episode'])!=episode:
                                reject=True
             
                    
                    if clean_name(original_title,1).lower() != (info['title'].lower().replace('[I]','')) or reject:
                        all_rejected.append(('[COLOR red][I]'+name+'[/I][/COLOR]',lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
                    else:
                        all_data.append((name,lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
        logging.warning('Sources Ready after filter:'+str(len(all_data)))
        logging.warning('Sources Ready Rest filter:'+str(len(all_rejected)))
        all_data=sorted(all_data, key=lambda x: x[3], reverse=False)
        all_2160=[]
        all_1080=[]
        all_720=[]
        all_rest=[]
        for name,lk,data,fix,quality,source in all_data:
            if fix==1:
                all_2160.append((name,lk,data,fix,quality,source))
            elif fix==2:
                all_1080.append((name,lk,data,fix,quality,source))
            elif fix==3:
                all_720.append((name,lk,data,fix,quality,source))
            else:
                all_rest.append((name,lk,data,fix,quality,source))
        
        all_2160=sorted(all_2160, key=lambda x: x[2], reverse=True)
        all_1080=sorted(all_1080, key=lambda x: x[2], reverse=True)
        all_720=sorted(all_720, key=lambda x: x[2], reverse=True)
        all_rest=sorted(all_rest, key=lambda x: x[2], reverse=True)
        all_data=all_2160+all_1080+all_720+all_rest+all_rejected
        list=[]
        all_dd=[]
        for name,lk,data,fix,quality,source in all_data:
                all_dd.append((name,lk,' ',' ',' ',data,id,season,episode,original_title,show_original_year,dd))
                color='white'
                if '2160' in quality or '4k' in quality.lower():
                    color='yellow'
                elif '1080' in quality:
                    color='lightblue'
                elif '720' in quality:
                    color='lightgreen'
                if '[COLOR red]' in name:
                    color='red'
                if '5.1' in name:
                    sound='-[COLOR khaki]5.1[/COLOR]-'
                elif '7.1' in name:
                    sound='-[COLOR khaki]7.1[/COLOR]-'
                else:
                    sound=''
                list.append('[COLOR %s]%s-[/COLOR]%s[COLOR bisque][I]%s[/I][/COLOR]-%s'%(color,quality,sound,data+'GB',source,)+'$$$$$$$'+lk)
    time_to_save_trk=int(Addon.getSetting("time_to_save"))
    logging.warning('Waiting for jump')
    logging.warning(xbmc.Player().isPlaying())
    timeout=0
    break_jump=1
    done=0
    if tv_movie=='tv':
      time_to_window=int(Addon.getSetting("window"))
    else:
        time_to_window=int(Addon.getSetting("movie_window"))
    time_left=999999
    while timeout<200:
        timeout+=1
        if break_jump==0:
            break
        if xbmc.Player().isPlaying():
            break
        xbmc.sleep(100)
    play_next=False
    count_ok=0
    while xbmc.Player().isPlaying():
        if break_jump==0:
            break
        try:
        
            vidtime = xbmc.Player().getTime()
        except Exception as e:
            vidtime=0
            pass
        #logging.warning('Waiting for Vid2:'+str(vidtime))
        
        if vidtime>10:
            try:
               
                g_timer=xbmc.Player().getTime()
                g_item_total_time=xbmc.Player().getTotalTime()
                if xbmc.Player().getTotalTime()>10 and xbmc.Player().getTime()>10:
                
                    time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
                
            except Exception as e:
                logging.warning('Takt Err:'+str(e))
                pass
            if (time_left<time_to_window) :
                count_ok+=1
            else:
                count_ok=0
            logging.warning('error counter:'+str(count_ok))
            if count_ok>10 :
              logging.warning('Ready to play next')
              play_next=True
              break
        xbmc.sleep(100)
    if break_jump==0:
            return 0
    if play_next:
     
      if tv_movie=='tv':
        from resources.modules.tmdb import get_episode_data
        logging.warning('Getting next episode')
        name_n,plot_n,image_n,season,episode=get_episode_data(id,season,str(int(episode)),o_name=original_title)
        logging.warning('Got it')
        next_up_page = UpNext("script-upnext-upnext.xml",Addon.getAddonInfo('path'), "DefaultSkin", "1080i")
        
        ep=load_test_data(name_n,image_n,image_n,plot_n,name_n,season,episode,list)
        
            
        next_up_page.setItem(ep)

        next_up_page.setProgressStepSize(calculate_progress_steps(30))
        next_up_page.doModal()
        del next_up_page
        logging.warning('clicked:'+str(clicked))
        if (Addon.getSetting('play_nextup_wait')=='false' and clicked==False) or len(list)==0:
                    return '0'
        if list_index!=999 and list_index!=888:
            xbmc.Player().stop()
            xbmc.sleep(2)
            logging.warning('Stoped')
            if len(list)==0:
                xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'No links found')))
                sys.exit()
            else:
                logging.warning(list_index)
                logging.warning('Link to play...:'+list[list_index])
                fast_link=list[list_index].split('$$$$$$$')[1]
        
                logging.warning('Link to play:'+fast_link)
        else:
            return '0'
        dd=[]
        dd.append((name,data,original_title,id,season,episode,show_original_year))

        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup_all_d')
        dbcur.execute("DELETE FROM nextup")
        dbcur.execute("DELETE FROM nextup_all_d")
        dbcur.execute("INSERT INTO nextup Values ('%s')"%(json.dumps(dd).encode('base64')))
        dbcur.execute("INSERT INTO nextup_all_d Values ('%s')"%(json.dumps(all_dd).encode('base64')))
        dbcon.commit()
        
        dbcur.close()
        dbcon.close()
        logging.warning('Nextup episode:'+episode)
        
        str_next='XBMC.RunPlugin("plugin://plugin.video.shadow/?nextup=true&url=%s&no_subs=0&season=%s&episode=%s&mode=6&original_title=%s&id=%s&dd=%s&data=%s&fanart=%s&iconimage=%s&name=%s&description=%s&get_sources_nextup=true")'%(urllib.quote_plus(fast_link),season,episode,original_title,id,dd,data,fanart,iconimage,name_n,plot_n)
        xbmc.executebuiltin(str_next.encode('utf-8'))
      else:
      
        window = fav_mv('plugin.video.shadow',id)
        window.doModal()

        del window
                    
    logging.warning('Next Episode Done')
   except Exception as e:
    import linecache
    sources_searching=False
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    logging.warning('ERROR IN Play IN:'+str(lineno))
    logging.warning('inline:'+line)
    logging.warning('Error:'+str(e))
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'PlayinLine:'+str(lineno))))
   
    pass
def simple_play(name,url):
        
        rd = real_debrid.RealDebrid()
        if 'Direct$$$$' in url:
            url=url.replace('Direct$$$$','')
            
            info=rd.torrentInfo(url)
            all_nm=[]
            all_lk=[]
            all_t=[]
            for items in info['links']:
                all_lk.append(items)
            count=0
            for items in info['files']:
               
                if (len(all_lk)-1)<count:
                    break
                all_t.append((items['path'].replace('/',''),all_lk[count]))
                count+=1
                
            
            all_t=sorted(all_t, key=lambda x: x[0], reverse=False)
            for nm,lk in all_t:
                all_nm.append(nm)
            if len(all_nm)==1:
                name,link=all_t[0]
            else:
                ret = xbmcgui.Dialog().select("Choose", all_nm)
                if ret!=-1:
                    name,link=all_t[ret]
            
                    
                else:
                
                    s=stop_play()
                    if s=='forceexit':
                        sys.exit(1)
                    else:
                        return 0
                    
            
            
            link=rd.unrestrict_link(link)
        elif '[' in url:
            all_ur=json.loads(url)
            all_nam=[]
            for items in all_ur:
                items_s=items.split('/')
                
                all_nam.append(items_s[len(items_s)-1])
            ret = xbmcgui.Dialog().select("Choose", all_nam)
            if ret!=-1:
                link=all_ur[ret]
                try:
                    link=urllib.unquote_plus(link)
                except:
                    pass
            else:
            
                s=stop_play()
                if s=='forceexit':
                    sys.exit(1)
                else:
                    return 0
        if link==None:
            xbmcgui.Dialog().ok('Error','[COLOR aqua][I] Item was removed from RD [/I][/COLOR]')
            s=stop_play()
            if s=='forceexit':
                sys.exit(1)
            else:
                return 0
                
        listItem = xbmcgui.ListItem(name, path=link) 
        
      
        listItem.setInfo(type='Video', infoLabels={'title':name}) 
        ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
def play_link(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,dd,nextup='false',video_data_exp={},all_dd=[],start_index=0,get_sources_nextup='false',all_w={}):
   try:
    direct=False
 
    if 'magnet' not in url:
        direct=True
        nextup='false'
    logging.warning('Episode:'+episode)
    
    logging.warning('URL::'+url)
    episode=episode.replace('+',"%20")
    global break_jump,all_w_global
    break_jump=0
  
    tmdbKey = '653bb8af90162bd98fc7ee32bcbbfb3d'
    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode
    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
    
    try:
        s=int(season)
        tv_movie='tv'
        
    except:
        tv_movie='movie'
    if direct==False:
        if Addon.getSetting('debrid_select')=='0':
           rd = real_debrid.RealDebrid()
          
           if tv_movie=='tv' and 's%se'%season_n not in url.lower():
               logging.warning('Play mode::season play')
               logging.warning(get_sources_nextup)
               if get_sources_nextup=='true':
                    try:
                        from sqlite3 import dbapi2 as database
                    except:
                        from pysqlite2 import dbapi2 as database
                    cacheFile=os.path.join(user_dataDir,'database.db')
                    dbcon = database.connect(cacheFile)
                    dbcur = dbcon.cursor()
                    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup_all_d')
                    dbcur.execute("SELECT * from nextup_all_d")
                    
                    
                    all_dd_pre = dbcur.fetchone()
                    
                    dbcur.close()
                    dbcon.close()
                    if all_dd_pre!=None:
                        all_dd=json.loads(all_dd_pre[0].decode('base64'))
                    start_index=0
                    for name,n_url,iconimage,fanart,description,data,id,season,episode,original_title,show_original_year,dd in all_dd:
                        if url==n_url:
                            break
                        start_index+=1
               if len(all_dd)>0:
                logging.warning('LEN ALLDD:'+str(len(all_dd)))
                counter_index=0
                start_time=time.time()
                dp = xbmcgui.DialogProgress()
                dp.create("Collecting", "Please wait", '')
                 
                elapsed_time = time.time() - start_time
                dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'playing', '')
             
                xxx=0
                for name,url,iconimage,fanart,description,data,id,season,episode,original_title,show_original_year,dd in all_dd:
                    if counter_index>=start_index:
                        logging.warning('Trying22:')
                        link=rd.singleMagnetToLink_season(url,tv_movie,season_n,episode_n,dp=dp)
                        logging.warning('Trying:'+str(link))
                        dp.update(int(((xxx* 100.0)/(len(all_dd)-selected_index)) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'playing', str(counter_index)+'/'+str(len(all_dd)-selected_index))
                        xxx+=1
                        if dp.iscanceled():
                            dp.close()
                            break
                        logging.warning(counter_index)
                        logging.warning(link)
                        if link!=None:
                            dp.close()
                            break
                    
                    counter_index+=1
                    
               
           else:
                logging.warning('Play mode::one play')
                link=rd.singleMagnetToLink(url)
        elif Addon.getSetting('debrid_select')=='1':
            pr= premiumize.Premiumize()
            link=pr._single_magnet_resolve(url)
        else:
            ad=all_debrid.AllDebrid()
            link=ad.movie_magnet_to_stream(url)
    else:
        link=url
    try:
        c=int(season)
        tv=True
    except:
       tv=False
       season='%20'
    
    
  
    
    video_data={}
    if season!=None and season!="%20":
       video_data['TVshowtitle']=original_title
       video_data['mediatype']='episode'
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids'%(id,tmdbKey)
    else:
       video_data['mediatype']='movie'
       url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids'%(id,tmdbKey)
    try:
        logging.warning(url2)
        imdb_id=requests.get(url2,timeout=10).json()['external_ids']['imdb_id']
    except:
        imdb_id=" "
    logging.warning('imdb_id:'+str(imdb_id))
    video_data['title']=original_title
    video_data['icon']=iconimage
    video_data['original_title']=name
    video_data['plot']=description
    video_data['year']=show_original_year
    video_data['season']=season
    video_data['episode']=episode
    video_data['poster']=fanart
    video_data['poster3']=fanart
    video_data['fanart2']=fanart
    video_data['imdb']=imdb_id
    video_data['code']=imdb_id
    video_data['IMDBNumber']=imdb_id
    
    
    
 
    logging.warning(link)
    if link:
        listItem = xbmcgui.ListItem(video_data['title'], path=link) 
        
        if video_data_exp!={}:
            video_data=json.loads(video_data_exp)
            #if video_data['mediatype']=='tvshow':
            #    video_data['mediatype']='episode'
        
        listItem.setInfo(type='Video', infoLabels=video_data)

        listItem.setArt({'icon': iconimage, 'thumb': iconimage, 'poster': fanart,'tvshow.poster': fanart, 'season.poster': fanart})
        video_streaminfo = {'codec': 'h264'}
        #listItem.addStreamInfo('video', video_streaminfo)
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
           
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        dbcon.commit()
        
        dbcur.execute("SELECT * FROM playback where name='%s' and tmdb='%s' and season='%s' and episode='%s'"%(original_title.replace("'",'%27'),id,season,episode))
        
        match_playtime = dbcur.fetchone()
        logging.warning(match_playtime)
        #return 0
        res=False
        if match_playtime!=None:
            name_r,timdb_r,season_r,episode_r,playtime,totaltime,free=match_playtime
            res={}
            res['wflag']=False
            res['resumetime']=playtime
            res['totaltime']=totaltime
        
        jump_time=0
        if Addon.getSetting("trakt_access_token")!='':
           logging.warning('Playing all_w_global:')
           logging.warning(all_w_global)
           if all_w_global!={}:
                all_w=all_w_global
           falback=False
           try:
            logging.warning('Mark start')
            
            logging.warning('All_w::')
            logging.warning(all_w)
            
            if str(all_w)!='{}':
              j_aa_w=json.loads(all_w)
              if id in j_aa_w:
                res={}
                falback=True
                if 'precentage' in j_aa_w[id]:
                   res['wflag']=False
                   res['resumetime']=j_aa_w[id]['precentage']
                else:
                
                    res['wflag']=False
                    res['resumetime']=j_aa_w[id]['resume']
                    res['totaltime']=j_aa_w[id]['totaltime']
           except Exception as e:
             logging.warning('Error in resume2:'+str(e))
             if falback:
                res=False
             pass
        precentage=False
        logging.warning('res::'+str(res))
        if res and 'precentage' not in all_w:
           
            if float(res['resumetime'])>10 and (100*(float(res['resumetime'])/float(res['totaltime'])))<95:
                choose_time='Resume from '+time.strftime("%H:%M:%S", time.gmtime(float(res['resumetime'])))
                selection =selection_time('Menu',choose_time)
                #window = selection_time('Menu',choose_time)
                #window.doModal()
                #selection = window.get_selection()
                #del window
                logging.warning('selection:'+str(selection))
                if selection!=-1:
                    
                    if selection==1:
                        
                        jump_time=0
                        listItem.setProperty('resumetime', u'0')
                        listItem.setProperty('totaltime', res['totaltime'])
                    else:
                        jump_time=res['resumetime']
                        listItem.setProperty('resumetime', res['resumetime'])
                        listItem.setProperty('totaltime', res['totaltime'])
                else:
                    s=stop_play()
                    if s=='forceexit':
                        sys.exit(1)
                    else:
                        return 0
            else:
                jump_time=0
        elif 'precentage'  in all_w:
            if float(res['resumetime'])>1 and float(res['resumetime'])<95:
                precentage=True
                choose_time='Resume from '+res['resumetime']+'%'
                selection =selection_time('Menu',choose_time)
               
               
                if selection!=-1:
                    
                    if selection==1:
                        
                        jump_time=0
                        
                    else:
                        jump_time=res['resumetime']
                        
                else:
                    s=stop_play()
                    if s=='forceexit':
                        sys.exit(1)
                    else:
                        return 0
            else:
                jump_time=0
        dbcur.close()
        dbcon.close()
        
        if nextup=='true':
            ok=xbmc.Player().play(link,listitem=listItem,windowed=False)
            ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
        else:
            ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        if season!=None and season!="%20":
           table_name='lastlinktv'
        else:
           table_name='lastlinkmovie'
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""id TEXT);"%table_name)
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
        
        dbcon.commit()
        dbcur.execute("DELETE FROM %s"%table_name)
                 
        match = dbcur.fetchone()
         
        if match==None:
            dbcur.execute("INSERT INTO %s Values ('f_name','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s');" %  (table_name,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '))
            dbcon.commit()
            try:
                try:
                    desk=description.replace("'","%27").encode('utf-8')
                except:
                    desk=''
                dbcur.execute("UPDATE %s SET name='%s',url='%s',iconimage='%s',fanart='%s',description='%s',data='%s',season='%s',episode='%s',original_title='%s',saved_name='%s',heb_name='%s',show_original_year='%s',eng_name='%s',isr='%s',prev_name='%s',id='%s' WHERE o_name = 'f_name'"%(table_name,original_title.replace("'","%27"),url.encode('base64'),iconimage,fanart,desk,str(show_original_year).replace("'","%27"),season,episode,original_title.replace("'","%27"),original_title.replace("'","%27"),original_title.replace("'","%27"),show_original_year,original_title.replace("'","%27").replace("'","%27"),'0',original_title.replace("'","%27"),id))
                dbcon.commit()
            except Exception as e:
                logging.warning('Error in Saving Last:'+str(e))
                pass
        
        if table_name=='lastlinktv':
            tv_movie='tv'
        else:
            tv_movie='movie'
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27"),tv_movie))

        match = dbcur.fetchone()
        if match==None:
          try:
            dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (original_title.replace("'","%27"),url,iconimage,fanart,descriptio.replace("'","%27"),show_original_year,original_title.replace("'","%27"),season,episode,id,original_title.replace("'","%27"),show_original_year,original_title.replace("'","%27"),'0',tv_movie))
          except:
            try:
                dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (original_title.replace("'","%27"),url,iconimage,fanart,description.decode('utf-8').replace("'","%27"),show_original_year,original_title.replace("'","%27"),season,episode,id,original_title.replace("'","%27"),show_original_year,original_title.replace("'","%27"),'0',tv_movie))
            except:
                dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (original_title.replace("'","%27"),url,iconimage,fanart,' ',show_original_year,original_title.replace("'","%27"),season,episode,id,original_title.replace("'","%27"),show_original_year,original_title.replace("'","%27"),'0',tv_movie))
          dbcon.commit()
         
        else:
          dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s' and season='%s' and episode='%s'"%(original_title.replace("'","%27"),tv_movie,season,episode))

          match = dbcur.fetchone()
         
          if match==None:
            dbcur.execute("UPDATE Lastepisode SET season='%s',episode='%s',image='%s',heb_name='%s' WHERE original_title = '%s' and type='%s'"%(season,episode,fanart,original_title.replace("'","%27"),original_title.replace("'","%27"),tv_movie))
            dbcon.commit()
                
        dbcur.close()
        dbcon.close()
        if id!='%20':
                try:
                    c=int(season)
                    tv=True
                except:
                   tv=False
        
                if season!=None and season!="%20" and tv :
                   '''
                   logging.warning('tv')
                   logging.warning(imdb_id)
                   url_pre='http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s&language=en'%imdb_id.replace('tt','')
                   html2=requests.get(url_pre).content
                   pre_tvdb = str(html2).split('<seriesid>')
                   if len(pre_tvdb) > 1:
                        tvdb = str(pre_tvdb[1]).split('</seriesid>')
                   logging.warning(tvdb)
                   '''
                   season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
                   
                   i = (post_trakt('/sync/watchlist', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
                else:
                   
                   i = (post_trakt('/sync/watchlist',data= {"movies": [{"ids": {"tmdb": id}}]}))
                logging.warning('Trakt Resoponce:')
                logging.warning(i)

        if str(id)!='0' and str(id)!='+':
            thread=[]
            
            thread.append(Thread(jump_seek,original_title,id,season,episode,jump_time,precentage))
                
            
            thread[0].start()
            try:
                s=int(season)
                tv_movie='tv'
                video_data['mediatype']='episode'
            except:
                tv_movie='movie'
                video_data['mediatype']='movie'
            
                
                
                
            #search_next(dd)
            logging.warning('Player Done')
            logging.warning('Nextup')
            if (Addon.getSetting("nextup_episode")=='true' and tv_movie=='tv') or (Addon.getSetting("nextup_movie")=='true' and tv_movie=='movie'):
                thread=[]
                    
                thread.append(Thread(search_next,dd,tv_movie,id))
                    
                
                thread[0].start()
        
   except Exception as e:
      import linecache
      exc_type, exc_obj, tb = sys.exc_info()
      f = tb.tb_frame
      lineno = tb.tb_lineno
      filename = f.f_code.co_filename
      linecache.checkcache(filename)
      line = linecache.getline(filename, lineno, f.f_globals)
      
      logging.warning('ERROR IN Playing:'+str(lineno))
      logging.warning('inline:'+line)
      logging.warning(e)
      xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'inLine:'+str(lineno)+str(e))))

def clear_rd():
    Addon.setSetting('rd.client_id','')
    Addon.setSetting('rd.auth','')
    Addon.setSetting('rd.refresh','')
    Addon.setSetting('rd.secret','')
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', ('Cleared').decode('utf8'))).encode('utf-8'))
def re_enable_rd():
    clear_rd()

    rd = real_debrid.RealDebrid()
    logging.warning('Enable_Rd')
    #rd.auth()
    logging.warning('Enable_RdDD')
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', ('OK').decode('utf8'))).encode('utf-8'))
def clear_pr():
    Addon.setSetting('premiumize.token','')
    
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', ('Cleared').decode('utf8'))).encode('utf-8'))
def clear_all_d():
    Addon.setSetting('alldebrid.token','')
    
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', ('Cleared').decode('utf8'))).encode('utf-8'))
def re_enable_pr():
    
    pr = premiumize.Premiumize()
    pr.auth()
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', ('OK').decode('utf8'))).encode('utf-8'))
def re_enable_all_d():
    
    alld = all_debrid.AllDebrid()
    alld.auth()
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', ('OK').decode('utf8'))).encode('utf-8'))
def add_remove_trakt(name,original_title,id,season,episode):

    if original_title=='add':
        if name=='tv':
         
           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
           
           i = (post_trakt('/sync/history', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
        else:
          
           i = (post_trakt('/sync/history',data= {"movies": [{"ids": {"tmdb": id}}]}))
    elif original_title=='remove':
        if name=='tv':
         
           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
           
           i = (post_trakt('/sync/history/remove', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
        else:
         
           i = (post_trakt('/sync/history/remove',data= {"movies": [{"ids": {"tmdb": id}}]}))
    if 'added' in i:
       xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'Marked as watched'.encode('utf-8'))))
    elif 'deleted' in i:
       xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'Watched removed'.encode('utf-8'))))
    else:
      xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'Error'.encode('utf-8'))))
    ClearCache()
    xbmc.executebuiltin('Container.Refresh')
def calendars():
        import datetime
        datetime_get = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        m = "January|February|March|April|May|June|July|August|September|October|November|December".encode('utf-8').split('|')
        try: months = [(m[0], 'January'), (m[1], 'February'), (m[2], 'March'), (m[3], 'April'), (m[4], 'May'), (m[5], 'June'), (m[6], 'July'), (m[7], 'August'), (m[8], 'September'), (m[9], 'October'), (m[10], 'November'), (m[11], 'December')]
        except: months = []

        d = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday".encode('utf-8').split('|')
        try: days = [(d[0], 'Monday'), (d[1], 'Tuesday'), (d[2], 'Wednesday'), (d[3], 'Thursday'), (d[4], 'Friday'), (d[5], 'Saturday'), (d[6], 'Sunday')]
        except: days = []
        list=[]
        calendar_link = 'https://api.tvmaze.com/schedule?date=%s'
        for i in range(0, 30):
            if 1:#try:
                name = (datetime_get - datetime.timedelta(days = i))
                name = ("[B]%s[/B] : %s" % (name.strftime('%A'), name.strftime('%d %B'))).encode('utf-8')
                for m in months: name = name.replace(m[1], m[0])
                for d in days: name = name.replace(d[1], d[0])
                try: name = name.encode('utf-8')
                except: pass

                url = calendar_link % (datetime_get - datetime.timedelta(days = i)).strftime('%Y-%m-%d')

                list.append({'name': name, 'url': url, 'image': 'calendar.png', 'action': 'calendar'})
            #except:
            #    pass
        
        return list
        
def c_get_tv_maze(urls,original_image):
   all_d=[]
   for url in urls:
    logging.warning(url)
    x=requests.get(url,headers=base_header).json()
    
    for items in x:
        season=str(items['season'])
        if items['number']==None:
            episode='1'
        else:
            episode=str(int(items['number']))
        
        if len(episode)==1:
          episode_n="0"+episode
        else:
           episode_n=episode
        if len(season)==1:
          season_n="0"+season
        else:
          season_n=season
        
        id=items['show']['externals']['thetvdb']
        if id==None:
            id=items['show']['externals']['imdb']
            id='imdb'+str(id)
        else:
            id='tvdb'+str(id)
            
        '''
        url2=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=tvdb_id&language=%s'%(imdb_id,lang)
        logging.warning(items['show']['externals'])
        html_im=requests.get(url2).json()
       
        data=html_im['tv_results']
        if len(data)==0:
            continue
        else:
            data=data[0]
        title=data['name']+' -S%sE%s - '%(season_n,episode_n)
        plot=items['airdate']+'\n'+data['overview']
        if data['poster_path']==None:
            data['poster_path']=''
        if data['backdrop_path']==None:
            data['backdrop_path']=''
        icon='https://image.tmdb.org/t/p/original/'+data['poster_path']
        fan='https://image.tmdb.org/t/p/original/'+data['backdrop_path']
        id=str(data['id'])
        original_name=data['original_name']
        eng_name=original_name
        if 'first_air_date' in data:
           year=str(data['first_air_date'].split("-")[0])
        elif 'release_date' in data:
            year=str(data['release_date'].split("-")[0])
        else:
            year='0'
        '''
        title=items['show']['name']+' -S%sE%s- %s'%(season_n,episode_n,items['name'])
        plot=items['show']['summary']
        if plot==None:
            plot=''
        plot=items['airdate']+'\n'+plot
        icon=' '
        if items['show']['image']==None:
            icon=original_image
        else:
         for it in items['show']['image']:
           icon=items['show']['image'][it]
        fan=icon
       
        original_name=items['show']['name']
        eng_name=items['show']['name']
        if 'premiered' in items:
           year=str(data['premiered'].split("-")[0])
       
        else:
            year='0'
        all_g=[]
        for it in items['show']['genres']:
            all_g.append(it)
        generes=','.join(all_g)
        
        aa=addDir3( title, 'www',15, icon,fan,plot,data=year,generes=generes,original_title=original_name,id=id,season=season,episode=episode,eng_name=eng_name,show_original_year=year,heb_name=original_name)
        all_d.append(aa)
   return all_d
def get_tv_maze(url,original_image):
    urls = [i['url'] for i in calendars()][:5]
    logging.warning(urls)
    
    all_d=c_get_tv_maze(urls,original_image)
    
    #time_to_save=int(Addon.getSetting("save_time"))
    #all_d=cache.get(c_get_tv_maze, time_to_save, urls,original_image)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def play_trailer(id,tv_movie):
    logging.warning('playing shadow Trailer')
    if tv_movie=='tv':
        url_t='http://api.themoviedb.org/3/tv/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id
        logging.warning(url_t)
        html_t=requests.get(url_t).json()
        if len(html_t['results'])==0:
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'No trailer')))
            return 
    else:
        url_t='http://api.themoviedb.org/3/movie/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id
        logging.warning(url_t)
        html_t=requests.get(url_t).json()
        if len(html_t['results'])==0:
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'No trailer')))
            return 
        if 'results' not in html_t:
            
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'No Trailer')))
            sys.exit()
        
    if len(html_t['results'])>1:
        all_nm=[]
        all_lk=[]
        for items in html_t['results']:
            all_nm.append(items['name']+","+str(items['size']))
            all_lk.append(items['key'])
        
        ret = xbmcgui.Dialog().select("Choose trailer", all_nm)
        if ret!=-1:
            video_id=(all_lk[ret])
        else:
            return 0
    else:
        video_id=(html_t['results'][0]['key'])
    from resources.modules.youtube_ext import get_youtube_link2
    playback_url=''
    if video_id!=None:
      try:
        logging.warning(video_id)
        playback_url= get_youtube_link2('https://www.youtube.com/watch?v='+video_id).replace(' ','%20')
        logging.warning(playback_url)
    
      except Exception as e:
            logging.warning('Error playing youtube:'+str(e))
            pass
      #from pytube import YouTube
      #playback_url = YouTube(domain_s+'www.youtube.com/watch?v='+video_id).streams.first().download()
         
       
        
      #playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
      item = xbmcgui.ListItem(path=playback_url)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
def search_history(url,icon,fan):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
   
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""tv_movie TEXT );" % 'search_string2')
   
    dbcon.commit()
    logging.warning('URL:'+url)
    if url=='both':
        dbcur.execute("SELECT * FROM search_string2 where tv_movie='tv'")
    else:
        dbcur.execute("SELECT * FROM search_string2 where tv_movie='%s'"%url)
    match = dbcur.fetchall()
    all=[]
    type_pre='none'
    for qua,type in match:
    
        if type!=type_pre and url=='both':
           aa=addNolink( '[COLOR blue][I]---%s---[/I][/COLOR]'%type, id,27,False,fanart=' ', iconimage=' ',plot=' ',dont_place=True)
           all.append(aa)
           type_pre=type
        aa=addDir3(qua,'http://api.themoviedb.org/3/search/{0}?api_key=34142515d9d23817496eeb4ff1d223d0&query={1}&language={2}&page=1'.format(type,qua,lang),14,BASE_LOGO+'search.png','https://www.york.ac.uk/media/study/courses/postgraduate/centreforlifelonglearning/English-Building-History-banner-bought.jpg','TMDB')
        all.append(aa)
        
    if url=='both':
        dbcur.execute("SELECT * FROM search_string2 where tv_movie='movie'")
        match = dbcur.fetchall()
 
        type_pre='none'
        for qua,type in match:

            if type!=type_pre and url=='both':
               aa=addNolink( '[COLOR blue][I]---%s---[/I][/COLOR]'%type, id,27,False,fanart=' ', iconimage=' ',plot=' ',dont_place=True)
               all.append(aa)
               type_pre=type
            aa=addDir3(qua,'http://api.themoviedb.org/3/search/{0}?api_key=34142515d9d23817496eeb4ff1d223d0&query={1}&language={2}&page=1'.format(type,qua,lang),14,BASE_LOGO+'search.png','https://www.york.ac.uk/media/study/courses/postgraduate/centreforlifelonglearning/English-Building-History-banner-bought.jpg','TMDB')
            all.append(aa)
    dbcur.close()
    dbcon.close()
    aa=addNolink( '[COLOR khaki][I]---Clear %s History---[/I][/COLOR]'%url,url,148,False,fanart=fan, iconimage=icon,plot='Clear %s History'%url,dont_place=True)
    all.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
def  last_played():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    
    table_name='lastlinktv'
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""id TEXT);"%table_name)
    
    table_name='lastlinkmovie'
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""id TEXT);"%table_name)
    
    
    dbcur.execute("SELECT * FROM lastlinktv WHERE o_name='f_name'")

    match_tv = dbcur.fetchone()
    
    dbcur.execute("SELECT * FROM lastlinkmovie WHERE o_name='f_name'")

    match_movie = dbcur.fetchone()
    
    dbcon.commit()
    
    dbcur.close()
    dbcon.close()
    all=[]
    if match_tv!=None:
       aa=addNolink( '[COLOR blue][I]---TV---[/I][/COLOR]', 'www',27,False,fanart=' ', iconimage=' ',plot=' ',dont_place=True)
       all.append(aa)
       f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match_tv
       try:
           if url!=' ':
             if 'http' not  in url:
           
               url=url.decode('base64')
             if len(episode)==1:
              episode_n="0"+episode
             else:
               episode_n=episode
             if len(season)==1:
              season_n="0"+season
             else:
              season_n=season
             aa=addLink(original_title+' - S%sE%s'%(season_n,episode_n), url,6,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season=season,episode=episode,tmdb=id,year=show_original_year,place_control=True)
             all.append(aa)
       except  Exception as e:
         logging.warning(e)
         pass
    if match_movie!=None:
       aa=addNolink( '[COLOR blue][I]---Movie---[/I][/COLOR]', 'www',27,False,fanart=' ', iconimage=' ',plot=' ',dont_place=True)
       all.append(aa)
       f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match_movie
       try:
           if url!=' ':
             if 'http' not  in url:
           
               url=url.decode('base64')
              
             aa=addLink(original_title, url,6,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season='%20',episode='%20',tmdb=id,year=show_original_year,place_control=True)
             all.append(aa)
       except  Exception as e:
         logging.warning(e)
         pass
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
def get_one_trk(color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image):
          global all_data_imdb
          import _strptime
          data_ep=''
          dates=' '
          fanart=image
          url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(id,season)
         
          html=requests.get(url).json()
          next=''
          ep=0
          f_episode=0
          catch=0
          counter=0
          if 'episodes' in html:
              for items in html['episodes']:
                if 'air_date' in items:
                   try:
                       datea=items['air_date']+'\n'
                       
                       a=(time.strptime(items['air_date'], '%Y-%m-%d'))
                       b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
                      
                   
                       if a>b:
                         if catch==0:
                           f_episode=counter
                           
                           catch=1
                       counter=counter+1
                       
                   except:
                         ep=0
          else:
             ep=0
          episode_fixed=int(episode)-1
          try:
              plot=html['episodes'][int(episode_fixed)]['overview']
          
              ep=len(html['episodes'])
              try:
                  if (html['episodes'][int(episode_fixed)]['still_path'])==None:
                    fanart=image
                  else:
                    fanart=domain_s+'image.tmdb.org/t/p/original/'+html['episodes'][int(episode_fixed)]['still_path']
              except:
                fanart=image
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'Season '+season+'-Episode '+episode+ '[/COLOR]\n[COLOR gold] out of ' +str(f_episode)  +' episode for this season[/COLOR]\n' 
              try:
                  if int(episode)>1:
                    
                    prev_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)-1]['air_date'], '%Y-%m-%d'))) 
                  else:
                    prev_ep=0
              except:
                prev_ep=0

          

                      
              if int(episode)<ep:

                if (int(episode)+1)>=f_episode:
                  color_ep='magenta'
                  next_ep='[COLOR %s]'%color_ep+time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) +'[/COLOR]'
                else:
                  
                  next_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
              else:
                next_ep=0
              dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
              if int(episode)<int(f_episode):
               color='gold'
              else:
               color='white'
               h2=requests.get('https://api.themoviedb.org/3/tv/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US'%id).json()
               last_s_to_air=int(h2['last_episode_to_air']['season_number'])
               last_e_to_air=int(h2['last_episode_to_air']['episode_number'])
              
               if int(season)<last_s_to_air:
      
                 color='lightblue'
            
               if h2['status']=='Ended' or h2['status']=='Canceled':
                color='peru'
               
               
               if h2['next_episode_to_air']!=None:
                 
                 if 'air_date' in h2['next_episode_to_air']:
                  
                  a=(time.strptime(h2['next_episode_to_air']['air_date'], '%Y-%m-%d'))
                  next=time.strftime( "%d-%m-%Y",a)
                  
               else:
                  next=''
                 
          except Exception as e:
              import linecache,sys
              exc_type, exc_obj, tb = sys.exc_info()
              f = tb.tb_frame
              lineno = tb.tb_lineno
              logging.warning('Error :'+ heb_name)
              logging.warning('Error :'+ str(e) +',line no:'+str(lineno))
              plot=' '
              color='green'
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'Season '+season+'-Episode '+episode+ '[/COLOR]\n[COLOR gold] out of ' +str(f_episode)  +' episode for this season [/COLOR]\n' 
              dates=' '
              fanart=image
          try:
            f_name=urllib.unquote_plus(heb_name.encode('utf8'))
     
          except:
            f_name=name
          if (heb_name)=='':
            f_name=name
          if color=='peru':
            add_p='[COLOR peru][B]This show was over or canceled[/B][/COLOR]'+'\n'
          else:
            add_p=''
          add_n=''
          if color=='white' and url_o=='tv' :
              if next !='':
                add_n='[COLOR tomato][I]Next episode at ' +next+'[/I][/COLOR]\n'
              else:
                add_n='[COLOR tomato][I]Next episode at ' +' Unknown '+'[/I][/COLOR]\n'

          
          all_data_imdb.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
          return data_ep,dates,fanart,color,next
def get_Series_trk_data(url_o,match):
        import _strptime
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile_trk = os.path.join(user_dataDir, 'cache_play_trk.db')
        dbcon_trk2 = database.connect(cacheFile_trk)
        dbcur_trk2  = dbcon_trk2.cursor()
        dbcur_trk2.execute("CREATE TABLE IF NOT EXISTS %s ( ""data_ep TEXT, ""dates TEXT, ""fanart TEXT,""color TEXT,""id TEXT,""season TEXT,""episode TEXT, ""next TEXT,""plot TEXT);" % 'AllData4')
        dbcon_trk2.commit()
        dbcur_trk2.execute("DELETE FROM AllData4")

        image=' '
        for item in match:
          next=''
          name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
          #name,id,season,episode=item
          data_ep=''
          dates=' '
          fanart=image
          url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(id,season)
         
          html=requests.get(url).json()
          if 'status_message' in html:
            if html['status_message']!='The resource you requested could not be found.':
                xbmc.sleep(10000)
                html=requests.get(url).json()
            
          ep=0
          f_episode=0
          catch=0
          counter=0
          if 'episodes' in html:
              for items in html['episodes']:
                if 'air_date' in items:
                   try:
                       datea=items['air_date']+'\n'
                       
                       a=(time.strptime(items['air_date'], '%Y-%m-%d'))
                       b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
                      
                   
                       if a>b:
                         if catch==0:
                           f_episode=counter
                           
                           catch=1
                       counter=counter+1
                       
                   except:
                         ep=0
          else:
             ep=0
          episode_fixed=int(episode)-1
          try:
              try:
                plot=html['episodes'][int(episode_fixed)]['overview']
              except:
                logging.warning(name.decode('utf-8'))
                if 'episodes' not in html:
                    logging.warning(html)
                    
                
                logging.warning(episode_fixed)
                
                plot=''
                pass
              
          
              ep=len(html['episodes'])
              try:
                  if (html['episodes'][int(episode_fixed)]['still_path'])==None:
                    fanart=image
                  else:
                    fanart=domain_s+'image.tmdb.org/t/p/original/'+html['episodes'][int(episode_fixed)]['still_path']
              except:
                fanart=image
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'Season '+season+'-Episode '+episode+ '[/COLOR]\n[COLOR gold] out of ' +str(f_episode)  +" Season's Episodes  [/COLOR]\n" 
              try:
                  if int(episode)>1:
                    
                    prev_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)-1]['air_date'], '%Y-%m-%d'))) 
                  else:
                    prev_ep=0
              except:
                prev_ep=0

          

              try:
                  if int(episode)<ep:
                    
                    if (int(episode)+1)>=f_episode:
                      color_ep='magenta'
                      next_ep='[COLOR %s]'%color_ep+time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) +'[/COLOR]'
                    else:
                      
                      next_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
                  else:
                    next_ep=0
              except:
                next_ep=0
              try:
                  dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
              except:
                dates=' '
              if int(episode)<int(f_episode):
               color='gold'
              else:
               color='white'
               h2=requests.get('https://api.themoviedb.org/3/tv/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US'%id).json()
               last_s_to_air=int(h2['last_episode_to_air']['season_number'])
               last_e_to_air=int(h2['last_episode_to_air']['episode_number'])
              
               if int(season)<last_s_to_air:
        
                 color='lightblue'
               if h2['status']=='Ended' or h2['status']=='Canceled':
                color='peru'
                
               if h2['next_episode_to_air']!=None:
                 if 'air_date' in h2['next_episode_to_air']:
                    a=(time.strptime(h2['next_episode_to_air']['air_date'], '%Y-%m-%d'))
                    next=time.strftime( "%d-%m-%Y",a)
               else:
                  next=''
          
          except Exception as e:
              import linecache
              exc_type, exc_obj, tb = sys.exc_info()
              f = tb.tb_frame
              lineno = tb.tb_lineno
              filename = f.f_code.co_filename
              linecache.checkcache(filename)
              line = linecache.getline(filename, lineno, f.f_globals)
              
              logging.warning('ERROR IN Series Tracker:'+str(lineno))
              logging.warning('inline:'+line)
              logging.warning(e)
              logging.warning('BAD Series Tracker')
              plot=' '
              color='green'
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'Season '+season+'-Episode '+episode+ '[/COLOR]\n[COLOR gold] out of ' +str(f_episode)  +" Season's episodes [/COLOR]\n" 
              dates=' '
              fanart=image
          
          dbcon_trk2.execute("INSERT INTO AllData4 Values ('%s', '%s', '%s', '%s','%s', '%s', '%s','%s','%s');" % (data_ep.replace("'","%27"),json.dumps(dates),fanart.replace("'","%27"),color,id,season,episode,next,plot.replace("'","%27")))
        dbcon_trk2.commit()
        dbcon_trk2.close()
        logging.warning('TRD SUCE')
        return 0
def sync_trk(removedb=False,show_msg=True):
    #tv
    
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    
    all_tv_prog=progress_trakt('users/me/watched/shows?extended=full',sync=True)
    
    if removedb:
        dbcur.execute("DELETE FROM Lastepisode")
    else:
        dbcur.execute("SELECT  * FROM Lastepisode WHERE  type='tv' ")
   
    match_tv = dbcur.fetchall()
   
    
    new_tv={}
    all_local_mv={}
    new_tv_far={}
    for item in match_tv:
      
      
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
     
      all_local_mv[id]={}
      all_local_mv[id]['icon']=icon
      all_local_mv[id]['fan']=image
      all_local_mv[id]['plot']=plot
      all_local_mv[id]['year']=year
      all_local_mv[id]['original_title']=original_title
      all_local_mv[id]['title']=name
      all_local_mv[id]['season']=season
      all_local_mv[id]['episode']=episode
      all_local_mv[id]['eng_name']=eng_name
      all_local_mv[id]['heb_name']=heb_name
      
      all_local_mv[id]['type']='tv'
     
      if id not in all_tv_prog:
       
        new_tv[id]={}
        new_tv[id]['item']=(all_local_mv[id])
        
        new_tv[id]['change_reason']='New'
       
        new_tv[id]['local']=''
        new_tv[id]['trk']=''
      else:
        if season!=all_tv_prog[id]['season']:
            if id not in new_tv:
                new_tv[id]={}
                new_tv[id]['change_reason']=''
            new_tv[id]['item']=(all_tv_prog[id])
            new_tv[id]['change_reason']=new_tv[id]['change_reason']+'$$$$season'
            
            new_tv[id]['local']=season
            new_tv[id]['trk']=all_tv_prog[id]['season']
        if episode!=all_tv_prog[id]['episode']:
            if id not in new_tv:
                new_tv[id]={}
                new_tv[id]['change_reason']=''
            new_tv[id]['item']=(all_tv_prog[id])
            
            new_tv[id]['change_reason']=new_tv[id]['change_reason']+'$$$$episode'
            new_tv[id]['local']=episode
            new_tv[id]['trk']=all_tv_prog[id]['episode']
    for id in all_tv_prog:
      if id not in all_local_mv:
        new_tv_far[id]={}
        new_tv_far[id]['item']=(all_tv_prog[id])
        new_tv_far[id]['change_reason']='New'

        new_tv_far[id]['local']=''
        new_tv_far[id]['trk']=''
      else:
        if all_tv_prog[id]['season']!=all_local_mv[id]['season']:
            if id not in new_tv_far:
                new_tv_far[id]={}
                new_tv_far[id]['change_reason']=''
            new_tv_far[id]['item']=(all_local_mv[id])
            new_tv_far[id]['change_reason']=new_tv_far[id]['change_reason']+'$$$$season'
            
            new_tv_far[id]['local']=all_local_mv[id]['season']
            new_tv_far[id]['trk']=all_tv_prog[id]['season']
        if all_tv_prog[id]['episode']!=all_local_mv[id]['episode']:
            if id not in new_tv_far:
                new_tv_far[id]={}
                new_tv_far[id]['change_reason']=''
            new_tv_far[id]['item']=(all_local_mv[id])
            
            new_tv_far[id]['change_reason']=new_tv_far[id]['change_reason']+'$$$$episode'
            new_tv_far[id]['local']=all_local_mv[id]['episode']
            new_tv_far[id]['trk']=all_tv_prog[id]['episode']
    not_on_trk=[]
    not_on_local=[]
    for id in new_tv:
        if new_tv[id]['change_reason']=='New':
            not_on_trk.append(clean_name(all_local_mv[id]['original_title'],1)+' S%sE%s'%(all_local_mv[id]['season'],all_local_mv[id]['episode'])+'-'+all_local_mv[id]['year'])
    for id in new_tv_far:
        if new_tv_far[id]['change_reason']=='New':
            not_on_local.append(clean_name(all_tv_prog[id]['original_title'],1)+' S%sE%s'%(all_tv_prog[id]['season'],all_tv_prog[id]['episode'])+'-'+all_tv_prog[id]['year'])
    

            
            
    #movie
    all_mv_prog=get_trk_data('users/me/watched/movies')
    
    dbcur.execute("SELECT * FROM Lastepisode WHERE  type='movie'")
    match_tv = dbcur.fetchall()


    new_mv={}
    all_local_mv={}
    new_mv_far={}
    for item in match_tv:
      
      
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
     
      all_local_mv[id]={}
      all_local_mv[id]['icon']=icon
      all_local_mv[id]['fan']=image
      all_local_mv[id]['plot']=plot
      all_local_mv[id]['year']=year
      all_local_mv[id]['original_title']=original_title
      all_local_mv[id]['title']=name
      all_local_mv[id]['season']=season
      all_local_mv[id]['episode']=episode
      all_local_mv[id]['eng_name']=eng_name
      all_local_mv[id]['heb_name']=heb_name
      
      all_local_mv[id]['type']='tv'
      if id not in all_mv_prog:
        new_mv[id]={}
        new_mv[id]['item']=(all_local_mv[id])
        
        new_mv[id]['change_reason']='New'
       
        new_mv[id]['local']=''
        new_mv[id]['trk']=''
    for id in all_mv_prog:
      if id not in all_local_mv:
        new_mv_far[id]={}
        new_mv_far[id]['item']=(all_mv_prog[id])
        new_mv_far[id]['change_reason']='New'

        new_mv_far[id]['local']=''
        new_mv_far[id]['trk']=''
    not_on_trk_mv=[]
    not_on_local_mv=[]
    for id in new_mv:
        if new_mv[id]['change_reason']=='New':
            not_on_trk_mv.append(clean_name(all_local_mv[id]['original_title'],1)+'-'+all_local_mv[id]['year'])
    for id in new_mv_far:
        if new_mv_far[id]['change_reason']=='New':
            not_on_local_mv.append(clean_name(all_mv_prog[id]['original_title'],1)+'-'+all_mv_prog[id]['year'])
    msg='[COLOR yellow][I]Tv shows[/I][/COLOR]\n[COLOR lightblue]not found on TRAKT'+'\n----------------\n'+'\n'.join(not_on_trk)+'[/COLOR]\n\n[COLOR khaki]only on TRAKT not in local db'+'\n----------------\n'+'\n'.join(not_on_local)+'[/COLOR]'
    msg=msg+'\n\n[COLOR yellow][I]movies[/I][/COLOR]\n[COLOR lightblue]not found on TRAKT'+'\n----------------\n'+'\n'.join(not_on_trk_mv)+'[/COLOR]\n\n[COLOR khaki]only on TRAKT not in local db'+'\n----------------\n'+'\n'.join(not_on_local_mv)+'[/COLOR]'
    if removedb:
        ok=True
    else:
       ok=TrkBox_help('Changes', msg)
    if ok:
        start_time=time.time()
     
        dp = xbmcgui.DialogProgress()
        dp.create("Syncing", "Please wait", '')
         
        elapsed_time = time.time() - start_time
        dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Collecting', '')
        xxx=0
        for id in new_tv_far:
           if new_tv_far[id]['change_reason']=='New':
            name=new_tv_far[id]['item']['title']
            url='www'
            icon=new_tv_far[id]['item']['icon']
            image=new_tv_far[id]['item']['fan']
            plot=new_tv_far[id]['item']['plot']
            year=new_tv_far[id]['item']['year']
            original_title=new_tv_far[id]['item']['original_title']
            season=new_tv_far[id]['item']['season']
            episode=new_tv_far[id]['item']['episode']
            eng_name=new_tv_far[id]['item']['eng_name']
            show_original_year=new_tv_far[id]['item']['year']
            heb_name=new_tv_far[id]['item']['heb_name']
            isr='0'
            tv_movie='tv'
            dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'","%27"),url,icon,image,plot.replace("'","%27"),year,original_title.replace("'","%27").replace(" ","%20"),season,episode,id,eng_name.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),isr,tv_movie))
            dp.update(int(((xxx* 100.0)/(len(new_tv_far))) ), ' Movies '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Sync DB', name)
            xxx+=1
        dbcon.commit()
            
        xxx=0
        for id in new_mv_far:
           
           if new_mv_far[id]['change_reason']=='New':
            name=new_mv_far[id]['item']['title']
            url='www'
            icon=new_mv_far[id]['item']['icon']
            image=new_mv_far[id]['item']['fan']
            plot=new_mv_far[id]['item']['plot']
            year=new_mv_far[id]['item']['year']
            original_title=new_mv_far[id]['item']['original_title']
            season=new_mv_far[id]['item']['season']
            episode=new_mv_far[id]['item']['episode']
            eng_name=new_mv_far[id]['item']['eng_name']
            show_original_year=new_mv_far[id]['item']['year']
            heb_name=new_mv_far[id]['item']['heb_name']
            isr='0'
            tv_movie='movie'
            dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'","%27"),url,icon,image,plot.replace("'","%27"),year,original_title.replace("'","%27").replace(" ","%20"),season,episode,id,eng_name.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),isr,tv_movie))
            dp.update(int(((xxx* 100.0)/(len(new_mv_far))) ), ' Tv shows '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Sync DB', name)
            xxx+=1
        dbcon.commit()
        xxx=0
        for id in new_mv:
          if new_mv[id]['change_reason']=='New':
            i = (post_trakt('/sync/history',data= {"movies": [{"ids": {"tmdb": id}}]}))
            dp.update(int(((xxx* 100.0)/(len(new_mv))) ), ' Movies '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Sync Trakt', id)
            xxx+=1
        xxx=0
        for id in new_tv:
          if new_tv[id]['change_reason']=='New':
            
            season=new_tv[id]['item']['season']
            episode=new_tv[id]['item']['episode']
            season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
            i = (post_trakt('/sync/watchlist', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
            
            
            i = (post_trakt('/sync/history', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
           
            dp.update(int(((xxx* 100.0)/(len(new_tv))) ), ' Tv shows '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Sync Trakt', id)
            xxx+=1
        if show_msg:
            xbmc.executebuiltin('Container.Refresh')
            xbmcgui.Dialog().ok('Sync','[COLOR aqua][I] Sync Complete [/I][/COLOR]')
            
    dbcur.close()
    dbcon.close()
    try:
     dp.close()
    except:
        pass
def last_viewed(url_o,isr=' '):
    global all_data_imdb
    all_folders=[]

    global susb_data,susb_data_next
    import datetime
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile_trk = os.path.join(user_dataDir, 'cache_play_trk.db')
    dbcon_trk = database.connect(cacheFile_trk)
    dbcur_trk  = dbcon_trk.cursor()
    dbcur_trk.execute("CREATE TABLE IF NOT EXISTS %s ( ""data_ep TEXT, ""dates TEXT, ""fanart TEXT,""color TEXT,""id TEXT,""season TEXT,""episode TEXT, ""next TEXT,""plot TEXT);" % 'AllData4')
    
    dbcon_trk.commit()
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    dbcon.commit()
    
    
       
    
    strptime = datetime.datetime.strptime
    start_time=time.time()
    if Addon.getSetting("dp")=='true':
     
         dp = xbmcgui.DialogProgress()
         dp.create("Collecting", "Please wait", '')
         
         elapsed_time = time.time() - start_time
         dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Collecting', '')
         
    color='white'
    
    if url_o=='tv':
        dbcur.execute("SELECT  * FROM Lastepisode WHERE  type='tv' ")
    else:
       dbcur.execute("SELECT * FROM Lastepisode WHERE  type='movie'")
    match_tv = dbcur.fetchall()
    xxx=0
    all_data_imdb=[]
    thread=[]
    
    for item in match_tv:
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
      
      logging.warning('isr2:'+isr)
      dates=' '
      next=''
      data_ep=''
      fanart=image
      if Addon.getSetting("dp")=='true' :
        dp.update(int(((xxx* 100.0)/(len(match_tv))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Collection', clean_name(original_title,1))
      xxx+=1
      done_data=0
      if url_o=='tv' :
          try:
              dbcur_trk.execute("SELECT  * FROM AllData4 WHERE  id='%s' AND season='%s' AND episode='%s'"%(id,season,episode))
               
                  
              match2 = dbcur_trk.fetchone()

            
              if match2!=None:
                data_ep,dates,fanart,color,i,j,k,next,plot=match2
                dates=json.loads(dates)

                if color=='white' :
                    
                    thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
                    thread[len(thread)-1].setName(clean_name(original_title,1))
                    done_data=1
                    #data_ep,dates,fanart,color,next=get_one_trk(color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image)
              else:

                thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
                thread[len(thread)-1].setName(clean_name(original_title,1))
                done_data=1
                #data_ep,dates,fanart,color,next=get_one_trk(color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image)
          except:
            thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
            thread[len(thread)-1].setName(clean_name(original_title,1))
            done_data=1
            #data_ep,dates,fanart,color,next=get_one_trk(color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image)
     
      if done_data==0:
          try:
            f_name=urllib.unquote_plus(heb_name.encode('utf8'))
     
          except:
            f_name=name
          if (heb_name)=='':
            f_name=name
          if color=='peru':
            add_p='[COLOR peru][B]This show was over or canceled[/B][/COLOR]'+'\n'
          else:
            add_p=''
          add_n=''
          if color=='white' and url_o=='tv' :
              if next !='':
                add_n='[COLOR tomato][I]Next episode at ' +next+'[/I][/COLOR]\n'
              else:
                add_n='[COLOR tomato][I]Next episode at ' +' Unknown '+'[/I][/COLOR]\n'
          
          all_data_imdb.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
      
    
    for td in thread:
        td.start()

        if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
        if len(thread)>38:
            xbmc.sleep(255)
        else:
            xbmc.sleep(10)
    while 1:

          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              
              still_alive=1
              all_alive.append(thread[yy].name)
          if still_alive==0:
            break
          if Addon.getSetting("dp")=='true' :
                elapsed_time = time.time() - start_time
                dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive)," ")
          xbmc.sleep(100)
          if Addon.getSetting("dp")=='true' :
              if dp.iscanceled():
                dp.close()
              
                break
    
    thread=[]
    if url_o=='tv':
        all_subs_db=[]
        if 0:
            dbcur.execute("SELECT * FROM subs")
            match = dbcur.fetchall()
            
            for title,id,season,episode in match:
                if len(episode)==1:
                  episode_n="0"+episode
                else:
                   episode_n=episode
                if len(season)==1:
                  season_n="0"+season
                else:
                  season_n=season
                next_ep=str(int(episode_n)+1)
                if len(next_ep)==1:
                  next_ep_n="0"+next_ep
                else:
                  next_ep_n=next_ep
                sub_title=title.replace("%27","'")+'-'+id+'-'+season_n+'-'+episode_n
                all_subs_db.append(sub_title)
        for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx in all_data_imdb:
            if len(episode)==1:
              episode_n="0"+episode
            else:
               episode_n=episode
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
            next_ep=str(int(episode_n)+1)
            if len(next_ep)==1:
              next_ep_n="0"+next_ep
            else:
              next_ep_n=next_ep
            sub_title=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+episode_n
            sub_title_next=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+next_ep_n
            #if (color=='gold' or color=='white')  :
           
                #if sub_title not in all_subs_db:
                #    thread.append(Thread(check_last_tv_subs,original_title,heb_name,season,episode,show_original_year,id))
                #    thread[len(thread)-1].setName(eng_name+' '+episode)
                #if color=='gold' and sub_title_next not in all_subs_db:
                #    thread.append(Thread(check_next_last_tv_subs,original_title,heb_name,season,str(int(episode)+1),show_original_year,id))
                #    thread[len(thread)-1].setName(eng_name+' '+str(int(episode)+1))
           
            
    susb_data={}
    susb_data_next={}
    if url_o=='tv' :
        for td in thread:
            td.start()

            if Addon.getSetting("dp")=='true' :
                    elapsed_time = time.time() - start_time
                    dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
        while 1:

              still_alive=0
              all_alive=[]
              for yy in range(0,len(thread)):
                
                if  thread[yy].is_alive():
                  
                  still_alive=1
                  all_alive.append(thread[yy].name)
              if still_alive==0:
                break
              
              xbmc.sleep(100)
              if Addon.getSetting("dp")=='true' :
                  if dp.iscanceled():
                    dp.close()
                  
                    break
    all_data_imdb=sorted(all_data_imdb, key=lambda x: x[19], reverse=False)
    all_o_data=[]
    level=0
    for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx in all_data_imdb:
        if url_o=='tv':
            if color=='gold':
                level=1
            elif color=='lightblue':
                level=2
            elif color=='green':
                level=3
            elif color=='white':
                level=4
            elif color=='peru':
                level=5
        else:
            level+=1
        all_o_data.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,level))
    if url_o=='tv':
        order=False
    else:
        order=True
    #if Addon.getSetting("order_latest")=='true':
    all_o_data=sorted(all_o_data, key=lambda x: x[20], reverse=order)
    for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,pos in all_o_data:
       
        if len(episode)==1:
          episode_n="0"+episode
        else:
           episode_n=episode
        if len(season)==1:
          season_n="0"+season
        else:
          season_n=season
        

        all_d=((dates))
        if color!='white' and len(all_d)>1:
          
            
            
            
            add_n='[COLOR aqua]'+' Aired at '+all_d[1] + '[/COLOR]\n'
            
        plot=plot.replace('%27',"'")
        if url_o=='tv':
            mode=146
        else:
            mode=15
        dd=[]
        dd.append((f_name,show_original_year,original_title,id,season,episode,show_original_year))
        aa=addNolink('[COLOR %s]'%color+ f_name+'[/COLOR]', url,mode,False, iconimage=icon,fanart=fanart,plot=add_p+data_ep+add_n+plot,original_title=original_title,id=id,season=season,episode=episode,eng_name=eng_name,show_original_year=show_original_year,dates=json.dumps(dates),dd=json.dumps(dd),dont_place=True)
        all_folders.append(aa)
    dbcur_trk.close()
    dbcon_trk.close()
    
    dbcur.close()
    dbcon.close()
    read_data2=[]
    
    if len(all_folders)>0:
        if Addon.getSetting("trakt_access_token")!='':
            aa=addNolink( '[COLOR blue][I]---sync trakt---[/I][/COLOR]', id,157,False,fanart='https://bestdroidplayer.com/wp-content/uploads/2019/06/trakt-what-is-how-use-on-kodi.png', iconimage=BASE_LOGO+'trakt.png',plot=' ',dont_place=True)
            all_folders.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_folders,len(all_folders))
    if url_o=='tv' :
        read_data2.append((url_o,match_tv))
    

    if Addon.getSetting("dp")=='true' :
        dp.close()
    return read_data2
def history_old(url):
    o_url=url
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    
    
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    
    dbcur.execute("SELECT * FROM Lastepisode WHERE type='%s'"%url)

    match = dbcur.fetchall()
    dbcon.commit()
    
    dbcur.close()
    dbcon.close()
    all_d=[]
    for name,url,icon,fan,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,type in match:
        if o_url=='tv':
            if len(episode)==1:
              episode_n="0"+episode
            else:
               episode_n=episode
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
            added='- S%sE%s'%(season_n,episode_n)
        else:
            added=''
        aa=addDir3( name+added, 'history',15, icon,fan,plot,data=year,original_title=original_title,id=id,season=season,episode=episode,eng_name=eng_name,show_original_year=year,heb_name=original_title)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def s_tracker(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,dates):
    menu=[]

    menu = Chose_ep('plugin.video.shadow', original_title,name,id,season,episode,dates,original_title)
    menu.doModal()
    ret = menu.params

    del menu
    logging.warning('ret:'+str(ret))
    if ret!=-1:
        all_d=json.loads(urllib.unquote_plus(dates))
        logging.warning('all_d:'+str(all_d))
        if all_d[2]==0 or all_d[0]==0:
          prev_index=1
        else:
          prev_index=2
        logging.warning('prev_index:'+str(prev_index))
        if ret==0 and all_d[2]!=0:
          episode=str(int(episode)+1)
          from resources.modules.tmdb import get_episode_data
          name,plot,image,season,episode=get_episode_data(id,season,episode)
          o_plot='Season %s Episode %s \n'%(season,episode)+plot
        elif ret==prev_index:
          
          if int(episode)>1:
            episode=str(int(episode)-1)
            from resources.modules.tmdb import get_episode_data
            name,plot,image,season,episode=get_episode_data(id,season,episode)
            o_plot='Season %s Episode %s \n'%(season,episode)+plot
        elif ret==(prev_index+1):
            
            
            xbmc.executebuiltin(('Container.update("plugin://plugin.video.shadow/?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode=19",return)'%(name,urllib.quote_plus(url),iconimage,fanart,urllib.quote_plus(description),show_original_year,original_title,id,season,id,show_original_year,original_title,'0')))
            
            return 'ok',[] 
          
        elif ret==(prev_index+2):
            
            xbmc.executebuiltin(('Container.update("plugin://plugin.video.shadow/?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode=16"),return'%(name,urllib.quote_plus(url),iconimage,fanart,urllib.quote_plus(description),show_original_year,original_title,id,season,id,show_original_year,original_title,'0')))
            
            return 'ok',[]
        xbmc.executebuiltin(('XBMC.RunPlugin("plugin://plugin.video.shadow/?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&episode=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode=15",return)'%(name,urllib.quote_plus(url),iconimage,fanart,urllib.quote_plus(description),show_original_year,original_title,id,season,episode,id,show_original_year,original_title,'0')))
def clear_trakt():
    from resources.modules.general import reset_trakt
    reset_trakt()
def clear_search(url):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    if url=='both':
        dbcur.execute("DELETE FROM search_string2 ;" )
        
    else:
      dbcur.execute("DELETE FROM search_string2 where tv_movie='%s';" % url)
   
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('History', 'Cleared')))
    xbmc.executebuiltin('Container.Refresh')
def get_html_data(url):
    html=requests.get(url).json()
    return html
def was_i():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    addNolink('[COLOR red][I][B]Clear history[/B][/I][/COLOR]','www',162,False,iconimage='https://keepingitclean.ca/images/social/keep-it-clean-social-sharing.jpg',fanart='https://the-clean-show.us.messefrankfurt.com/content/dam/messefrankfurt-usa/the-clean-show/2021/images/kv/Cleanshow%20websideheader_tropfen_2560x1440px_01.jpg')
    dbcur.execute("SELECT * FROM playback")
    dbcon.commit()
    match = dbcur.fetchall()
    if Addon.getSetting("dp")=='true':
        dp = xbmcgui . DialogProgress ( )
        dp.create('Please wait','Collecting', '','')
        dp.update(0, 'Please wait','Collecting', '' )
    zzz=0
    tmdbKey='653bb8af90162bd98fc7ee32bcbbfb3d'
    all_d=[]
    for name,tmdb,season,episode,playtime,totaltime,free in match:
      
      if float(totaltime)==0:
        continue
      if (int((float(playtime)*100)/float(totaltime)))<95:
        try:
        
            a=int(tmdb)
            
        except:
            if 'tt' in free:
             url=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=%s'%(free,lang)
             html_im=requests.get(url).json()
             logging.warning(free)
             logging.warning(html_im)
             
             if season=='0':
                 if len(html_im['movie_results'])>0:
                    tmdb=str(html_im['movie_results'][0]['id'])
             else:
                if len(html_im['tv_results'])>0:
                    tmdb=str(html_im['tv_results'][0]['id'])
             try:
        
                a=int(tmdb)
                
             except:
                continue
            else:
                continue
        
        if season!='0' and season!='' and season!='%20':
          url_t='http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=%s&append_to_response=external_ids'%(tmdb,season,episode,lang)
          html_t=cache.get(get_html_data,9999,url_t, table='posters')
          if 'status_code' in html_t:
            continue
          if 'still_path' in html_t:
            if html_t['still_path']==None:
                html_t['still_path']=''
          else:
            html_t['still_path']=''
          fan=domain_s+'image.tmdb.org/t/p/original/'+html_t['still_path']
          
          plot= '[COLOR yellow] %s '%str(int((float(playtime)*100)/float(totaltime)))+'%[/COLOR]\n'+html_t['overview']
          url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=external_ids'%(tmdb,tmdbKey,lang)
          html=cache.get(get_html_data,9999,url2, table='posters')
          if 'poster_path' in html:
              if html['poster_path']==None:
                html['poster_path']=''
          else:
            html['poster_path']=''
          icon=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
          new_name=html['name']+ ' S%sE%s '%(season,episode)
          url='www'
          if 'air_date' in html_t:
           if html_t['air_date']!=None:
             
             year=str(html_t['air_date'].split("-")[0])
           else:
            year='0'
          else:
            year='0'
          if 'first_air_date' in html:
           if html['first_air_date']!=None:
             
             data=str(html['first_air_date'].split("-")[0])
           else:
            data='0'
          else:
            data='0'
          original_name=html['original_name']
          rating=html['vote_average']
          heb_name=html['name']
          isr='0'
          genres_list=[]
          if 'genres' in html:
            for g in html['genres']:
                  genres_list.append(g['name'])
            
            try:genere = u' / '.join(genres_list)
            except:genere=''
          trailer = "plugin://plugin.video.shadow?mode=25&url=www&id=%s&tv_movie=%s" % (tmdb,'tv')
          
          all_d.append(addDir3(new_name,url,15,icon,fan,plot,data=year,original_title=original_name,id=tmdb,rating=rating,heb_name=heb_name,show_original_year=data,isr=isr,generes=genere,trailer=trailer,season=season,episode=episode,hist='true'))
        
        else:
          url_t='http://api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s'%(tmdb,lang)
          
          
          logging.warning(url_t)
          html=cache.get(get_html_data,9999,url_t, table='poster')
          if 'status_code' in html:
            continue
          if 'backdrop_path' in html:
              if html['backdrop_path']==None:
                html['backdrop_path']=''
          else:
            html['backdrop_path']=''
          fan=domain_s+'image.tmdb.org/t/p/original/'+html['backdrop_path']
          
          plot= '[COLOR yellow] %s '%str(int((float(playtime)*100)/float(totaltime)))+'%[/COLOR]\n'+html['overview']
          if 'poster_path' in html:
              if html['poster_path']==None:
                html['poster_path']=''
          else:
            html['poster_path']=''
          icon=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
          new_name=html['title']
          url='www'
          if 'release_date' in html:
           if html['release_date']!=None:
             
             year=str(html['release_date'].split("-")[0])
           else:
            year='0'
          else:
            year='0'
          original_title=html['original_title']
          rating=html['vote_average']
          heb_name=html['title']
          isr='0'
          genres_list=[]
          if 'genres' in html:
            for g in html['genres']:
                  genres_list.append(g['name'])
            
            try:genere = u' / '.join(genres_list)
            except:genere=''
          trailer = "plugin://plugin.video.shadow?mode=25&url=www&id=%s&tv_movie=%s" % (tmdb,'tv')
          all_d.append(addDir3(new_name,url,15,icon,fan,plot,episode=' ',season=' ',data=year,original_title=original_title,id=tmdb,rating=rating,heb_name=heb_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,hist='true'))
        if Addon.getSetting("dp")=='true':
            dp.update(int(((zzz* 100.0)/(len(match))) ), 'Please wait','Loading', new_name )
            zzz+=1
            if dp.iscanceled():
               dp.close()
               break
    if Addon.getSetting("dp")=='true':
        dp.close()
    dbcur.close()
    dbcon.close()
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def remove_was_i(name,id,season,episode):
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE  FROM playback   where tmdb='%s' and season='%s' and episode='%s'"%(id,str(season).replace('%20','0').replace(' ','0'),str(episode).replace('%20','0').replace(' ','0')))
        logging.warning(' Remove DATA')
        logging.warning("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(id,str(season).replace('%20','0').replace(' ','0'),str(episode).replace('%20','0').replace(' ','0')))
        dbcon.commit()
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Shadow', 'Removed...'.decode('utf8')+name)).encode('utf-8'))
        xbmc.executebuiltin('Container.Refresh')
        dbcur.close()
        dbcon.close()

def clear_was_i():
    ok=xbmcgui.Dialog().yesno(("Clear Resume points"),('Are you sure there is no way back...?'))
    if ok:
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM playback")
        dbcon.commit()
        dbcur.close()
        dbcon.close()

        xbmc.executebuiltin('Container.Refresh')
def remove_from_trace(name,original_title,id,season,episode):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    #dbcur.execute("select id from Lastepisode WHERE original_title = '%s'"%(original_title))

    #dbcon.commit()
    #id_new = dbcur.fetchone()[0]
    logging.warning('Remove trace')
    if id=='0':
      ok=xbmcgui.Dialog().yesno(("Remove from series tracker"),('Are you sure you want to remove '+name+" from series tracker?"))
    else:
      ok=xbmcgui.Dialog().yesno(("Mark as unwatched"),('Unwatched '+name+" ?"))
    if ok:
      if id=='0':
        
        dbcur.execute("DELETE  FROM Lastepisode WHERE original_title = '%s' or original_title = '%s'"%(original_title.replace(' ','%20').replace("'","%27"),original_title.replace('%20',' ').replace("'","%27")))
        
        dbcon.commit()
      else:
      
        if len(episode)==0:
          episode='%20'
        if len(season)==0:
          season='%20'
        episode=episode.replace(" ","%20")
        season=season.replace(" ","%20")
        dbcur.execute("DELETE  FROM  AllData WHERE original_title = '%s'  AND season='%s' AND episode = '%s'"%(original_title,season.replace(" ","%20"),episode.replace(" ","%20")))
       
        
        dbcon.commit()
      dbcur.close()
      dbcon.close()
      
      xbmc.executebuiltin('Container.Refresh')
      
def trakt_world():
    all=[]
    aa=addNolink( '[COLOR blue][I]---Movies---[/I][/COLOR]', id,27,False,fanart=' ', iconimage=' ',plot=' ',dont_place=True)
    all.append(aa)
    
    
    
    aa=addDir3('People Watching [Movies]','movies/trending?limit=40&page=1',117,BASE_LOGO+'people.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
    all.append(aa)
    
    aa=addDir3('popular [Movies]','movies/popular?limit=40&page=1$$$noaut',166,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
    all.append(aa)
    aa=addDir3('Most played [Movies]','movies/played/%s?limit=40&page=1',117,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
    all.append(aa)
    
    aa=addDir3('Most Watched [Movies]','movies/watched/%s?limit=40&page=1',117,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
    all.append(aa)
    
    aa=addDir3('Most Collected [Movies]','movies/collected/%s?limit=40&page=1',117,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
    all.append(aa)
    
    aa=addDir3('Most anticipated [Movies]','movies/anticipated?limit=40&page=1$$$noaut',117,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
    all.append(aa)
    
    aa=addDir3('Most Grossing Weekly [Movies]','movies/boxoffice?limit=40&page=1$$$noaut',117,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
    all.append(aa)
    
    aa=addNolink( '[COLOR blue][I]---TV---[/I][/COLOR]', id,27,False,fanart=' ', iconimage=' ',plot=' ',dont_place=True)
    all.append(aa)
    aa=addDir3('People Watching [TV]','shows/trending?limit=40&page=1$$$noaut',117,BASE_LOGO+'people.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Tv')
    all.append(aa)
    
    aa=addDir3('popular [TV]','shows/popular?limit=40&page=1$$$noaut',166,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Tv')
    all.append(aa)
    
    aa=addDir3('Most played [TV]','shows/played/%s?limit=40&page=1',117,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Tv')
    all.append(aa)
    
    aa=addDir3('Most collected [TV]','shows/collected/%s?limit=40&page=1',117,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Tv')
    all.append(aa)
    
    aa=addDir3('Most anticipated [TV]','shows/anticipated?limit=40&page=1$$$noaut',117,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Tv')
    all.append(aa)
    
    aa=addNolink( '[COLOR blue][I]---Lists---[/I][/COLOR]', id,27,False,fanart=' ', iconimage=' ',plot=' ',dont_place=True)
    all.append(aa)
    aa=addDir3('Trending Lists [TV]','lists/trending',119,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Tv')
    all.append(aa)
    
    aa=addDir3('Popular lists [TV]','lists/popular',119,BASE_LOGO+'trakt.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Tv')
    all.append(aa)
    
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))

        
def set_view_type(pre_mode):
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    preserve_viewid = window.getFocusId()
    view_type=xbmc.getInfoLabel('Container.Viewmode' )
    listlabel = xbmc.getInfoLabel("ListItem.Tag")
    
    view_mode_id='List'
    #xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    all_types=['Shadow default','files', 'movies', 'tvshows', 'episodes']
    ret = xbmcgui.Dialog().select("Choose Type", all_types)
    if ret!=-1:
        selected_view=all_types[ret]
    else:
        selected_view='Defualt'

    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s (""mode TEXT,""name TEXT, ""id TEXT, ""type TEXT, ""free TEXT,""free2 TEXT);"%'views')
    
    dbcur.execute("SELECT * FROM views ")

    match = dbcur.fetchall()
    dbcon.commit()
    all_modes=[]
    for mode,name,id,type,free1,free2 in match:
        all_modes.append(mode)
    
    if pre_mode in all_modes:
        dbcur.execute("UPDATE views SET name='%s',id='%s',type='%s' WHERE mode = '%s'"%(view_type,str(preserve_viewid),selected_view,str(pre_mode)))
    else:
        dbcur.execute("INSERT INTO views Values ('%s','%s','%s','%s','%s','%s')"%(str(pre_mode),view_type,str(preserve_viewid),selected_view,' ',' '))
    dbcon.commit()
    logging.warning('Updated to '+(view_type)+', '+selected_view)
    a= str('Updated to '+(view_type)+', '+selected_view)
    xbmcgui.Dialog().ok('Ok',a)
   
    dbcur.close()
    dbcon.close()
def rd_history_torrents():
    rd = real_debrid.RealDebrid()
    items=rd.list_torrents()
    
    items = [i for i in items if i['status'] == 'downloaded']
    logging.warning(json.dumps(items))
    addNolink( '[COLOR blue][I]---Won\'t sync with trakt!---[/I][/COLOR]', id,27,False,fanart=' ', iconimage=' ',plot=' ')
    
    all=[]
    all_links=[]
    for i in items:
        i['name'] = i['filename']
       
          
          
        aa=addLink(i['name'], 'Direct$$$$'+i['id'],170,False,BASE_LOGO+'rd.png','https://sfilev2.f-static.com/image/users/350976/ftp/my_files/sop-resize-800-36aa0a0160a3eeaaa92d076e1f914735.jpg?sopC=1494244549658','Rd',place_control=True)
        
        all.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
def rd_history(url):
    o_url=url
    rd = real_debrid.RealDebrid()
    all_hist=rd.get_history(url)
   
    all=[]
    all_data={}
    all_full_data={}
    addNolink( '[COLOR blue][I]---Won\'t sync with trakt!---[/I][/COLOR]', id,27,False,fanart=' ', iconimage=' ',plot=' ')
    
    for items in all_hist:
        if 'video' in items['mimeType']:
            from resources.modules import PTN
        
            info=(PTN.parse(items['filename']))
            show_original_year='0'
            season='%20'
            episode='%20'
            if 'title' in info:
                original_title=info['title']
            else:
                original_title=items['filename']
            if 'year' in info:
                show_original_year=info['year']
            if 'season' in info:
                season=str(info['season'])
            if 'episode' in info:
                episode=str(info['episode'])
            if season!='%20' and episode!='%20':
                if len(episode)==1:
                  episode_n="0"+episode
                else:
                   episode_n=episode
                if len(season)==1:
                  season_n="0"+season
                else:
                  season_n=season
                nm=original_title+' - S%sE%s'%(season_n,episode_n)
            else:
                nm=original_title
            if nm.lower() not in all_data:
                all_data[nm.lower()]=[]
                all_full_data[nm.lower()]=[]
            if items['download'] not in all_data[nm.lower()]:
               all_data[nm.lower()].append(items['download'])
               all_full_data[nm.lower()].append((show_original_year,items['filename'],season,episode))
    
    for items in all_full_data:
      if len(items)>2:
        nm=items
        season=items[2]
        episode=items[3]
        show_original_year=items[0]
        name=items[1]
        aa=addLink(nm, json.dumps(all_data[items]),170,False,' ',' ',' ',data=show_original_year,original_title=name,season=season,episode=episode,tmdb=' ',year=show_original_year,place_control=True)
        all.append(aa)
        
    aa=addDir3('[COLOR aqua][I]Next page[/I][/COLOR]',str(int(o_url)+1),168,BASE_LOGO+'rd.png','https://sfilev2.f-static.com/image/users/350976/ftp/my_files/sop-resize-800-36aa0a0160a3eeaaa92d076e1f914735.jpg?sopC=1494244549658','Rd')
    all.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
data=None
original_title=None
read_data2=''
id='0'
dates=' '
season='0'
episode='0'
show_original_year='0'
nextup='true'
dd=''
video_data={}
get_sources_nextup='false'
all_w={}
use_filter='true'
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
try:        
        data=(params["data"])
except:
        pass
try:        
        original_title=urllib.unquote_plus(params["original_title"])
except:
        pass
        
try:        
        id=(params["id"])
except:
        pass
try:        
        season=(params["season"])
except:
        pass
try:        
        episode=(params["episode"])
except:
        pass
try:        
        show_original_year=(params["show_original_year"])
except:
        pass
try:        
        dd=(params["dd"])
except:
        pass
try:        
        nextup=(params["nextup"])
except:
        pass
try:        
        dates=(params["dates"])
except:
        pass
try:        
        video_data=urllib.unquote_plus(params["video_data"])
except:
        pass
try:        
        get_sources_nextup=(params["get_sources_nextup"])
except:
        pass
        
try:        
        all_w=urllib.unquote_plus(params["all_w"])
except:
        pass
        
try:        
        use_filter=(params["use_filter"])
except:
        pass
        
logging.warning('mode:'+str(mode))
logging.warning(id)
logging.warning(all_w)
logging.warning(url)
from resources.modules import public
public.pre_mode=mode

if mode==None or url==None or len(url)<1:
        main_menu()
elif mode==2:
    movie_world()
elif mode==3:
    tv_show_menu()
elif mode==5:
    from resources.modules.tmdb import get_movies
    search_entered=''
    keyboard = xbmc.Keyboard(search_entered, 'Enter Search')
    keyboard.doModal()
    if keyboard.isConfirmed() :
           search_entered = urllib.quote_plus(keyboard.getText())
           if search_entered=='':
            sys.exit()
    addNolink( '[COLOR blue][I]---Movies---[/I][/COLOR]', id,27,False,fanart=' ', iconimage=' ',plot=' ')
    get_movies('http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query={0}&language={1}&append_to_response=origin_country&page=1'.format(search_entered,lang),global_s=True)
    
    addNolink( '[COLOR blue][I]---TV---[/I][/COLOR]', id,27,False,fanart=' ', iconimage=' ',plot=' ')
    get_movies('http://api.themoviedb.org/3/search/tv?api_key=34142515d9d23817496eeb4ff1d223d0&query={0}&language={1}&page=1'.format(search_entered,lang),global_s=True)
elif mode==6:
    
    play_link(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,dd,nextup=nextup,video_data_exp=video_data,get_sources_nextup=get_sources_nextup,all_w=all_w)
elif mode==14:
    from resources.modules.tmdb import get_movies
    get_movies(url)
elif mode==15:
    #logging.warning(name)
    #logging.warning(original_title)
    #sys.exit()
    logging.warning('Get Sources')
    get_sources(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,video_data_exp=video_data,all_w=all_w,use_filter=use_filter)
elif mode==16:
    if 'tvdb' in id :
        url2=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=tvdb_id&language=%s'%(id.replace('tvdb',''),lang)
        pre_id=requests.get(url2).json()['tv_results']
        
        if len(pre_id)>0:
            id=str(pre_id[0]['id'])
    elif 'imdb' in id:
        url2=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=%s'%(id.replace('imdb',''),lang)
       
        pre_id=requests.get(url2).json()['tv_results']
        
        if len(pre_id)>0:
            id=str(pre_id[0]['id'])
    from resources.modules.tmdb import get_seasons
    
    get_seasons(name,url,iconimage,fanart,description,data,original_title,id)
elif mode==18:
    get_genere(url)
elif mode==19:
    from resources.modules.tmdb import get_episode
    get_episode(name,url,iconimage,fanart,description,data,original_title,id,season,id,show_original_year)
elif mode==20:
    get_tv_maze(url,iconimage)
elif mode==21:
    trakt_world()
elif mode==25:
    play_trailer(id,url)
elif mode==34:
    remove_from_trace(name,original_title,id,season,episode)
elif mode==35:
    
    ClearCache()
elif mode==65:
    add_remove_trakt(name,original_title,id,season,episode)
elif mode==101:
    tv_neworks()
elif mode==112:
    movie_prodiction()

elif mode==114:
    main_trakt()
elif mode==115:
    progress_trakt(url)
elif mode==116:
    get_trakt(url)
elif mode==117:
     get_trk_data(url)
elif mode==118:
    trakt_liked(url,iconimage,fanart)
elif mode==119:
    from resources.modules.trakt import get_simple_trakt
    get_simple_trakt(url)
elif mode==137:
    clear_rd()
elif mode==138:
    re_enable_rd()
elif mode==139:
    clear_pr()
elif mode==140:
    re_enable_pr()
elif mode==141:
    clear_all_d()
elif mode==142:
    re_enable_all_d()
elif mode==143:
    search_history(url,iconimage,fanart)
elif mode==144:
   last_played()
elif mode==145:
   read_data2=last_viewed(url)
elif mode==146:
    s_tracker(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,dates)
elif mode==147:
    clear_trakt()
elif mode==148:
    clear_search(url)
elif mode==149:
    show_updates(force=True)
elif mode==150:
    from resources.modules.trakt import manager
   
    manager(name, url, data)
elif mode==151:
    Addon.openSettings()
elif mode==157:
    ok=xbmcgui.Dialog().yesno(("Override"),('Override local DB? (override Shadow progress)'))
    remove_db=False
    show_msg=True
    if ok:
        remove_db=True
        show_msg=False
    sync_trk(removedb=False,show_msg=show_msg)
    if remove_db:
        show_msg=True
        sync_trk(removedb=True,show_msg=show_msg)
       
elif mode==158:
    was_i()
elif mode==159:
    remove_was_i(name,id,season,episode)
elif mode==160:
    from resources.modules.trakt import remove_trk_resume
    remove_trk_resume(name,id,season,episode,data)
elif mode==162:
    clear_was_i()
elif mode==163:
    from resources.modules import logupload
    logupload.start()
elif mode==164:
    from resources.modules.trakt import resume_episode_list
    resume_episode_list(url)
elif mode==166:
    from resources.modules.trakt import get_simple_trk_data
    get_simple_trk_data(url)
elif mode==167:
    set_view_type(str(url))
elif mode==168:
    rd_history(url)
elif mode==169:
    rd_history_torrents()
elif mode==170:
    simple_play(name,url)
match=[]
if Addon.getSetting("display_lock")=='true':
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s (""mode TEXT,""name TEXT, ""id TEXT, ""type TEXT, ""free TEXT,""free2 TEXT);"%'views')

    dbcur.execute("SELECT * FROM views where mode='%s'"%(str(mode)))


            
    match = dbcur.fetchall()
    
    dbcur.close()
    dbcon.close()
all_modes=[]
type='Defualt'
for mode,name,id,type,free1,free2 in match:
        all_modes.append(mode)
if type!='Defualt':
    xbmcplugin.setContent(int(sys.argv[1]), type)
else:
    if mode==2 or mode==3 or mode==114 or mode==112 or mode==101:
        xbmcplugin.setContent(int(sys.argv[1]), 'files')
    elif mode==16 :
       xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
    elif mode==19 or mode==20:
       xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    else:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')

if len(all_modes)>0:
    logging.warning('Container.SetViewMode(%d)' % int(id))
    xbmc.executebuiltin('Container.SetViewMode(%d)' % int(id))
xbmcplugin.endOfDirectory(int(sys.argv[1]))
if len(read_data2)>0:
    url_o,match=read_data2[0]
    thread=[]
    thread.append(Thread(get_Series_trk_data,url_o,match))
    import datetime
    strptime = datetime.datetime.strptime
    thread[0].start()
logging.warning('Done')
