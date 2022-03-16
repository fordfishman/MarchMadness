#!/usr/bin/env python

##This program uses Five Thirty Eight's NCAAM power rankings (made through combining BPI, ELO, and other sources)
##to predict an outcome of March Madness.  If teams win, their ranking is slightly increased.  If an underdog 
##wins, then their ranking is improved based upon how much worse they were considered than the other team
##by a tier-based approach.  

##Set up argparse to take in command line arguments

#teams: names of teams in order of power rankings; FORMAT: One team name per line (i.e. Miami(FL)\n)
#rankings: power rankings greatest to least; FORMAT: One rank per line (98.2\n)
#DEPRECATED!! - randomnumbers: randomly generated integers 1-100 (currently using R, would like to do it natively in Python); FORMAT: All integers spaced on one line separated by spaces(4 23 41 51...)
#firstround: first round matchups; FORMAT: matchups arranged by region (east, west, midwest, south), team names separated by space in single line, one matchup per row (Wisconsin VirginiaTech\n)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-t','--teams')
parser.add_argument('-r','--rankings')
#parser.add_argument('--randomnumbers')
parser.add_argument('-f','--firstround')
parser.add_argument('-o','--output', default = 'MarchMadnessResults.txt')
arguments = parser.parse_args()
teams_filename = arguments.teams
rankings_filename = arguments.rankings
#randomnumbers_filename = arguments.randomnumbers
firstround_filename = arguments.firstround
output = arguments.output

#List to contain team names in order of original power ranking
teams_list = []
#Dict. to contain power rankings in original order
team_rank = {}

#Imports team names
with open(teams_filename, 'r') as teamfile:
	for team in teamfile:
		team = team.strip()
		teams_list.append(team)

#Imports power rankings, and creates a dictionary entry for each team of form TeamName: Powerrank
with open(rankings_filename, 'r') as rankingsfile:
	for index, rank in enumerate(rankingsfile):
		rank = float(rank.strip())
		team_rank[teams_list[index]] = rank


#Creates a set of random numbers to determine wins
from random import *
ran_num = []
for x in range(63):
	ran_num.append(uniform(1,100))

#Imports first round matchups
matchups= []
with open(firstround_filename, 'r') as firstround_file:
	for index, line in enumerate(firstround_file):
		game = line.split(' ')
		game[0] = game[0].strip()
		game[1] = game[1].strip()
		matchups.append(game)

#Defines regions
east = matchups[0:8]
west = matchups[8:16]
midwest = matchups[16:24]
south = matchups[24:32]


#Defining main function "probability."  Takes the team power ranks of the matchup and converts it into form:
#r = 10^(PR/10)
#Where PR is the power rank, and r is new rank.  
#New ranks are compared by form of 1. (rank2/rank1+rank2) or 2. (rank1/rank1+rank2) (depending on which rank is higher
#This determines probability of victory.  If (random number)/100 in case 1. is above probability, then team 1 wins.
#If a team wins, its rating is increased.  If the winning team's power ranking was lower, it will raised according to how much lower it was.
def probability(team1, team2, ind):
	rank1 = 10 ** (team_rank[team1]/10)
	rank2 = 10 ** (team_rank[team2]/10)
	if rank1 >= rank2:
		prob = (rank2/(rank1+rank2))
		if (ran_num[ind])/100 > prob:
			winner = team1
			team_rank[team1] += 0.15
		else:
			winner = team2
			if ((team_rank[team2]-team_rank[team1]) > -1):
				team_rank[team2] += 0.25
			elif (team_rank[team2]-team_rank[team1]) >  -1.5:
				team_rank[team2] += 0.5
			elif (team_rank[team2]-team_rank[team1]) >  -3:
				team_rank[team2] += 1
			elif (team_rank[team2]-team_rank[team1]) >  -5:
				team_rank[team2] += 1.5
			elif (team_rank[team2]-team_rank[team1]) >  -7.5:
				team_rank[team2] += 2.0
			elif (team_rank[team2]-team_rank[team1]) >  -10:
				team_rank[team2] += 3.0
			elif (team_rank[team2]-team_rank[team1]) >  -15:
				team_rank[team2] += 4.0			
	else:
		prob = rank1/(rank1+rank2)
		if (ran_num[ind])/100 > prob:
			winner = team2
			team_rank[team1] += 0.15
		else:
			winner = team1
			if ((team_rank[team2]-team_rank[team1]) > -1):
				team_rank[team2] += 0.25
			elif (team_rank[team2]-team_rank[team1]) >  -1.5:
				team_rank[team2] += 0.5
			elif (team_rank[team2]-team_rank[team1]) >  -3:
				team_rank[team2] += 1
			elif (team_rank[team2]-team_rank[team1]) >  -5:
				team_rank[team2] += 1.5
			elif (team_rank[team2]-team_rank[team1]) >  -7.5:
				team_rank[team2] += 2.0
			elif (team_rank[team2]-team_rank[team1]) >  -10:
				team_rank[team2] += 3.0
			elif (team_rank[team2]-team_rank[team1]) >  -15:
				team_rank[team2] += 4.0
	return winner

#The rest of the code will go region by region until the final four and championship games

#establishes index for random number cycling
i = 0

#ROUNDOF64
eastfirst = []
for game in east:
	win = probability(game[0], game[1], i)
	i += 1
	if win in east[0]:
		eastfirst.append([win])
	if win in east[1]:
		eastfirst[0].append(win)
	if win in east[2]:
		eastfirst.append([win])
	if win in east[3]:
		eastfirst[1].append(win)
	if win in east[4]:
		eastfirst.append([win])
	if win in east[5]:
		eastfirst[2].append(win)
	if win in east[6]:
		eastfirst.append([win])
	if win in east[7]:
		eastfirst[3].append(win)
westfirst = []
for game in west:
	win = probability(game[0], game[1], i)
	i += 1
	if win in west[0]:
		westfirst.append([win])
	if win in west[1]:
		westfirst[0].append(win)
	if win in west[2]:
		westfirst.append([win])
	if win in west[3]:
		westfirst[1].append(win)
	if win in west[4]:
		westfirst.append([win])
	if win in west[5]:
		westfirst[2].append(win)
	if win in west[6]:
		westfirst.append([win])
	if win in west[7]:
		westfirst[3].append(win)
midwestfirst = []
for game in midwest:
	win = probability(game[0], game[1], i)
	i += 1
	if win in midwest[0]:
		midwestfirst.append([win])
	if win in midwest[1]:
		midwestfirst[0].append(win)
	if win in midwest[2]:
		midwestfirst.append([win])
	if win in midwest[3]:
		midwestfirst[1].append(win)
	if win in midwest[4]:
		midwestfirst.append([win])
	if win in midwest[5]:
		midwestfirst[2].append(win)
	if win in midwest[6]:
		midwestfirst.append([win])
	if win in midwest[7]:
		midwestfirst[3].append(win)
southfirst = []
for game in south:
	win = probability(game[0], game[1], i)
	i += 1
	if win in south[0]:
		southfirst.append([win])
	if win in south[1]:
		southfirst[0].append(win)
	if win in south[2]:
		southfirst.append([win])
	if win in south[3]:
		southfirst[1].append(win)
	if win in south[4]:
		southfirst.append([win])
	if win in south[5]:
		southfirst[2].append(win)
	if win in south[6]:
		southfirst.append([win])
	if win in south[7]:
		southfirst[3].append(win)

#ROUNDOF32
eastsecond = []
for game in eastfirst:
	win = probability(game[0], game[1], i)
	i += 1
	if win in eastfirst[0]:
		eastsecond.append([win])
	if win in eastfirst[1]:
		eastsecond[0].append(win)
	if win in eastfirst[2]:
		eastsecond.append([win])
	if win in eastfirst[3]:
		eastsecond[1].append(win)
westsecond = []
for game in westfirst:
	win = probability(game[0], game[1], i)
	i += 1
	if win in westfirst[0]:
		westsecond.append([win])
	if win in westfirst[1]:
		westsecond[0].append(win)
	if win in westfirst[2]:
		westsecond.append([win])
	if win in westfirst[3]:
		westsecond[1].append(win)
midwestsecond = []
for game in midwestfirst:
	win = probability(game[0], game[1], i)
	i += 1
	if win in midwestfirst[0]:
		midwestsecond.append([win])
	if win in midwestfirst[1]:
		midwestsecond[0].append(win)
	if win in midwestfirst[2]:
		midwestsecond.append([win])
	if win in midwestfirst[3]:
		midwestsecond[1].append(win)
southsecond = []
for game in southfirst:
	win = probability(game[0], game[1], i)
	i += 1
	if win in southfirst[0]:
		southsecond.append([win])
	if win in southfirst[1]:
		southsecond[0].append(win)
	if win in southfirst[2]:
		southsecond.append([win])
	if win in southfirst[3]:
		southsecond[1].append(win)

#SWEETSIXTEEN
eastthird = []
for game in eastsecond:
	win = probability(game[0], game[1], i)
	i += 1
	if win in eastsecond[0]:
		eastthird.append([win])
	if win in eastsecond[1]:
		eastthird[0].append(win)
westthird = []
for game in westsecond:
	win = probability(game[0], game[1], i)
	i += 1
	if win in westsecond[0]:
		westthird.append([win])
	if win in westsecond[1]:
		westthird[0].append(win)
midwestthird = []
for game in midwestsecond:
	win = probability(game[0], game[1], i)
	i += 1
	if win in midwestsecond[0]:
		midwestthird.append([win])
	if win in midwestsecond[1]:
		midwestthird[0].append(win)
souththird = []
for game in southsecond:
	win = probability(game[0], game[1], i)
	i += 1
	if win in southsecond[0]:
		souththird.append([win])
	if win in southsecond[1]:
		souththird[0].append(win)

#ELITEEIGHT
for game in eastthird:
	win = probability(game[0], game[1], i)
	i += 1
	eastwin = win
for game in westthird:
	win = probability(game[0], game[1], i)
	i += 1
	westwin = win
for game in midwestthird:
	win = probability(game[0], game[1], i)
	i += 1
	midwestwin = win
for game in souththird:
	win = probability(game[0], game[1], i)
	i += 1
	southwin = win

#FINALFOUR
finals1 = probability(eastwin, westwin, i)
i+=1
finals2 = probability(midwestwin, southwin, i)
i+=1
#CHAMPTIONSHIP
thewinner = probability(finals1, finals2, i)
print(thewinner)

#Output into tab delineated form. Best opened in excel.
with open(output, 'w') as f:
	f.write('FIRSTROUND:\t')
	for game in eastfirst:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in westfirst:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in midwestfirst:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in southfirst:
		for win in game:
			f.write(win)
			f.write('\t')
	f.write('\nSECONDROUND:\t')
	for game in eastsecond:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in westsecond:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in midwestsecond:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in southsecond:
		for win in game:
			f.write(win)
			f.write('\t')	
	f.write('\nTHIRDROUND:\t')
	for game in eastthird:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in westthird:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in midwestthird:
		for win in game:
			f.write(win)
			f.write('\t')
	for game in souththird:
		for win in game:
			f.write(win)
			f.write('\t')
	f.write('\nREGIONAL:\t')
	f.write(eastwin + '\t' + westwin + '\t' + midwestwin + '\t' + southwin+ '\n')
	f.write('FINALS_MATCHUP:\t')
	f.write(finals1 +'\t'+finals2 +'\n')
	f.write('WINNER:\t' + thewinner)




			
