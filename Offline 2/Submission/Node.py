import numpy as np

from Side import *
from Board import *

class Node:
    def __init__(self, player, board, move=-1, add_turn=0, heuristic=1, h_args=[], move_order=None):
        self.player = player
        self.board = board # player board
        self.side = self.board.sides[self.player] # get players own side
        self.value = None # prize value according to heuristic
        self.move = move # mode index -> the move which made this node
        self.additional_turn = add_turn # how many turns of same player
        self.successors = None
        self.heuristic = heuristic # get heuristic number
        self.heuristic_args = h_args # heuristic args
        self.move_order = move_order if move_order is not None else range(NO_OF_BINS)

    def set_heuristic(self, heuristic, h_args):
        self.heuristic = heuristic
        self.heuristic_args = h_args

    def get_heuristic(self, max_player):
        if self.heuristic == 1:
            return self.board.heuristic1(max_player)
        elif self.heuristic == 2:
            return self.board.heuristic2(max_player, self.heuristic_args[0], self.heuristic_args[1])
        elif self.heuristic == 3:
            return self.board.heuristic3(max_player, self.heuristic_args[0], self.heuristic_args[1], self.heuristic_args[2])
        elif self.heuristic == 4:
            return self.board.heuristic4(max_player, self.heuristic_args[0], self.heuristic_args[1], self.heuristic_args[2])
        elif self.heuristic == 5:
            return self.board.heuristic5(max_player, self.heuristic_args[0], self.heuristic_args[1], self.heuristic_args[2])
        elif self.heuristic == 6:
            return self.board.heuristic6(max_player, self.heuristic_args[0], self.heuristic_args[1], self.heuristic_args[2])


    def game_end(self):
        return self.side.game_end()

    def gen_successors(self):
        nodes = []
        # select which bin to select
        old_board = self.board.get_board()
        for idx in self.move_order:
            valid_idx, same_player_turn = self.board.select_bin(idx, self.player)
            # if bin in this index is empty; continue
            if not valid_idx:
                continue
            add_turn = self.additional_turn + 1 if same_player_turn else 0 # keep track of turn
            next_board = Board(self.board.side1, self.board.side2)
            next_node = Node(
                self.player if same_player_turn else 1-self.player,
                next_board,
                idx, 
                add_turn,
                self.heuristic,
                self.heuristic_args,
                self.move_order
            )
            nodes.append(next_node) 
            self.board.set_board(old_board[0], old_board[1])# get prev board
            # print("RESTORE : ")
            # self.board.print()
            # print("DONE")
        # if nodes == []: print("HERE", "#"*100)
        self.successors = nodes
        return nodes

def get_tree(start_node, depth=10):
    level_successors = start_node.gen_successors()
    for i in range(1, depth):
        next_level_successors = []
        for node in level_successors:
            next_nodes = node.gen_successors()
            next_level_successors += next_nodes
        level_successors = next_level_successors
    return start_node

def print_tree(start_node, level=3):
    # level = 0
    successors = start_node.successors
    for lvl in range(level):
        next_successors = []
        print("IN LEVEL : ", lvl)
        for idx in range(len(successors)):
            # if lvl == (level-1): print(f"level {lvl} node no {idx}")
            successors[idx].board.print()
            if successors[idx].successors is not None: next_successors += successors[idx].successors
        successors = next_successors


if __name__ == "__main__":
    n = Node(0, Board())
    # print("Original : ")
    # print(n.board.print())
    # print(n.set_heuristic(1, [100, 200]))
    # nodes = n.gen_successors()
    # for idx in range(len(nodes)):
    #     print(idx)
    #     nodes[idx].board.print()

    # test tree
    node = get_tree(n, depth=2)
    print_tree(node, 2)



