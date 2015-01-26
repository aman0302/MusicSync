'''
Created on Jan 24, 2015

@author: serenity
'''

import MySQLdb

class DataBase:
    
    def establishConnection(self):
        try:
            self.db = MySQLdb.connect(host="localhost",user="root",passwd="mariolla",db="Music_Sync")
        
        except MySQLdb.Error, e:
            self.firstTimeSetUp()
            self.db = MySQLdb.connect(host="localhost",user="root",passwd="mariolla",db="Music_Sync")
            
        self.cursor = self.db.cursor()
        return self.cursor
    
    def closeConnection(self):
        self.db.close()
        
    def firstTimeSetUp(self):
        print "first time"
        self.db = MySQLdb.connect(host="localhost",user="root",passwd="mariolla")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS Music_Sync")
        self.db = MySQLdb.connect(host="localhost",user="root",passwd="mariolla",db="Music_Sync")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE playlists (PLAYLIST_ID int NOT NULL AUTO_INCREMENT, PLAYLIST_NAME varchar(255) NOT NULL, LAST_MODIFIED varchar(255) NOT NULL, PRIMARY KEY(PLAYLIST_ID)); ")
        self.cursor.execute("CREATE TABLE songs (SONG_ID int NOT NULL AUTO_INCREMENT, SONG_NAME varchar(255), PRIMARY KEY(SONG_ID));")
        self.cursor.execute("CREATE TABLE playlists_songs_map(MAP_ID int NOT NULL AUTO_INCREMENT, PLAYLIST_ID int, SONG_ID int, PRIMARY KEY(MAP_ID));")
        self.cursor.execute("CREATE TABLE song_sync_info(SYNC_ID int NOT NULL AUTO_INCREMENT, SONG_ID int, SYSTEM_LOCATION varchar(1000), ON_SYSTEM ENUM('true','false'), ON_DROPBOX ENUM('true','false'), PRIMARY KEY (SYNC_ID));") 
    
    def checkIfPlaylistExists(self,database,playlist,modifiedDate):
        sql = "SELECT PLAYLIST_ID, LAST_MODIFIED FROM playlists WHERE PLAYLIST_NAME = '{}'".format(playlist)
        print sql
        database.cursor.execute(sql)
        results = database.cursor.fetchall()
        
        if not results:
            print "PLAYLIST DOES NOT EXISTS"
            return 0
        
        else:
            print "PLAYLIST EXISTS"
            for row in results:
                playlistID = row[0]
                lastModified = row[1]
                
                print lastModified
                
                #if(modifiedDate == lastModified):
                #    return -1
                
                #else:
                return playlistID
                
                
            
    
    def checkIfSongExists(self,songName):
         
        return 1
     
    def createNewPlaylist(self,playlistName,lastModifed):
        
        sql = "INSERT INTO playlists (PLAYLIST_NAME, LAST_MODIFIED) VALUES ('{}','{}');".format(playlistName, lastModifed)
        print sql
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            
        sql = "SELECT LAST_INSERT_ID();"
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        
        print "NEW PLAYLIST CREATED "+playlistName 
        print results[0]
        return results[0]
    
    def putSongInDB(self, songLocation, songName, songDuration, playlistNumber):
        
        songName = songName.replace("\'","\'\'")
        songLocation = songLocation.replace("\'","\'\'")
        
        print "MODIFIED EXTRACTED SONG NAME FOR MYSQL : "+songName
        print "MODIFIED EXTRACTED SONG LOCATION FOR MYSQL : "+songLocation
        
        sql = "SELECT SONG_ID FROM songs WHERE SONG_NAME = '{}'".format(songName)
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        songID =0
        
        if not results:
            print "SONG DOES NOT EXIST"
            sql = "INSERT INTO songs (SONG_NAME) VALUES ('{}');".format(songName)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                
            sql = "SELECT LAST_INSERT_ID();"
            self.cursor.execute(sql)
            results = self.cursor.fetchone()
            songID=results[0]
            
            
        else:
            print "SONG EXISTS"
            songID = results[0]
            
        print "SONG ID : ",songID
        print "SONG NAME MODIFIED: ",songName
        
        
        sql = "SELECT MAP_ID FROM playlists_songs_map WHERE SONG_ID = '{}' AND PLAYLIST_ID='{}';".format(songID,playlistNumber)
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        
        if not results:
        
            sql = "INSERT INTO playlists_songs_map (PLAYLIST_ID, SONG_ID) VALUES ({},{});".format(playlistNumber ,songID)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        
        sql = "SELECT SYNC_ID FROM song_sync_info WHERE SONG_ID = '{}'".format(songID)
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        
        if not results:
            sql = "INSERT INTO song_sync_info (SONG_ID, SYSTEM_LOCATION) VALUES ({},'{}');".format(songID, songLocation)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        #return songID
            
        
        