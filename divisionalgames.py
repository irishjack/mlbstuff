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

def linescore(url_day,gameindex):
	days_games = url_day + 'master_scoreboard.xml'
	xml_masterscore = urllib.urlopen(days_games).read()
	xmlscoreboard = minidom.parseString(xml_masterscore)
	game_values = xmlscoreboard.getElementsByTagName('r')

	away_score = game_values[gameindex].attributes['away'].value
	home_score = game_values[gameindex].attributes['home'].value

	return away_score,home_score

def master_scoreboard_status(url_day):
	days_games = url_day + 'master_scoreboard.xml'
	xml_masterscore = urllib.urlopen(days_games).read()
	xmlscoreboard = minidom.parseString(xml_masterscore)
	status_values = xmlscoreboard.getElementsByTagName('status')

	return (status_values)

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
pre_game_print = []
post_game_print = []
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
pre_game_print = ['N'] * game_count
post_game_print = ['N'] * game_count
#print division_games_id

while any('F' != i for i in game_status_flag):

	#print all('F' != i for i in game_status_flag)

	for i, f in enumerate(game_status_flag):

		for gameindex, gameid in enumerate(game_values):

			if division_games_id[i] in gameid.attributes['id'].value:

				#print gameid.attributes['id'].value

				status_values = master_scoreboard_status(url_day)
				game_status = status_values[gameindex].attributes['status'].value

				#print game_status

				if game_status == "Pre-Game":

					if pre_game_print[i] == "N":
						print gameid.attributes['away_name_abbrev'].value + ' @ ' + gameid.attributes['home_name_abbrev'].value +' start at ' + gameid.attributes['time'].value + ' ' + gameid.attributes['ampm'].value + ' ' + gameid.attributes['time_zone'].value
						pre_game_print[i] = 'Y'

				if game_status == "Warmup":

					pass

				if game_status == "In Progress":

					game_status_flag[i] = 'G' 

				else:

					if post_game_print[i] == "N":

						away_score,home_score = linescore(url_day,gameindex)
						print 'Final ' + gameid.attributes['away_name_abbrev'].value + ' ' + away_score + ' @ ' + gameid.attributes['home_name_abbrev'].value + ' ' + home_score
						post_game_print[i] = 'Y'
						game_status_flag[i] = 'F'
	time.sleep(300)