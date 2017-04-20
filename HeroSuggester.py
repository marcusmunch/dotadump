#!/bin/user/python
from ftplib import FTP
from random import randint

import json
import os
import requests
import settings
import sys
import time


# DotaTools Hero Suggester, written by MarcusMunch
# Last updated April 19th 2017

# Edit below line to change name of file being output
outFile = 'whattoplay.txt'

# Give user warning if Debug Mode is enabled in settings.py
if settings.DEBUG_MODE == True:
    try:
        print ('\n' + '='*(len(settings.DEBUG_MESSAGE)+2))
        print (' ' + settings.DEBUG_MESSAGE + ' ')
        print ('='*(len(settings.DEBUG_MESSAGE)+2) + '\n')
    except AttributeError: print ('='*73 + '\nNOTE: No DEBUG_MESSAGE set - please see settings_example.py for reference\n' + '='*73 + '\n')


def identifyHeroes(toIdentify=""):
    print "Searching for localized names for found Hero ID's."
    r = requests.get('https://api.opendota.com/api/heroes')
    data = json.loads(r.text)
    for i in range(0, len(toIdentify)):
        lookup = int(toIdentify[i]['hero_id'])
        if lookup < 24:
            lookup -= 1
        else:
            lookup -= 2
        toIdentify[i]['localized_name'] = data[lookup]['localized_name']
    return toIdentify


def noRecent(minmatches=10, days=60):
    output = []
    print ('Finding heroes not played within the last ' + str(days) + ' days (minimum of ' + str(
        minmatches) + ' games played and minimum win rate of ' + str(settings.SUGGEST_MIN_WINRATE)   + '%)...')
    r = requests.get('https://api.opendota.com/api/players/' + settings.STEAM_ID + '/Heroes')
    data = json.loads(r.text)
    longago = time.time() - (86400 * days)
    for i in range(0, len(data)):
        if data[i]['games'] > 0: winrate = (float(data[i]['win']) / float(data[i]['games'])) * 100
        else: winrate = 0
        if data[i]['last_played'] == 0: None
        elif winrate <= settings.SUGGEST_MIN_WINRATE: None
        elif data[i]['games'] <= minmatches: None
        elif data[i]['last_played'] <= longago:
            oldHero = data[i]
            output.append(oldHero)
    return output


def whatToPlay(pickFrom, suggestion_num=3):
    print ('\nNow, what should you play today? \nPicking ' + str(suggestion_num) + ' out of ' + str(
        len(pickFrom)) + ' eligible heroes...\n')
    if suggestion_num <= 0:
        print "\nYou specifically asked for no (or less than zero(!)) suggestions!"
    else:
        leader = (str(suggestion_num) + ' hero challenge for ' + time.strftime("%d/%m-%Y") + ': ')
        suggestions = 0
        challenge = []
        while suggestions < suggestion_num and len(pickFrom) > 0:
            rng = randint(0, len(pickFrom)) - 1
            challenge.append(pickFrom[rng]['localized_name'])
            pickFrom.remove(pickFrom[rng])
            suggestions += 1
        output = leader + ', '.join(challenge) + '.' 
        return output


def writeToFile(output="", outFile=""):
    if outFile == "":
        print "No output selected - no file written"
    else:
        if not os.path.exists('output'):
            print 'Folder "output" not found. Creating...\n'
            if settings.DEBUG_MODE is False: os.mkdir('output')
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
                ftp.storbinary('STOR WhatToPlay.txt', file)
            file.close()
            print 'Uploaded file to FTP at ' + settings.FTP_ADDR + '. Closing connection...\n'
            ftp.quit()
        except:
            print ('Unexpected error!'), sys.exc_info()


def main():
    HeroPool = noRecent(settings.SUGGEST_MIN_GAMES, settings.SUGGEST_MIN_DAYS)
    ToPlay = whatToPlay(identifyHeroes(HeroPool), settings.SUGGEST_AMOUNT)
    writeToFile(ToPlay, outFile)
    uploadToFTP(outFile)

if __name__ == "__main__":
    main()
