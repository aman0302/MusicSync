'''
Created on Jan 23, 2015

@author: serenity
'''

import os, time
from stat import *
from MusicSync.Database import DataBase

class ExtractorM3U:
    
    def __init__(self):
        self.playlists=[]
        self.db=DataBase()
                
    def getListOfPlaylist(self,location):
        self.location=location
        #contents=[]
        dirFiles = os.listdir(location)
        for dirFile in dirFiles:
            if(dirFile.endswith(".m3u")):
                self.playlists.append(dirFile)
                
    def printListOfPlaylist(self):
        for playlist in self.playlists:
            print playlist
            
    def parsePlaylist(self,playlist):
        
        m3uFile = open(self.location+"\\"+playlist,"r")
        m3uFileContent = m3uFile.read()
        #print m3uFileContent
        songBundle = m3uFileContent.split("#EXTINF:")
        #putContentinDB(playlist,)
        
        for song in songBundle[1:]:
            
            songDetails =(song.split("\n")[0])
            songDuration = songDetails.split(",")[0]
            songName = songDetails.split(",")[1]
            songLocation = song.split("\n")[1]
            print songLocation
            print songName
            #putSongInDB(songLocation,SongName,Duration,playlist)
            
        m3uFile.close()
                
    def playlistEngine(self,cursor,location):
        
        self.getListOfPlaylist(location)
        
        for playlist in self.playlists:
            stat = os.stat(self.location+"\\"+playlist)
            print "file modified:", time.asctime(time.localtime(stat[ST_MTIME]))
            print "file modified:", time.asctime(time.localtime(stat[ST_ATIME]))
            print "file modified:", time.asctime(time.localtime(stat[ST_CTIME]))
            
            modifiedTime = time.asctime(time.localtime(stat[ST_MTIME]))
                                        
            indicator = self.db.checkPlaylist(playlist,modifiedTime)
            
            if(indicator==0):
                self.createPlaylist(playlist,modifiedTime)
                print 0
            if(indicator>0):
                self.updatePlaylist(indicator)
                print 1
                
            #self.parsePlaylist(playlist) 
            
            
    def createPlaylist(self,playlist,modifiedTime):
        
        playlistNumber = self.db.createPlaylist(playlist,modifiedTime)
        self.parsePlaylist(playlistNumber,playlist)
        
        
    def updatePlaylist(self):
        print 1 
        
    