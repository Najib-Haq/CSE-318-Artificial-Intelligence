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

    # TODO : if both have 24, the one whose move caused the board to be 0 be the winner/loser? - check it out
    def check_if_empty(self):
        '''
        returns whether game is finished
        '''
        # if self.side1.playable_marbels == 0: winner = self.side2
        # elif self.side2.playable_marbels == 0: winner = self.side1
        if ((self.side1.bins.sum() == 0 or self.side2.bins.sum() == 0) or 
            (self.side1.store > NO_OF_MARBELS or  self.side2.store > NO_OF_MARBELS)):
            if self.side1.store >= self.side2.store: winner = self.side1
            else: winner = self.side2
        else: return False, None

        for marbels in winner.bins:
            winner.store += marbels
            winner.playable_marbels = 0
        # print("winner is player - ", winner.player)
        return True, winner.player

    def print(self):
        s2=str(int(self.side2.store)).rjust(2)
        s1=str(int(self.side1.store)).rjust(2)
        bins2=map(str, self.side2.bins[::-1].astype(int))
        a2, b2, c2, d2, e2, f2 = [s.rjust(2) for s in bins2]
        bins1=map(str, self.side1.bins.astype(int))
        a1, b1, c1, d1, e1, f1 = [s.rjust(2) for s in bins1]
        
        console_gui = f" Moves ->     5     4     3     2     1     0 \n" + \
                      f" Player 1 -----------------------------------------------\n" + \
                      f"         |   {a2} |  {b2} |  {c2} |  {d2} |  {e2} |  {f2} |         \n" + \
                      f"  {s2}     |------------------------------------|    {s1}     \n" + \
                      f"         |   {a1} |  {b1} |  {c1} |  {d1} |  {e1} |  {f1} |         \n" + \
                      f"---------------------------------------------- Player 0 \n" + \
                      f"              0     1     2     3     4     5  <- Moves"
                            
        print(console_gui)
        # space = f"store {self.side2.store}"
        # print(space, self.side2.bins[::-1])
        # print(" "*len(space), self.side1.bins, "; store: ", self.side1.store)


    ########## heuristics
    def heuristic1(self, player):
        # (stones_in_my_storage – stones_in_opponents_storage)
        return self.sides[player].store - self.sides[1-player].store 

    def heuristic2(self, player, W1, W2):
        # W1 * (stones_in_my_storage – stones_in_opponents_storage) + W2 * (stones_on_my_side - stones_on_opponents_side)
        val1 = self.sides[player].store - self.sides[1-player].store
        val2 = self.sides[player].bins.sum() - self.sides[1-player].bins.sum()
        return W1*val1 + W2*val2

    # considers whether a free move is available in this turn
    def heuristic3(self, player, W1, W2, W3):
        return self.heuristic2(player, W1, W2) + W3*self.sides[player].free_move

    # considers whether free moves can be generated from this position
    # def heuristic3(self, player, W1, W2, W3):
    #     free_move_available = False
    #     bins = self.sides[player].bins
    #     for i in range(NO_OF_BINS):
    #         marbel_count = bins[i]
    #         # if dist to store is equal to number of marbels in that bin than free move will be available
    #         dist_to_store = NO_OF_BINS - i
    #         if marbel_count == dist_to_store:
    #              free_move_available = True
    #              break
    #     return self.heuristic2(player, W1, W2) + W3*free_move_available

    # considers how many free moves generated so far
    # def heuristic3(self, player, W1, W2, W3, additional_moves):
    #     return self.heuristic2(player, W1, W2) + W3*additional_moves

    # my designs
    # considers whether a capture has occured
    def heuristic4(self, player, W1, W2, W3):
        return self.heuristic2(player, W1, W2) + W3*self.sides[player].has_captured

    # considers stones close to storage
    def heuristic5(self, player, W1, W2):
        close_stones1 = self.sides[player].marbels_close_2_storage()
        close_stones2 = self.sides[1-player].marbels_close_2_storage()
        return W1*self.heuristic1(player) + W2*(close_stones1 - close_stones2)

    # considering close to winning
    def heuristic6(self, player, W1, W2):
        winning1 = (NO_OF_MARBELS - self.sides[player].store)
        winning2 = (NO_OF_MARBELS - self.sides[1-player].store)

        close_stones1 = self.sides[player].marbels_close_2_storage()
        close_stones2 = self.sides[1-player].marbels_close_2_storage()
            
        return W1*(winning2 - winning1) + W2*(close_stones1 - close_stones2)





if __name__ == '__main__':
    board = Board()
    player = 0
    board.print()
    # print("PLAYER 2")
    # print(board.side2.store, board.side2.bins[::-1])
    # print("PLAYER 1")
    # print(board.side1.bins, board.side1.store)
    
    # while(not board.check_if_empty()):
    #     print("ENTER PLAYER ", player, ": ")
    #     idx = int(input())
    #     if(not board.select_bin(idx, player)):
    #         player = 1 - player
    #     print("PLAYER 2")
    #     print(board.side2.store, board.side2.bins[::-1])
    #     print("PLAYER 1")
    #     print(board.side1.bins, board.side1.store)
    
    #     print("#"*50)
        


    