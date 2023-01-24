import numpy as np
from Board import Board

class Node:
    def __init__(self, board, n_moves=0, prev_node=None, heuristic="manhattan"):
        self.board = board
        self.n_moves = n_moves
        self.prev_node = prev_node
        self.heuristic = heuristic

    def __lt__(self, other):
        this_h = self.board.get_heuristic(self.heuristic, self.n_moves)
        other_h = other.board.get_heuristic(self.heuristic, other.n_moves)
        # tie breaker
        if this_h == other_h:
            this_h -= self.n_moves
            other_h -= other.n_moves
        return  this_h < other_h 
            
    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def print(self):
        print("Current Board: ")
        self.board.print()
        print("N_Moves: ", self.n_moves)
        print("Previous Node: ")
        if self.prev_node is None:
            print("None")
        else:
            self.prev_node.print()

    def get_next_boards(self):
        idx = self.board.find_blank()
        compare = True if self.prev_node is not None else False
        next_idxes = self.board.valid_moves(idx)
        current_cell = self.board.board[idx]
        next_boards = []
        for replace_idx in next_idxes:
            replace_cell = self.board.board[replace_idx]
            next_bd = Board(self.board.size, self.board.board, final_state=(self.board.idxes, self.board.gt_board, self.board.limit))
            # replace
            next_bd.board[idx] = replace_cell
            next_bd.board[replace_idx] = current_cell
            
            if(compare and self.prev_node is not None and (next_bd == self.prev_node.board)): continue # dont need this as already traversed
            next_boards.append(next_bd)
        return next_boards

    def get_next_nodes(self):
        next_boards = self.get_next_boards()
        return [Node(new_bd, self.n_moves+1, self, heuristic=self.heuristic) for new_bd in next_boards]


if __name__ == "__main__":
    node = Node(
        board=Board(
            size=3,
            board=np.array([
                [8, 1, 3], [4, 2, 0], [7, 6, 5]
            ])
        ),
        n_moves=1,
        prev_node=Node(
            board=Board(
                size=3,
                board=np.array([
                    [8, 1, 3], [4, 0, 2], [7, 6, 5]
                ])
            ),
            n_moves=0,
            prev_node=None
        )
    )


    node = Node(
        board=Board(
            size=3,
            board=np.array([
                [1, 3, 5], [4, 2, 6], [7, 8, 0]
            ])
        ),
        n_moves=1,
        prev_node=None
    )

    node.print()
    next_bd = node.get_next_boards()
    node.board.print()
    [bd.print() for bd in next_bd]
