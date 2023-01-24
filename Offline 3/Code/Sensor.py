import random
import numpy as np

class Sensor:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def get_adjacent(self, cur_pos):
        adj_cells = []
        i, j = cur_pos
        row, col = self.row, self.col
        ghost_detected = 0
        
        valid_cells = [(i, j)]
        # check left
        ############ check edge sharing
        # check left
        if (j!=0): valid_cells.append([i, j-1])
        # check right
        if (j!=col-1): valid_cells.append([i, j+1])
        # check up
        if (i!=0): valid_cells.append([i-1, j])
        # check down
        if (i!=row-1): valid_cells.append([i+1, j])

        ############ check corner sharing
        # check upper left
        if ((i!=0) and (j!=0)): valid_cells.append([i-1, j-1])
        # check upper right
        if ((i!=0) and(j!=col-1)): valid_cells.append([i-1, j+1])
        # check lower left
        if ((i!=row-1) and (j!=0)): valid_cells.append([i+1, j-1])
        # check lower right
        if ((i!=row-1) and (j!=col-1)): valid_cells.append([i+1, j+1])

        # for cell in valid_cells:
        #     if(cell[0] == cur_ghost_post[0]) and (cell[1] == cur_ghost_post[1]):
        #         ghost_detected = 1
        #         break
        # # introduce randomness
        # if np.random.random() > 0.85:
        #     ghost_detected = 1-ghost_detected
        return valid_cells
