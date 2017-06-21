#  DotaTools main tool
#  Written by MarcusMunch
#  http://marcusmunch.github.com

from ftplib import FTP
from time import sleep

import json
import requests
import settings
import os
import sys


# Give user warning if Debug Mode is enabled in settings.py
if settings.DEBUG_MODE == True:
    try:
        print ('\n' + '='*(len(settings.DEBUG_MESSAGE)+2))
        print (' ' + settings.DEBUG_MESSAGE + ' ')
        print ('='*(len(settings.DEBUG_MESSAGE)+2) + '\n')
    except AttributeError: print ('='*73 + '\nNOTE: No DEBUG_MESSAGE set - please see settings_example.py for reference\n' + '='*73 + '\n')


def identifyHeroes(toIdentify=""):
    print "Searching for localized names for found Hero ID's...\n"
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


def gameMode():
    r = requests.get('https://dota2api.readthedocs.io/en/latest/responses.html', timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')
    section = soup.find(id='game-mode').find('tbody')
    items = list(section.stripped_strings)
    keys = []
    values = []
    for n in range(0,len(items),2):
        keys.append(int(items[n]))
    for n in range(1,len(items),2):
        values.append(items[n])
    result = dict(izip(keys, values))
    return result


def upload(toUpload=False):
    if not settings.FTP_ADDR:
        print "No FTP settings were found. Skipping upload..."
    if toUpload and settings.FTP_ADDR:
        try:
            print ('Uploading %s...' % toUpload)
            ftp = FTP(settings.FTP_ADDR)
            ftp.login(settings.FTP_ADDR, settings.FTP_PASS)
            if not 'DotaTools' in ftp.nlst():
                print 'Folder "DotaTools" not found. Creating...'
                ftp.mkd('DotaTools')
            ftp.cwd('DotaTools')
            file = open('output/' + toUpload, 'r')
            if settings.DEBUG_MODE is False:
                ftp.storbinary('STOR ' + toUpload, file)
            file.close()
            print 'Uploaded file to FTP at ' + settings.FTP_ADDR + '. Closing connection...\n'
            ftp.quit()
        except:
            print ('Unexpected error!'), sys.exc_info()

def writeToFile(output="", outFile=""):
    if outFile == "":
        print "No output selected - no file written"
    else:
        if not os.path.exists('output'):
            print 'Folder "output" not found. Creating...\n'
            if settings.DEBUG_MODE is False: os.mkdir('output')
        print ('Writing to file %s: "%s"' % (outFile, output))
        if settings.DEBUG_MODE is False:
            file = open('./output/' + outFile, "w")
            file.write(output)
            file.close
        print "Successfully wrote to file!\n"

if __name__ == '__main__':
    print " __    __  __ __   ___    ___   ____    _____ __ "
    print "|  |__|  ||  |  | /   \  /   \ |    \  / ___/|  |"
    print "|  |  |  ||  |  ||     ||     ||  o  )(   \_ |  |"
    print "|  |  |  ||  _  ||  O  ||  O  ||   _/  \__  ||__|"
    print "|  `  '  ||  |  ||     ||     ||  |    /  \ | __ "
    print " \      / |  |  ||     ||     ||  |    \    ||  |"
    print "  \_/\_/  |__|__| \___/  \___/ |__|     \___||__|"
    sleep(1)
    print "\nThis script isn't meant to be run this way - it merely contains some of the functions used by the actual scripts within this folder!"
    sleep(5)
