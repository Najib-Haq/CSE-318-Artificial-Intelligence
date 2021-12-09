import numpy as np
from Side import Side

class Board:
    def __init__(self):
        PlAYER_ONE = 0
        PLAYER_TWO = 1
        # initialize board
        self.side1 = Side(PlAYER_ONE, None)
        self.side2 = Side(PLAYER_TWO, self.side1)
        self.side1.set_other_side(self.side2)

    # TODO: handle no marbels left on user side
    def select_bin(self, bin_idx, player):
        '''
        returns whether player can take turn again
        '''
        if player == 0: side = self.side1
        elif player == 1: side = self.side2

        no_of_marbels = side.bins[bin_idx]
        side.bins[bin_idx] = 0
        side.playable_marbels -= no_of_marbels
        return side.add_2_bins(bin_idx+1, no_of_marbels, player)

    def check_if_empty(self):
        '''
        returns whether game is finished
        '''
        if self.side1.playable_marbels == 0: winner = self.side2;
        elif self.side2.playable_marbels == 0: winner = self.side1
        else: return False

        for marbels in winner.bins:
            winner.store += marbels
            winner.playable_marbels = 0
        print("winner is playe - ", winner.player+1)
        return True



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
        


    