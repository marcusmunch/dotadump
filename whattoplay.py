#!/bin/user/python

# DotaTools Hero Suggester, written by MarcusMunch
# http://github.com/MarcusMunch

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
outFile = os.path.splitext(base)[0] + '.txt'


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
    print 'Finding heroes not played within the last %s days (minimum of %s games played and minimum win rate of %s%%)...' % (days, minmatches, settings.SUGGEST_MIN_WINRATE)
    r = requests.get('https://api.opendota.com/api/players/%s/Heroes' % settings.STEAM_ID)
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
    if len(pickFrom) == 0:
        print 'No heroes fulfill the selected criteria'
        return ''
    else:
        print '\nNow, what should you play today? \nPicking %s out of %s eligible heroes...\n' % (min(suggestion_num, len(pickFrom)), len(pickFrom))
        if suggestion_num <= 0:
            print "\nYou specifically asked for no (or less than zero(!)) suggestions!"
        else:
            leader = (str(suggestion_num) + ' hero challenge for ' + time.strftime("%d/%m-%Y") + ': ')
            suggestions = 0
            challenge = []
            def winrate(hero):
                rate = '%.2f' % (float(pickFrom[hero]['win']) / float(pickFrom[hero]['games'])*100)
                return ('(%s%% win)') % rate
            while suggestions < suggestion_num and len(pickFrom) > 0:
                rng = randint(0, len(pickFrom)) - 1
                string = pickFrom[rng]['localized_name'] + ' ' + winrate(rng)
                challenge.append(string)
                pickFrom.remove(pickFrom[rng])
                suggestions += 1
            output = leader + ', '.join(challenge) + '.' 
            return output


def main():
    HeroPool = noRecent(settings.SUGGEST_MIN_GAMES, settings.SUGGEST_MIN_DAYS)
    ToPlay = whatToPlay(identifyHeroes(HeroPool), settings.SUGGEST_AMOUNT)
    DotaTools.writeToFile(ToPlay, outFile)
    DotaTools.upload(outFile)


if __name__ == "__main__":
    main()
