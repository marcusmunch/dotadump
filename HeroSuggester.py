#!/bin/user/python
import requests, json, time, os, sys
from random import randint
from ftplib import FTP

# DotaTools Hero Suggester, written by MarcusMunch
# Last updated March 3rd 2017

def fetchID():
	global id, FTPaddr, FTPpass
	file = open("config.ini", 'r').read()
	credent = json.loads(file)
	id = credent['steamID']
	FTPaddr = credent['FTPaddr']
	FTPpass = credent['FTPpass']

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
	print "Converting found Hero ID's to localized names..."
	r = requests.get('https://api.opendota.com/api/heroes')
	data = json.loads(r.text)
	for i in range(0, len(toIdentify)):
		lookup = int(toIdentify[i])
		HeroNames.append(data[lookup]['localized_name'])

def noRecent(minmatches=10, days=60):
	global Heroes
	Heroes = []
	print ('Finding heroes not played within the last ' + str(days) + ' days (minimm of ' + str(minmatches) + ' games played)...')
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

def whatToPlay(suggestion_num=1):
	print ('\nNow, what should you play today? \nPicking ' + str(suggestion_num) + ' out of ' + str(len(HeroNames)) + ' eligible heroes...\n')
	if suggestion_num <= 0: print "\nYou specifically asked for no (or less than zero(!)) suggestions!"
	else:
		leader = (str(suggestion_num) + ' hero challenge for ' + time.strftime("%d/%m-%Y") + ': ')
		suggestions = 0
		challenge = []
		while suggestions < suggestion_num and len(HeroNames) > 0:
			rng = randint(0,len(HeroNames)) -1
			challenge.append(HeroNames[rng])
			HeroNames.remove(HeroNames[rng])
			suggestions += 1
		return (leader + ', '.join(challenge) + '.')

def writeToFile(output="", outFile=""):
	if outFile == "": print "No output selected - no file written"
	else:
		global outputFile
		file = open('./output/' + outFile, "w")
		print ("Writing to file " + outFile + ': "' + output + '"')
		file.write(output)
		print "Successfully wrote to file!\n"
		file.close

def uploadToFTP(toUpload=False):
	if toUpload:
		try:
			ftp = FTP(FTPaddr)
			ftp.login(FTPaddr, FTPpass)
			if not 'DotaTools' in ftp.nlst():
				print 'Folder "DotaTools" not found. Creating...'
				ftp.mkd('DotaTools')
			ftp.cwd('DotaTools')
			file = open('output/' + toUpload, 'r')
			ftp.storbinary('STOR WhatToPlay.txt', file)
			file.close()
			print 'Uploaded file to FTP at ' + FTPaddr + '. Closing connection...\n'
			ftp.quit()
		except: print ('Unexpected error!'), sys.exc_info()

if __name__ == "__main__":
	fetchID()
	noRecent(10, 30)
	writeToFile(whatToPlay(3), 'WhatToPlay.txt')
	uploadToFTP('WhatToPlay.txt')
