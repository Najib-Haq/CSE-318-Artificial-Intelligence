import numpy as np
from numpy.lib.function_base import append
# from queue import PriorityQueue
import heapq
import os
import math, time

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
        self.pq, self.closed_list = [], None
        
    def take_input(self, filename):
        board = Board(filename=filename)
        return board.size, board

    def is_solvable(self):
        return self.init_board.solvable(verbose=True)
    
    def search_algo(self, method='manhattan'):
        print("Using Heuristic : ", method)
        self.init_node.heuristic = method
        self.pq = []
        # print("Begin search")
        self.pq.append(self.init_node)
        
        self.closed_list = set()
        heapq.heapify(self.pq)
        while(len(self.pq)):
            node = heapq.heappop(self.pq)
            # print(node.board.get_heuristic(node.heuristic, node.n_moves)-node.n_moves) #check value
            # node.board.print()

            # dequeued node is final state
            if(node.board == self.final_board): 
                print('# Expanded Nodes : ', len(self.closed_list))
                print('# Explored Nodes : ', len(self.pq)+len(self.closed_list)+1)
                return node
            
            self.closed_list.add(tuple(node.board.board.flatten()))
            next_nodes = node.get_next_nodes()
            # print(25*'#')
            for n_node in next_nodes:
                # print("SCORE : " , n_node.board.get_heuristic(method, n_node.n_moves))
                # n_node.board.print()
                if tuple(n_node.board.board.flatten()) not in self.closed_list:
                    heapq.heappush(self.pq, n_node)
                    # self.pq.append(n_node)
            # print(25*'#')
        return None;

    def compare_heuristics(self, heuristics=['hamming', 'manhattan', 'linear'], print_path=False):
        print("COMPARING : ")
        for heuristic in heuristics:
            start = time.time()
            path = self.search_algo(heuristic)
            print("TIME taken : ", time.time()-start)
            if heuristic==heuristics[-1] and print_path: print_all(path)
            print()

### HELPER FUNCTIONS

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

def print_limited(path, step=0, total=9, underline=True):
    reset = step
    for row in range(path[0].board.size):
        step = reset
        out = ""
        for i in range(len(path)):
            board = path[i].board.board
            if underline: out += "|\033[4m"
            else: out += "|"
            for x in board[row]:
                out += fill(x, path[0].board.size) + "|"
            if underline: out += "\033[0m"
            step += 1
            if row != 1: 
                out += "      " #6 spaces
                if row==0 and (step!=total): out += str(step) + " "
                else: out +=  " "*(len(str(step)) + 1)
            elif step!=total:        out += " ---> " + " "*(len(str(step)) + 1)
        print(out)

def print_all(path):
    actual_paths = [path]
    while(actual_paths[-1].prev_node is not None):
        actual_paths.append(actual_paths[-1].prev_node)
    path = actual_paths[::-1]
    print("COST : ", len(path)-1)
    for i in range(math.ceil(len(path)/5)):
        print_limited(path[5*i: 5*i+5], step=5*i, total=len(path))
        print("\n")

def test_file(filename, solve=True, compare=True):
    print("#"*10, " Using board in ", filename)
    astar = Astar(filename)
    solvable = astar.is_solvable()
    print("Solvability : ", solvable)
    if solvable:
        if solve:
            start = time.time()
            path = astar.search_algo(method='manhattan')
            end = time.time()
            print("TIME taken : ", end-start)
            print_all(path)
        if compare:
            astar.compare_heuristics(print_path=not solve)

def test_samples(folder='sample', solve=True, compare=True):
    files = os.listdir(folder)
    import time
    for file in files[:8]:
        filename = f'sample/{file}'
        test_file(filename, solve, compare)

if __name__ == '__main__':
    # test_samples(solve=True, compare=False)
    FILENAME = "sample/sample8.txt"
    test_file(FILENAME, solve=False, compare=True)


    
