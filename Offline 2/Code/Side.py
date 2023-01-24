import numpy as np
import copy

NO_OF_BINS = 6
NO_OF_MARBELS = 24

class Side:
    def __init__(self, player, other_side):
        '''
        player - int (0/1) defining which player
        other_side - Side object of opposition player
        '''
        self.player = player
        self.other_side = other_side
        # the store is the end of the bins
        self.bins, self.playable_marbels = self.initialize()
        self.store = 0
        self.free_move = False
        self.has_captured = 0

    def copy(self):
        # dont copy other else no connection
        # other_side = self.other_side
        # if other_side is not None: other_side.bins = self.other_side.bins.copy()
        s = Side(self.player, self.other_side)
        s.bins = self.bins.copy()
        s.playable_marbels, s.store = copy.copy(self.playable_marbels), copy.copy(self.store)
        s.free_move, s.has_captured = copy.copy(self.free_move), copy.copy(self.has_captured)
        return s

    def set_other_side(self, other_side):
        self.other_side = other_side

    def initialize(self):
        initial_bin_count = NO_OF_MARBELS / NO_OF_BINS
        # store at the end so add 1 to NO_OF_BINS
        return np.array([initial_bin_count] * NO_OF_BINS), NO_OF_MARBELS

    def marbels_close_2_storage(self):
        count = 0
        for i in range(NO_OF_BINS):
            # only gets the count of stones which wouldnt overflow to opponent
            count += max(NO_OF_BINS-i, self.bins[i])
        return count

    def weighted_marbels(self):
        count = 0
        for i in range(NO_OF_BINS):
            # give more weight to the marbels on the left
            count += (NO_OF_BINS-i)*self.bins[i]
        return count

    # This can occur after going around once  
    def check_capture(self, idx, execute=True):
        '''
        Checks if the capture move can occur. If yes then it is executed.
        idx - index of last marbel place
        '''
        # if multiple marbels present in idx
        if (self.bins[idx] != 1): return False

        opposition_idx = (NO_OF_BINS-1) - idx
        # if marbels exits in opposition bin: capture them if execute=True
        if self.other_side.bins[opposition_idx] > 0:
            if not execute: return True
            # add marbels to own store
            self.store += self.other_side.bins[opposition_idx] + self.bins[idx]
            self.has_captured = self.other_side.bins[opposition_idx] # need for heuristic, how many captured
            # adjust playable marbels numbers
            self.playable_marbels -= self.bins[idx]
            self.other_side.playable_marbels -= self.other_side.bins[opposition_idx]
            self.bins[idx] = 0            
            self.other_side.bins[opposition_idx] = 0
            return True
        return False

    def add_2_bins(self, bin_idx, no_of_marbels, player):
        '''
        adds no_of_bins starting from bin_idx
        bin_idx - index of bin from where to deposite marbels
        no_of_marbels - total no of marbels to deposit
        player - current player

        returns whether current player can go again
        '''
        # initialize
        self.free_move = False
        self.has_captured = 0

        # counter clockwise move from bin_idx to store to opponenet side
        idx = bin_idx
        for idx in range(bin_idx, NO_OF_BINS): 
            self.bins[idx] += 1 # add one marbel to this bin
            self.playable_marbels += 1 # remember to remove marbels when 1st call
            no_of_marbels -= 1
            if(no_of_marbels == 0): 
                if player != self.player:
                    return False # no more marbels left
                else:
                    self.check_capture(idx)
                    break
            
        # send to store if marbels still left
        if player == self.player:
            if(no_of_marbels > 0): 
                self.store += 1
                no_of_marbels -= 1
            # else this turn is done
            else: 
                return False
        
        # send to opposition 1st bin if marbels still left
        if(no_of_marbels > 0):
           self.free_move = self.other_side.add_2_bins(0, no_of_marbels, player)
        # if no marbels left, then this was last marbel and player can go again
        else:
            self.free_move = True 
        return self.free_move

    def game_end(self):
        # return self.playable_marbels == 0
        return self.bins.sum() == 0 or self.other_side.bins.sum() == 0
