import numpy as np

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

    def set_other_side(self, other_side):
        self.other_side = other_side

    def initialize(self):
        initial_bin_count = NO_OF_MARBELS / NO_OF_BINS
        # store at the end so add 1 to NO_OF_BINS
        return np.array([initial_bin_count] * NO_OF_BINS), NO_OF_MARBELS


    # TODO : only happens if lies on own side?
    # This can occur after going around once  
    def check_capture(self, idx):
        '''
        Checks if the capture move can occur. If yes then it is executed.
        idx - index of last marbel place
        '''
        # if multiple marbels present in idx
        if (self.bins[idx] != 1): return False

        opposition_idx = (NO_OF_BINS-1) - idx
        # if marbels exits in opposition bin: capture them
        if self.other_side.bins[opposition_idx] > 0:
            # add marbels to own store
            self.bins[-1] += self.other_side.bins[opposition_idx] + self.bins[idx]
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
            return self.other_side.add_2_bins(0, no_of_marbels, player)
        # if no marbels left, then this was last marbel and player can go again
        else: 
            return True
    