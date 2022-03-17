from utils import game

class Region():

    def __init__(self, matchups) -> None:
        self.first_round = matchups
        self.second_round = [ [] for i in range(4) ]
        self.third_round = [ [] for i in range(2) ]
        self.fourth_round = [ ]
        self.winner = None
    
    def r64(self, team_ranks) -> None:

        for i, match in enumerate(self.first_round):

            win, team_ranks = game(match[0], match[1], team_ranks)

            self.second_round[i//2].append(win)

        return team_ranks

    def r32(self, team_ranks) -> None:

        for i, match in enumerate(self.second_round):

            win, team_ranks = game(match[0], match[1], team_ranks)

            self.third_round[i//2].append(win)

        return team_ranks
    
    def s16(self, team_ranks) -> None:

        for i, match in enumerate(self.third_round):

            win, team_ranks = game(match[0], match[1], team_ranks)

            self.fourth_round.append(win)

        return team_ranks
    
    def e8(self, team_ranks) -> None:

        win, team_ranks = game(self.fourth_round[0], self.fourth_round[1], team_ranks)

        self.winner = win

        return team_ranks
    
    def results(self):
        print(self.first_round)
        print(self.second_round)
        print(self.third_round)
        print(self.fourth_round)
        print(self.winner)