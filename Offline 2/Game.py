import numpy as np

from Board import *
from Node import *
from Minmax import *

class Game:
    def __init__(self, player_media, first_move):
        self.board = Board()
        self.player_media = player_media # pc or human
        self.player = 0 if first_move else 1
        self.pc_heuristic = None
        self.player_heuristic = None
        self.pc_hr_args = []
        self.player_hr_args = []
        self.additional_args = {}

    def set_heuristic(self, pc_hr, pc_hr_args, player_hr=None, player_hr_args=None, depth=3):
        self.pc_heuristic = pc_hr
        self.player_heuristic = player_hr
        self.pc_hr_args = pc_hr_args
        self.player_hr_args = player_hr_args
        self.additional_args['depth'] = depth

    def get_next_move(self, player):
        n = Node(player, self.board, -1, 0,
                 self.player_heuristic if player == self.player else self.pc_heuristic,
                 self.player_hr_args if player == self.player else self.pc_hr_args
        )
        max_val = minmax(n, self.additional_args['depth'], -np.inf, np.inf)
        if(n.successors is None):
            print("Problem with:")
            n.board.print()
            return -1
        else:
            for child in n.successors:
                if child.value == max_val:
                    return child.move

    def game_play_human(self):
        turn = 0
        while(True):
            if turn == self.player: 
                print("PLAYER ", turn, " ENTER MOVE: ")
                idx = int(input())
            else:
                idx = self.get_next_move(turn)
                print("PLAYER ", turn, " move : ", idx)
            valid_idx, same_turn = self.board.select_bin(idx, turn)
            if not valid_idx: print("Please enter valid index")
            turn = 1 - turn if not same_turn else turn
            self.board.print()
            print("#"*50)
            finish, winner = self.board.check_if_empty()
            print("FINISH : ", finish)
            if finish: break
        print("WINNER IS ", winner)
        return winner

    def game_play_pc(self):
        turn = 0
        while(True):
            idx = self.get_next_move(turn)
            print("PLAYER ", turn, " move : ", idx)
            if(not self.board.select_bin(idx, turn)[1]):
                turn = 1 - turn
            self.board.print()
            print("#"*50)
            print(self.board.side1.playable_marbels, self.board.side2.playable_marbels)
            finish, winner = self.board.check_if_empty()
            print("FINISH : ", finish)
            if finish: break
        print("WINNER IS ", winner)
        return winner

    def game(self):
        if self.player_media == "pc":
            return self.game_play_pc()
        if self.player_media == "human":
            return self.game_play_human()


if __name__ == "__main__":
    g = Game("pc", True)
    g.set_heuristic(1, [], 1, [])
    g.game()

    