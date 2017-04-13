#!/bin/user/python
from ftplib import FTP
from random import randint

import json
import requests
import settings
import sys
import time

# DotaTools Solo MMR tracker, written by MarcusMunch
# Last updated April 13th 2017

# Edit below line to change name of file being output
outFile = 'solommr.txt'


# Give user warning if Debug Mode is enabled in settings.py
if settings.DEBUG_MODE == True:
    print ('\n' + '='*(len(settings.DEBUG_MESSAGE)+2))
    print (' ' + settings.DEBUG_MESSAGE + ' ')
    print ('='*(len(settings.DEBUG_MESSAGE)+2) + '\n')


# Look up basic profile data
def lookup(param=""):
    if param:
        r = requests.get('https://api.opendota.com/api/players/' + settings.STEAM_ID)
        data = json.loads(r.text)
        if param: print ('Your "' + param + '" is: ' + data[param])
        return data[param]

# Some profile data requires you to look deeper into the profile.
def profileLookup(param=""):
    if param:
        r = requests.get('https://api.opendota.com/api/players/' + settings.STEAM_ID)
        data = json.loads(r.text)
        return data['profile'][param]

# Convert returned number of seconds since Epoch to human-readable time
def translateTime(inputTime=time.time()):
    return time.strftime('%m/%d %H:%M:%S', time.localtime(int(inputTime)))

def compileOutput(result='', outputTime=time.time()):
    global output
    output = ''
    if result:
        output = 'Solo MMR for player "' + profileLookup('personaname') + '" as of ' + translateTime(lookup('tracked_until')) + ': ' + result

def writeToFile(output="", outFile=""):
    if outFile == "":
        print "No output selected - no file written"
    else:
        print ("Writing to file " + outFile + ': "' + output + '"')
        if settings.DEBUG_MODE is False:
            file = open('./output/' + outFile, "w")
            file.write(output)
            file.close
        print "Successfully wrote to file!\n"

def uploadToFTP(toUpload=False):
    if not settings.FTP_ADDR:
        print "No FTP settings were found. Skipping upload..."
    if toUpload and settings.FTP_ADDR:
        try:
            print ('Uploading ' + toUpload + '...')
            ftp = FTP(settings.FTP_ADDR)
            ftp.login(settings.FTP_ADDR, settings.FTP_PASS)
            if not 'DotaTools' in ftp.nlst():
                print 'Folder "DotaTools" not found. Creating...'
                ftp.mkd('DotaTools')
            ftp.cwd('DotaTools')
            file = open('output/' + toUpload, 'r')
            if settings.DEBUG_MODE is False:
                ftp.storbinary('STOR ' + outFile, file)
            file.close()
            print 'Uploaded file to FTP at ' + settings.FTP_ADDR + '. Closing connection...\n'
            ftp.quit()
        except:
            print ('Unexpected error!'), sys.exc_info()

if __name__ == '__main__':
    compileOutput(lookup('solo_competitive_rank'))
    writeToFile(output, outFile)
    uploadToFTP(outFile)
