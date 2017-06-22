import DotaTools
import json
import os
import requests
import settings
import sys
import time

# Edit below line to change name of file being output
base = os.path.basename(__file__)
outFile = os.path.splitext(base)[0] + '.txt'


# get time in secs since epoch for today at 4 AM - hopefully you're not playing Dota this late(!)
def setLimit(format):
	reset_time = time.mktime((time.localtime()[0], time.localtime()[1], time.localtime()[2], 4, 0, 0, -1, -1, -1))
	reset_struct = time.localtime(reset_time)
	if format == 'seconds': return reset_time
	elif format == 'struct': return reset_struct
	else: 
		print 'Error in setLimit(format): "format" must be either "seconds" or "struct"!\n'
		sys.exit()

def matchesToday():
	r = requests.get("https://api.opendota.com/api/players/%s/matches?date=10" % settings.STEAM_ID)
	data = json.loads(r.text)
	reset = setLimit('seconds')
	t = setLimit('struct')
	output = {}
	print 'Getting matches played today...'
	for match in range(0,len(data)): # This enables debugging by removing games played after reset time
		if not settings.DEBUG_MODE:
			if data[match]['start_time'] >= reset: output[match] = data[match]
		else: output[match] = data[match]
	if output == {}:
		print 'No games played today!\n'
	else:
		DotaTools.identifyHeroes(output)
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
	if lobbynum == 9: return 'Battle Cup'


def compileOutput():
	pool = matchesToday()
	mode = DotaTools.gameMode()
	if len(pool) > 0:
		appendResult(pool)
		out = []
		for i in range(0,len(pool)):
			out.append('%s (%s - %s) at %s' % (pool[i]['localized_name'], mode[(pool[i]['game_mode'])], pool[i]['result'], time.strftime('%H:%M', time.localtime(pool[i]['start_time']))))
		out.reverse()
		return ('Heroes played today: ' + ', '.join(out) + '.')
	else: return 'No games played so far today!'


def main():
	DotaTools.writeToFile(compileOutput(), outFile)
	DotaTools.upload(outFile)


if __name__ == '__main__':
	main()
