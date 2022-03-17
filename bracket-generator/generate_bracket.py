#!/usr/bin/env python
## Ford Fishman

from Region import Region
from utils import file_import, game, flatten
import pandas as pd

def output(path, regions, w1, w2, wf):

    data = dict()

    for name, region in regions.items():

        data['{}firstround'.format(name)] = flatten(region.second_round)
        data['{}secondround '.format(name)] = flatten(region.third_round)
        data['{}sweet16'.format(name)] = region.fourth_round
        data['{}elite8 winner'.format(name)] = [region.winner]
    
    data['final4winners'] = [ w1, w2 ]
    data['overallwinner'] = [ wf ]

    return pd.DataFrame({key:pd.Series(value) for key, value in data.items()})



def main():
    teams_list, team_rank, matchups = file_import('2022/team_names.txt', '2022/power_rankings.txt', '2022/firstround.txt')

    regions = {
        'west': Region(matchups[0:8]),
        'south': Region(matchups[8:16]),
        'east': Region(matchups[16:24]),
        'midwest': Region(matchups[24:32])    
    }

    for region in regions.values():

        team_rank = region.r64(team_rank)
        team_rank = region.r32(team_rank)
        team_rank = region.s16(team_rank)
        team_rank = region.e8(team_rank)
        # region.results()
    
    # final four
    win1, team_rank = game(regions['east'].winner, regions['west'].winner, team_rank)
    win2, team_rank = game(regions['south'].winner, regions['midwest'].winner, team_rank)

    final_winner, team_rank = game(win1, win2, team_rank)
    df = output('2021/randombracket.csv', regions, win1, win2, final_winner)
    return (final_winner, df)