import DotaTools
import json
import os
import requests
import settings
import time

from whattoplay import identifyHeroes

# Edit below line to change name of file being output
base = os.path.basename(__file__)
outFile = os.path.splitext(base)[0] + '.txt'


# get time in secs since epoch for today at 4 AM - hopefully you're not playing Dota this late(!)
def setLimit():
	reset_time = time.mktime((time.localtime()[0], time.localtime()[1], time.localtime()[2], 4, 0, 0, -1, -1, -1))
	reset_struct = time.localtime(reset_time)


def matchesToday():
	r = requests.get("https://api.opendota.com/api/players/%s/matches?date=1" % settings.STEAM_ID)
	data = json.loads(r.text)
	output = {}
	print 'Getting matches played today...'
	for match in range(0,len(data)): # To ensure that we only get matches today and not within 24 hours
		if 'reset_time' in globals() and not settings.DEBUG_MODE:
			if data[match]['start_time'] >= reset_time: output[match] = data[match]
		else: output[match] = data[match]
	if output == {}:
		print 'No games played today!'
	else:
		identifyHeroes(output)
	return output


def appendResult(input):
	for i in range(0,len(input)):
		if input[i]['player_slot'] <= 4 and input[i]['radiant_win'] == True: input[i]['result'] = 'Win'  # Radiant victory
		elif input[i]['player_slot'] >= 128 and input[i]['radiant_win'] == False: input[i]['result'] = 'Win'  # Dire victory
		else: input[i]['result'] = 'Loss'
	return input


def identifyLobby(match):
	lobbynum = match['lobby_type']
	if lobbynum == 0: return 'Unranked'
	if lobbynum == 1: return 'Practice'
	if lobbynum == 2: return 'Tournament'
	if lobbynum == 3: return 'Tutorial'
	if lobbynum == 4: return 'Co-op with AI'
	if lobbynum == 5: return 'Team match'
	if lobbynum == 6: return 'Solo queue'
	if lobbynum == 7: return 'Ranked'
	if lobbynum == 8: return '1v1 solo mid'
	if lobbynum == 9: return 'Seasonal ranked'


def compileOutput():
	HeroPool = matchesToday()
	if len(HeroPool) > 0:
		appendResult(HeroPool)
		output = []
		for item in range(0,len(HeroPool)):
			output.append('%s (%s %s)' % (HeroPool[item]['localized_name'], identifyLobby(HeroPool[item]), HeroPool[item]['result']))
		return ('Heroes played today: ' + ', '.join(output) + '.')
	else: return 'No games played so far today!'


def main():
	DotaTools.writeToFile(compileOutput(), outFile)
	DotaTools.upload(outFile)


if __name__ == '__main__':
	main()
