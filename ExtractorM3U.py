'''
Created on Jan 23, 2015

@author: serenity
'''

import os, time
from stat import *
from MusicSync.Database import DataBase
from MusicSync import Transfer

class ExtractorM3U:
    
    def __init__(self):
        self.playlists = []
    
    def initialSetup(self,database,transfer, systemLocation):
        self.db = database
        self.transfer = transfer
        self.systemLocation = systemLocation
                
    def getListOfPlaylist(self):
        dirFiles = os.listdir(self.systemLocation)
        for dirFile in dirFiles:
            if(dirFile.endswith(".m3u")):
                self.playlists.append(dirFile)
                
    def printListOfPlaylist(self):
        for playlist in self.playlists:
            print playlist
            
    def parsePlaylist(self, playlistNumber, playlist):
        playlistFileLocation = self.systemLocation + "\\" + playlist
        m3uFile = open(playlistFileLocation, "r")
        m3uFileContent = m3uFile.read()
        # print m3uFileContent
        songBundle = m3uFileContent.split("#EXTINF:")
        # putContentinDB(playlist,)
        
        for song in songBundle[1:]:
            
            songDetails = (song.split("\n")[0])
            songDuration = songDetails.split(",")[0]
            songName = songDetails.split(",")[1]
            songLocation = song.split("\n")[1]
            songLocation = os.path.normpath(songLocation)
            songLocation = songLocation.replace('\\', '\\\\')
            print "EXTRACTED LOCATION : "+songLocation
            print "EXTRACTED SONG NAME : "+songName
            
            
            #songName=songName.encode('string-escape').replace("'", "\\'")
            self.db.putSongInDB(songLocation, songName, songDuration, playlistNumber)
            
        self.transfer.generatePlaylist(playlistFileLocation,playlist)
        m3uFile.close()
                
    def playlistEngine(self):
        
        self.getListOfPlaylist()
        self.printListOfPlaylist()
        for playlist in self.playlists:
            stat = os.stat(self.systemLocation + "\\" + playlist)
            # print "file modified:", time.asctime(time.localtime(stat[ST_TIME]))
            
            modifiedTime = time.asctime(time.localtime(stat[ST_MTIME]))
                                        
            indicator = self.db.checkIfPlaylistExists(self.db, playlist, modifiedTime)
            
            if(indicator == 0):
                self.createPlaylist( playlist, modifiedTime)
                print indicator
            if(indicator > 0):
                self.updatePlaylist( indicator, playlist)
                print indicator
            
            if(indicator == -1):
                self.verifyPlaylist()
                
            # self.parsePlaylist(playlist) 
            
    def verifyPlaylist(self):
        print "verify playlist"     
            
    def createPlaylist(self, playlist, modifiedTime):
        
        playlistNumber = self.db.createNewPlaylist(playlist, modifiedTime)
        self.parsePlaylist(playlistNumber, playlist)
        
        
    def updatePlaylist(self, playlistNumber, playlist):
        self.parsePlaylist(playlistNumber, playlist)
        
    
