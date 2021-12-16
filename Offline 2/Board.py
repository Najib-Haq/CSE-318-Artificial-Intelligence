import numpy as np
from Side import *

PLAYER_ONE = 0
PLAYER_TWO = 1

class Board:
    def __init__(self, side1=None, side2=None):
        # initialize board
        self.side1 = side1.copy() if side1 is not None else Side(PLAYER_ONE, None)
        self.side2 = side2.copy() if side2 is not None else Side(PLAYER_TWO, self.side1)
        self.side1.set_other_side(self.side2)
        self.sides = {
            PLAYER_ONE : self.side1,
            PLAYER_TWO : self.side2
        }

    def set_board(self, side1, side2):
        self.side1 = side1.copy()
        self.side2 = side2.copy()
        self.side1.other_side = self.side2
        self.side2.other_side = self.side1
        self.sides[PLAYER_ONE] = self.side1
        self.sides[PLAYER_TWO] = self.side2

    def get_board(self):
        return self.side1.copy(), self.side2.copy()

    # TODO: handle no marbels left on user side
    def select_bin(self, bin_idx, player):
        '''
        returns (valid_index, whether player can take turn again)
        '''
        side = self.sides[player]
        if bin_idx<0 or bin_idx>=NO_OF_BINS or side.bins[bin_idx] == 0:
            return False, True
        no_of_marbels = side.bins[bin_idx]
        side.bins[bin_idx] = 0
        side.playable_marbels -= no_of_marbels
        same_player_next = side.add_2_bins(bin_idx+1, no_of_marbels, player)
        # print("HERE ", side.other_side.bins)
        return True, same_player_next

    def check_if_empty(self):
        '''
        returns whether game is finished
        '''
        # if self.side1.playable_marbels == 0: winner = self.side2
        # elif self.side2.playable_marbels == 0: winner = self.side1
        if self.side1.bins.sum() == 0: winner = self.side2
        elif self.side2.bins.sum() == 0: winner = self.side1
        else: return False, None

        for marbels in winner.bins:
            winner.store += marbels
            winner.playable_marbels = 0
        # print("winner is player - ", winner.player)
        return True, winner.player

    def print(self):
        space = f"store {self.side2.store}"
        print(space, self.side2.bins[::-1])
        print(" "*len(space), self.side1.bins, "; store: ", self.side1.store)
    

if __name__ == '__main__':
    board = Board()
    player = 0
    print("PLAYER 2")
    print(board.side2.store, board.side2.bins[::-1])
    print("PLAYER 1")
    print(board.side1.bins, board.side1.store)
    
    while(not board.check_if_empty()):
        print("ENTER PLAYER ", player, ": ")
        idx = int(input())
        if(not board.select_bin(idx, player)):
            player = 1 - player
        print("PLAYER 2")
        print(board.side2.store, board.side2.bins[::-1])
        print("PLAYER 1")
        print(board.side1.bins, board.side1.store)
    
        print("#"*50)
        


    