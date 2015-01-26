'''
Created on Jan 24, 2015

@author: serenity
'''

import os,shutil

class Transfer:
    
    def initialSetup(self,dropboxPath, database):
        self.dropboxPath = dropboxPath
        self.database = database
        
    
    def validateSystemPresence(self):
        sql = "SELECT SYNC_ID, SYSTEM_LOCATION FROM song_sync_info;"
        self.database.cursor.execute(sql)
        results = self.database.cursor.fetchall()
        for rows in results:
            syncID= rows[0]
            systemLocation = rows[1]
            #systemLocation.replace('//','////')
            print systemLocation
            if os.path.exists(systemLocation):
                sql = "UPDATE song_sync_info SET ON_SYSTEM ='true' WHERE SYNC_ID={};".format(syncID)
                try:
                    self.database.cursor.execute(sql)
                    self.database.db.commit()
                except:
                    self.database.db.rollback()
            
            else :
                sql = "UPDATE song_sync_info SET ON_SYSTEM ='false' WHERE SYNC_ID={};".format(syncID)
                try:
                    self.database.cursor.execute(sql)
                    self.database.db.commit()
                except:
                    self.database.db.rollback()
                   
    def validateDropboxPresence(self):
        sql = "SELECT SYNC_ID, SYSTEM_LOCATION FROM song_sync_info;"
        self.database.cursor.execute(sql)
        results = self.database.cursor.fetchall()
        for rows in results:
            syncID= rows[0]
            systemLocation = rows[1]
            #systemLocation.replace('//','////')
            #print dropboxLocation
            fileLocationDropbox = self.dropboxPath+"\\{}\\{}\\".format("MusicSync", "Tracks")+str(systemLocation).split('\\')[-1:][0]
            print fileLocationDropbox
            if os.path.exists(fileLocationDropbox):
                print "ALREADY ON DROPBOX"
                sql = "UPDATE song_sync_info SET ON_DROPBOX ='true' WHERE SYNC_ID={};".format(syncID)
                try:
                    self.database.cursor.execute(sql)
                    self.database.db.commit()
                except:
                    self.database.db.rollback()
            
            else :
                print "NOT IN DROPBOX"
                sql = "UPDATE song_sync_info SET ON_DROPBOX ='false' WHERE SYNC_ID={};".format(syncID)
                try:
                    self.database.cursor.execute(sql)
                    self.database.db.commit()
                except:
                    self.database.db.rollback()
    
    def initiateTransferToDropbox(self):
        sql = "SELECT SYNC_ID,SYSTEM_LOCATION, ON_SYSTEM, ON_DROPBOX FROM song_sync_info;"
        self.database.cursor.execute(sql)
        results = self.database.cursor.fetchall()
        
        dropboxSongLocation = self.dropboxPath+"\\{}\\{}".format("MusicSync", "Tracks")
        dropboxSongLocation = dropboxSongLocation.replace('\\','\\\\')
        
        if not os.path.exists(dropboxSongLocation):
            os.makedirs(dropboxSongLocation)
        
        for rows in results:
            syncID= rows[0]
            systemLocation = rows[1]
            onSystem = rows[2]
            onDropbox = rows[3]
            
            systemLocation = systemLocation.replace("\'\'","\'")
            
            if(not onDropbox):
                if(onSystem=="true"):
                    shutil.copy(systemLocation, dropboxSongLocation)
                    sql = "UPDATE song_sync_info SET ON_DROPBOX ='true' WHERE SYNC_ID={};".format(syncID)
                    print sql
                    try:
                        self.database.cursor.execute(sql)
                        self.database.db.commit()
                    except:
                        self.database.db.rollback()
                
                
            elif(onDropbox=="false"):
                if(onSystem=="true"):
                    shutil.copy(systemLocation, dropboxSongLocation)
                    sql = "UPDATE song_sync_info SET ON_DROPBOX ='true', WHERE SYNC_ID={};".format(syncID)
                    try:
                        self.database.cursor.execute(sql)
                        self.database.db.commit()
                    except:
                        self.database.db.rollback()
        
    def generatePlaylist(self,playlistLocation,playlistName):
        
        dropboxPlaylistFolder= self.dropboxPath+"\\{}\\{}".format("MusicSync", "Playlists")
        dropboxPlaylistFolder = dropboxPlaylistFolder.replace('\\','\\\\')
        
        if not os.path.exists(dropboxPlaylistFolder):
            os.makedirs(dropboxPlaylistFolder)
            
        dropboxPlaylistLocation = dropboxPlaylistFolder+"\\\\"+playlistName
            
        
        playlistToCopy = open(playlistLocation, "r")
        playlistContent = playlistToCopy.read()
        # print m3uFileContent
        
        playlistToWrite = open(dropboxPlaylistLocation,"w")
        playlistToWrite.write("#EXTM3U\n")
        songBundle = playlistContent.split("#EXTINF:")
        for song in songBundle[1:]:
            playlistToWrite.write("#EXTINF:")
            songDetails = (song.split("\n")[0])
            playlistToWrite.write(songDetails)
            playlistToWrite.write("\n")
            songLocation = song.split("\n")[1]
            #newSongLocation = self.dropboxPath+"\\{}\\{}\\".format("MusicSync", "Tracks")+str(songLocation).split('\\')[-1:][0]
            newSongLocation = "..\\{}\\".format("Tracks")+str(songLocation).split('\\')[-1:][0]
            playlistToWrite.write(newSongLocation)
            playlistToWrite.write("\n")
            