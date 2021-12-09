import numpy as np
from numpy.lib.function_base import append
from queue import PriorityQueue
import os
import math

from Board import Board
from Node import Node


class Astar:
    def __init__(self, filename=''):
        self.size, self.init_board = self.take_input(filename)
        self.final_board = Board(self.init_board.size, self.init_board.gt_board)
        self.init_node = Node(
            board=self.init_board,
            n_moves=0,
            prev_node=None
        )
        self.pq, self.closed_list = None, None
        
    def take_input(self, filename):
        board = Board(filename=filename)

        return board.size, board

    def is_solvable(self):
        return self.init_board.solvable(verbose=True)
    
    def search_algo(self, method='manhattan'):
        print("Using Heuristic : ", method)
        self.init_node.heuristic = method
        self.pq = PriorityQueue()
        # print("Begin search")
        self.pq.put(self.init_node)
        
        self.closed_list = set()
        while(not self.pq.empty()):
            node = self.pq.get()
            # node.board.print()
            # self.closed_list.append(node)
            # node.print()

            # dequeued node is final state
            if(node.board == self.final_board): 
                print('# Expanded Nodes : ', len(self.closed_list))
                print('# Explored Nodes : ', len(self.pq.queue)+len(self.closed_list))
                return node
            
            self.closed_list.add(tuple(node.board.board.flatten()))
            next_nodes = node.get_next_nodes()
            # print(25*'#')
            for n_node in next_nodes:
                # print("SCORE : " , n_node.board.get_heuristic(method, n_node.n_moves))
                # n_node.board.print()
                if tuple(n_node.board.board.flatten()) not in self.closed_list:
                    self.pq.put(n_node)
            # print(25*'#')
        return None;

    def compare_heuristics(self, heuristics=['hamming', 'manhattan', 'linear']):
        print("COMPARING : ")
        for heuristic in heuristics:
            self.search_algo(heuristic)
            print()


def fill(input, size):
    if size<4:
        zfill=1
    elif size>=4 and size<10:
        zfill=2
    else:
        zfill=3
    if input == 0:
        return '*'*zfill
    return str(input).zfill(zfill)


def print_limited(path, step=0, total=9):
    reset = step
    for row in range(path[0].board.size):
        step = reset
        out = ""
        for i in range(len(path)):
            board = path[i].board.board
            out += "|\033[4m"
            for x in board[row]:
                out += fill(x, path[0].board.size) + "|"
            out += "\033[0m"
            step += 1
            if row != 1: 
                out += "      " #6 spaces
                if row==0 and (step!=total): out += str(step) + " "
                else: out +=  " "*(len(str(step)) + 1)
            elif step!=total:        out += " ---> " + " "*(len(str(step)) + 1)
        print(out)

def print_all(path):
    for i in range(math.ceil(len(path)/5)):
        print_limited(path[5*i: 5*i+5], step=5*i, total=len(path))
        print("\n")
    

def test_samples(folder='sample'):
    files = os.listdir(folder)
    import time
    for file in files[:8]:
        filename = f'sample/{file}'
        print("Using board in ", filename)
        astar = Astar(filename)
        print("Solvability : ", astar.is_solvable())
        start = time.time()
        path = astar.search_algo()
        end = time.time()
        print("TIME taken : ", end-start)
        actual_paths = [path]
        while(actual_paths[-1].prev_node is not None):
            actual_paths.append(actual_paths[-1].prev_node)
        path = actual_paths[::-1]
        # print()
        print_all(path)

        # comparing
        # astar.compare_heuristics()


if __name__ == '__main__':

    test_samples()

    # astar = Astar()
    # path = astar.search_algo()
    # # # show sequence
    # actual_paths = [path[-1]]
    # while(actual_paths[-1].prev_node is not None):
    #     actual_paths.append(actual_paths[-1].prev_node)
    # path = actual_paths[::-1]
    # print_all(path)
    

'''
samples
https://tristanpenman.com/demos/n-puzzle/
https://stackoverflow.com/questions/60747903/n-puzzle-problem-using-a-star-search-algorithm
18 steps: {1,4,0,5,2,8,7,6,3}
26 steps: {2,1,7,5,0,8,3,4,6}
27 steps: {8,5,3,4,7,0,6,1,2}
28 steps: {0,6,7,3,8,5,4,2,1}
30 steps: {5,7,0,4,6,8,1,2,3}
31 steps: {8,6,7,2,5,4,3,0,1}
'''
