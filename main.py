'''
Created on Jan 23, 2015

@author: serenity
'''
from MusicSync import ExtractorM3U, Database, Transfer




systemLocation = "C:\Users\serenity\Music\Playlists"
dropboxLocation = "Z:\Dropbox"
class Maindo:
    
    def do(self):
        
        
        database = Database.DataBase()
        database.establishConnection()
        
        transfer = Transfer.Transfer()
        transfer.initialSetup(dropboxLocation, database)
            
        extractor = ExtractorM3U.ExtractorM3U()
        extractor.initialSetup(database, transfer, systemLocation)
        extractor.playlistEngine()
        
        transfer.validateSystemPresence()
        transfer.validateDropboxPresence()
        transfer.initiateTransferToDropbox()

b = Maindo()
b.do()
