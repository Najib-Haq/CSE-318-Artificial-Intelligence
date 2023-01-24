import random
import numpy as np

class Ghost:
    def __init__(self, grid):
        '''
        grid -> grid from Grid object
        '''
        self.all_moves = self.find_all_moves(grid)
        self.all_prev_moves = self.find_all_prev_moves()

    def find_all_moves(self, grid):
        '''
        return [index] : [(index0, index1, prob), (index0, index1, prob), ...]
        '''
        row, col = grid.shape
        all_moves = {}
        for i in range(row):
            for j in range(col):
                edge_sharing_moves = []
                corner_sharing_moves = []
                # only consider if not an obstacle
                if(grid[i][j] != 0):
                    ############ check edge sharing
                    # check left
                    if (j!=0) and (grid[i][j-1] != 0): edge_sharing_moves.append([i, j-1])
                    # check right
                    if (j!=col-1) and (grid[i][j+1] != 0): edge_sharing_moves.append([i, j+1])
                    # check up
                    if (i!=0) and (grid[i-1][j] != 0): edge_sharing_moves.append([i-1, j])
                    # check down
                    if (i!=row-1) and (grid[i+1][j] != 0): edge_sharing_moves.append([i+1, j])

                    ############ check corner sharing
                    # check self
                    corner_sharing_moves.append([i, j])
                    # check upper left
                    if ((i!=0) and (j!=0)) and (grid[i-1][j-1] != 0): corner_sharing_moves.append([i-1, j-1])
                    # check upper right
                    if ((i!=0) and(j!=col-1)) and (grid[i-1][j+1] != 0): corner_sharing_moves.append([i-1, j+1])
                    # check lower left
                    if ((i!=row-1) and (j!=0)) and (grid[i+1][j-1] != 0): corner_sharing_moves.append([i+1, j-1])
                    # check lower right
                    if ((i!=row-1) and (j!=col-1)) and (grid[i+1][j+1] != 0): corner_sharing_moves.append([i+1, j+1])

                    # add probabilities to indexes
                    all_edge_moves = len(edge_sharing_moves)
                    all_edge_moves_prob = 0.9 / all_edge_moves  if all_edge_moves else 0

                    all_corner_moves = len(corner_sharing_moves)
                    all_corner_moves_prob = 0.1 / all_corner_moves if all_edge_moves else 1 / all_corner_moves

                    for l in edge_sharing_moves: l.append(all_edge_moves_prob) 
                    for l in corner_sharing_moves: l.append(all_corner_moves_prob)

                    all_moves[(i, j)] = edge_sharing_moves + corner_sharing_moves
        return all_moves

    def find_all_prev_moves(self):
        '''
        return [index] : [(index0, index1, prob), (index0, index1, prob), ...]
        '''
        all_prev_moves = {}
        for from_move in self.all_moves.keys():
            for to_data in self.all_moves[from_move]:
                from_data = [from_move[0], from_move[1], to_data[2]]
                to_move = tuple(to_data[:2]) # extract index
                if tuple(to_move) in all_prev_moves.keys():
                    all_prev_moves[to_move].append(from_data)
                else:
                    all_prev_moves[to_move] = [from_data]
        return all_prev_moves