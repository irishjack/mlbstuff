from xml.dom import minidom
import urllib
import time

#Get Score
def box_score(game_data):
	box_url = 'http://gd2.mlb.com' + game_data + '/boxscore.xml'
	xml_str2 = urllib.urlopen(box_url).read()
	xmldoc2 = minidom.parseString(xml_str2)
	
	away_score = xmldoc2.getElementsByTagName('linescore')[0].attributes['away_team_runs'].value
	home_score = xmldoc2.getElementsByTagName('linescore')[0].attributes['home_team_runs'].value
	away_hits = xmldoc2.getElementsByTagName('linescore')[0].attributes['away_team_hits'].value
	home_hits = xmldoc2.getElementsByTagName('linescore')[0].attributes['home_team_hits'].value
	away_errors = xmldoc2.getElementsByTagName('linescore')[0].attributes['away_team_errors'].value
	home_errors = xmldoc2.getElementsByTagName('linescore')[0].attributes['home_team_errors'].value

	return away_score,home_score,away_hits,home_hits,away_errors,home_errors

#function for getting alerts
def scoring_plays(game_data,away_score,home_score):
	game_url = 'http://gd2.mlb.com' + game_data + '/atv_runScoringPlays.xml'
	
	xml_str = urllib.urlopen(game_url).read()
	
	xmldoc = minidom.parseString(xml_str)
	
	if away_score or home_score > 0:
		event = xmldoc.getElementsByTagName('description')[-1].firstChild.data
	else:
		event = ''
	return event
#get values from game tag
def master_scoreboard_game(url_day):
	days_games = url_day + 'master_scoreboard.xml'
	xml_masterscore = urllib.urlopen(days_games).read()
	xmlscoreboard = minidom.parseString(xml_masterscore)
	game_values = xmlscoreboard.getElementsByTagName('game')

	return (game_values)

def master_scoreboard_status(url_day):
	days_games = url_day + 'master_scoreboard.xml'
	xml_masterscore = urllib.urlopen(days_games).read()
	xmlscoreboard = minidom.parseString(xml_masterscore)
	status_values = xmlscoreboard.getElementsByTagName('status')

	return (status_values)
#Get line score after end of inning

#get year
year = (time.strftime("%Y"))
#get two digit month
month = (time.strftime("%m"))
#get two digit day 
day = (time.strftime("%d"))


url_day = 'http://gd2.mlb.com/components/game/mlb/year_' + year + '/month_' + month +'/day_' + day + '/'

#get todays games

game_values = master_scoreboard_game(url_day)

#find game of particular team
#print (game_values[1].attributes['id'].value)
count = 0
pre_count = 0
game_count = 0
current_inning = 0
lastscore = ''
scoreplay = ''
for gameid in game_values:
	#print gameid.attributes['id'].value
	#count +=1
	if 'ari' in gameid.attributes['id'].value: 
		#print gameid.attributes['id'].value
		status_values = master_scoreboard_status(url_day)
		game_status = status_values[count].attributes['status'].value
		while game_status == "Pre-Game":
			if pre_count == 1:
				print gameid.attributes['away_name_abbrev'].value + ' @ ' + gameid.attributes['home_name_abbrev'].value +' start at ' + gameid.attributes['time'].value + ' ' + gameid.attributes['ampm'].value + ' ' + gameid.attributes['time_zone'].value
			pre_count +=1
			#time.sleep(30)
			pass
		while game_status == "Warmup":
			pre_count = 0
			if pre_count == 0:
				print 'Game start ' + gameid.attributes['away_name_abbrev'].value + ' @ ' + gameid.attributes['home_name_abbrev'].value
				#print xmlscoreboard.getElementsByTagName('pitcher')[count].attributes['first'].value + ' ' + xmlscoreboard.getElementsByTagName('pitcher')[count].attributes['last'].value + ' ' + xmlscoreboard.getElementsByTagName('pitcher')[count].attributes['era'].value + 'ERA ' + xmlscoreboard.getElementsByTagName('pitcher')[count].attributes['wins'].value + '-' + xmlscoreboard.getElementsByTagName('pitcher')[count].attributes['losses'].value
				#print 'VS'
				#print xmlscoreboard.getElementsByTagName('opposing_pitcher')[count].attributes['first'].value + ' ' + xmlscoreboard.getElementsByTagName('opposing_pitcher')[count].attributes['last'].value
			#time.sleep(30)
			pre_count +=1			
			pass
		while game_status == "In Progress":
			#if game_count == 0:
				#
			(away_score,home_score,away_hits,home_hits,away_errors,home_errors) = box_score(gameid.attributes['game_data_directory'].value)
			away_score = int(away_score)
			home_score = int(home_score)
			if home_score or away_score > 0:
				scoreplay = scoring_plays(gameid.attributes['game_data_directory'].value,away_score,home_score)
			if scoreplay != lastscore:
				print scoreplay
				lastscore = scoreplay
				print str(away_score) + ' ' + gameid.attributes['away_name_abbrev'].value + ' @ ' + str(home_score) + ' ' + gameid.attributes['home_name_abbrev'].value
				#print xmlscoreboard.getElementsByTagName('r')[count].attributes['away'].value
			inning_state = game_status[count].attributes['inning_state'].value
			inning = game_status[count].attributes['inning'].value
			#print inning_state
			if inning_state == "End":
				print inning_state
				if game_status[count].attributes['inning'].value != current_inning:
					print gameid.attributes['away_name_abbrev'].value + ' ' + str(away_score) + ' runs ' + away_hits + ' hits ' + away_errors + ' errors' 
			#time.sleep(30)
			pass
	count +=1
		
