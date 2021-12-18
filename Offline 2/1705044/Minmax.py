import numpy as np

from Node import *
from Board import *

# count = 0

def minmax(node, max_player, depth, alpha=None, beta=None):
    # if leaf mode
    if node.game_end() or depth==0:
        # global count
        # count += 1
        node.value = node.get_heuristic(max_player)
        # print(node.value)
        return node.value

    child_nodes = node.gen_successors()
    # print(child_nodes)
        
    # max is playing
    if node.player == max_player:
        best_val = -np.inf # -infinity
        for child in child_nodes:
            val = minmax(child, max_player, depth-1, alpha, beta)
            best_val = max(best_val, val)
            # if depth == 1: print("max in ", depth, " : ", best_val, val)
            # if alpha-beta pruning
            if alpha is not None and beta is not None:
                alpha = max(best_val, alpha)
                # prune
                if alpha >= beta:
                    break
    
    # if min is playing
    else:
        best_val = np.inf # infinity
        for child in child_nodes:
            val = minmax(child, max_player, depth-1, alpha, beta)
            best_val = min(best_val, val)
            # print("min", best_val, val)
            # if alpha-beta pruning
            if alpha is not None and beta is not None:
                beta = min(best_val, beta)
                # prune
                if alpha >= beta:
                    break

    node.value = best_val
    return best_val

def print_tree(start_node, level=3):
    # level = 0
    successors = start_node.successors
    for lvl in range(level):
        next_successors = []
        print("IN LEVEL : ", lvl)
        if lvl == (level-1): print("Total nodes : ", len(successors)) ; #break
        # print(f"Level {lvl} Max : ", max(ch.value for ch in successors))
        # print(f"Level {lvl} Min : ", min(ch.value for ch in successors))
        for idx in range(len(successors)):
            # if lvl == (level-1): print("h val : ", successors[idx].value)
            # print(f"level {lvl} node no {idx}")
            # successors[idx].board.print()
            if successors[idx].successors is not None: next_successors += successors[idx].successors
        successors = next_successors

if __name__ == "__main__":
    n = Node(0, Board())
    print(minmax(n, 0, 2, -np.inf, np.inf))
    print(n.value)
    print_tree(n, 2)

    # print(count)