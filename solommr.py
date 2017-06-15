#!/bin/user/python

# DotaTools Solo MMR tracker, written by MarcusMunch
# http://github.com/MarcusMunch

from ftplib import FTP
from random import randint

import DotaTools
import json
import os
import requests
import settings
import sys
import time


# Set output filename to be the same at the basename of this script
base = os.path.basename(__file__)
outFile = os.path.splitext(base)[0]


# Give user warning if Debug Mode is enabled in settings.py
if settings.DEBUG_MODE == True:
    try:
        print ('\n' + '='*(len(settings.DEBUG_MESSAGE)+2))
        print (' ' + settings.DEBUG_MESSAGE + ' ')
        print ('='*(len(settings.DEBUG_MESSAGE)+2) + '\n')
    except AttributeError: print ('='*73 + '\nNOTE: No DEBUG_MESSAGE set - please see settings_example.py for reference\n' + '='*73 + '\n')


# Look up basic profile data
def lookup(param=""):
    if param:
        r = requests.get('https://api.opendota.com/api/players/' + settings.STEAM_ID)
        data = json.loads(r.text)
        return data[param]


# Some profile data requires you to look deeper into the profile.
def profileLookup(param=""):
    if param:
        r = requests.get('https://api.opendota.com/api/players/' + settings.STEAM_ID)
        data = json.loads(r.text)
        return data['profile'][param]


# Convert returned number of seconds since Epoch to human-readable time
def translateTime(inputTime=time.time()):
    return time.strftime('%d/%m %H:%M:%S', time.localtime(int(inputTime)))


# Compile the output that will be written to the file
def compileOutput(result='', outputTime=time.time()):
    global output
    output = ''
    if result:
        data = json.loads(requests.get('https://api.opendota.com/api/players/%s/matches?limit=1&lobby_type=7' % settings.STEAM_ID).text)
        output = 'Solo MMR for player "%s" as of %s: %s' % (profileLookup('personaname'), translateTime(data[0]['start_time'] + data[0]['duration']), result)


def main():
    def mmrNoUpdate():
        if not os.path.exists('./output/' + outFile): return False
        oldOutput = open('./output/' + outFile, 'r').read()
        oldMMR = oldOutput[-len(lookup('solo_competitive_rank')):]
        if oldMMR == lookup('solo_competitive_rank'):
            return True
    if not mmrNoUpdate():
        print 'Looking up solo MMR...'
        print 'Current solo MMR is %s\n' % lookup('solo_competitive_rank')
        compileOutput(lookup('solo_competitive_rank'))
        DotaTools.writeToFile(output, outFile)
        DotaTools.upload(outFile)
    else: print (time.strftime('[%d/%m-%y %H:%M]: ') + 'No new MMR. No changes will be written.')


if __name__ == '__main__':
    main()
    