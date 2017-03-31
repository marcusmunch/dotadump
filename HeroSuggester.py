#!/bin/user/python
import requests, json, time
from random import randint

""" TO DO:
-Move API fix from topHeroes() to identifyHeroes()
-Print output in one line for better use with AnkhBot
-Upload output to server (maybe separate script for privacy reasons)
"""

id = open("./config.cfg", 'r').read()

def topHeroes(limit=25):
	global Heroes
	Heroes = []
	r = requests.get('https://api.opendota.com/api/players/' + str(id) + '/heroes')
	data = json.loads(r.text)
	for i in range(0,limit):
		input = int(data[i]['hero_id'])
		if input < 24: input -= 1
		else: input -= 2
		Heroes.append(input)
	identifyHeroes(Heroes)

def outsidetopHeroes(outside=10, limit=30):
	topHeroes(outside + limit)
	del Heroes[:outside]
	print len(Heroes)

def identifyHeroes(toIdentify=""):
	global HeroNames
	HeroNames = []
	r = requests.get('https://api.opendota.com/api/heroes')
	data = json.loads(r.text)
	for i in range(0, len(toIdentify)):
		lookup = int(toIdentify[i])
		HeroNames.append(data[lookup]['localized_name'])

def noRecent(minmatches, days=60):
	global Heroes
	Heroes = []
	r = requests.get('https://api.opendota.com/api/players/' + str(id) + '/Heroes')
	data = json.loads(r.text)
	longago = time.time() - 86400*days
	for i in range(0,len(data)):
		if data[i]['last_played'] == 0: None
		elif data[i]['games'] < minmatches: None
		elif data[i]['last_played'] <= longago:
			input = int(data[i]['hero_id'])
			if input < 24: input -= 1
			else: input -= 2
			Heroes.append(input)
	identifyHeroes(Heroes)

def WhatToPlay(suggestion_num=1):
	if suggestion_num <= 0: print "You specifically asked for no (or less than zero) suggestions!"
	else:
		print "I think you should play one of the following heroes:"
		suggestions = 0
		while suggestions < suggestion_num and len(HeroNames) > 0:
			rng = randint(0,len(HeroNames)) -1
			print HeroNames[rng]
			HeroNames.remove(HeroNames[rng])
			suggestions += 1

if __name__ == "__main__":
	noRecent(10, 30)
	WhatToPlay(5)
