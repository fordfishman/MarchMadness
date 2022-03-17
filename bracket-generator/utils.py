import numpy.random as ran
from itertools import chain


def file_import(teams_filename, rankings_filename,firstround_filename):

    # List to contain team names in order of original power ranking
    teams_list = []
    # Dict to contain power rankings in original order
    team_rank = {}

    # Imports team names
    with open(teams_filename, 'r') as teamfile:
        for team in teamfile:
            team = team.strip()
            teams_list.append(team)

    # Imports power rankings, and creates a dictionary entry for each team of form TeamName: Powerrank
    with open(rankings_filename, 'r') as rankingsfile:
        for index, rank in enumerate(rankingsfile):
            rank = float(rank.strip())
            team_rank[teams_list[index]] = rank
    
    matchups= []
    with open(firstround_filename, 'r') as firstround_file:
        for index, line in enumerate(firstround_file):
            game = line.split(' ')
            game[0] = game[0].strip()
            game[1] = game[1].strip()
            matchups.append(game)



    return teams_list, team_rank, matchups



def game(team1, team2, team_rank):
    """
    Takes the team power ranks of the matchup and converts it into form:
    r = 10^(PR/10)
    Where PR is the power rank, and r is new rank.
    New ranks are compared as either (rank2/rank1+rank2) or (rank1/rank1+rank2) (depending on which rank is higher)
    This determines probability of victory.  If (random number)/100 in case 1. is above probability, then team 1 wins. 
    If a team wins, its rating is increased.  If the winning team's power ranking was lower, it will raised according to how much lower it was.
    """
    rank1 = 10 ** (team_rank[team1]/10)
    rank2 = 10 ** (team_rank[team2]/10)
    if rank1 >= rank2:
        prob = (rank2/(rank1+rank2))
        if ran.uniform() > prob:
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
        if ran.uniform() > prob:
            winner = team2
            team_rank[team1] += 0.15
        else:
            winner = team1
            if ((team_rank[team2]-team_rank[team1]) > -1):
                team_rank[team2] += 0.25
            elif (team_rank[team2]-team_rank[team1]) > -1.5:
                team_rank[team2] += 0.5
            elif (team_rank[team2]-team_rank[team1]) > -3:
                team_rank[team2] += 1
            elif (team_rank[team2]-team_rank[team1]) > -5:
                team_rank[team2] += 1.5
            elif (team_rank[team2]-team_rank[team1]) > -7.5:
                team_rank[team2] += 2.0
            elif (team_rank[team2]-team_rank[team1]) > -10:
                team_rank[team2] += 3.0
            elif (team_rank[team2]-team_rank[team1]) > -15:
                team_rank[team2] += 4.0
    return winner, team_rank

def flatten(iterable):
    return list(chain.from_iterable(iterable))
