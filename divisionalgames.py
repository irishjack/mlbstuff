#!/usr/bin/env python
from xml.dom import minidom
import urllib
import time

#This gets the game start data and final scores of gomes in a division.
#AL Central league id 103 division C

def master_scoreboard_game(url_day):
	days_games = url_day + 'master_scoreboard.xml'
	xml_masterscore = urllib.urlopen(days_games).read()
	xmlscoreboard = minidom.parseString(xml_masterscore)
	game_values = xmlscoreboard.getElementsByTagName('game')

	return (game_values)

#get year
year = (time.strftime("%Y"))
#get two digit month
month = (time.strftime("%m"))
#get two digit day 
day = (time.strftime("%d"))


url_day = 'http://gd2.mlb.com/components/game/mlb/year_' + year + '/month_' + month +'/day_' + day + '/'

#get todays games

game_values = master_scoreboard_game(url_day)

count = 0

division_games_id = []
game_status_flag = []
game_count = 0

#gets the game id of any game played by divisional opponents that are not 
for gameid in game_values:
	if gameid.attributes['away_league_id'].value == '103' or gameid.attributes['home_league_id'].value == '103':
		if gameid.attributes['away_division'].value == 'C' or gameid.attributes['home_division'].value == 'C':
			if not 'cle' in gameid.attributes['id'].value:
				if not gameid.attributes['id'].value in division_games_id:
					division_games_id.append(gameid.attributes['id'].value)

game_count = len(division_games_id)

game_status_flag = ['U'] * game_count

while all(i != 'F' for i in game_status_flag):
	print count
	print game_status_flag[count]
	game_status_flag[count] = 'F'
	print game_status_flag
	count =+1