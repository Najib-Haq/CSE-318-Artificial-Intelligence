import numpy as np

class Board:
    def __init__(self, size=3, board=None, filename='', final_state=None):
        self.size = size
        self.board = board.copy() if board is not None else None
        if self.board is None:
            self.create_board(filename)
        # dont want to calculate this continuously as final state same across a single problem
        # limit is the left limit and right limit of masks for linear conflict
        self.idxes, self.gt_board, self.limit = self.get_final_state() if final_state is None else final_state
        self.zero_position = self.find_blank() # finds zero position
        
    def __eq__(self, other):
        if(self.board is None) and (other.board is None): return True
        if(self.board is None) or (other.board is None): return False
        # np.any tests if any element is True or > 0 -> then not equal
        return not np.any(self.board - other.board)

    def get_final_state(self):
        # correct GT indexes
        idxes = {}
        gt_board = np.zeros(shape=(self.size, self.size), dtype=int)
        number = 1
        for i in range(self.size):
            for j in range(self.size):
                if(i==(self.size-1) and j==(self.size-1)): number=0
                idxes[number] = [i, j]
                gt_board[i][j] = number
                number += 1
        # get mask for linear conflict
        limit = self.get_mask_linear()
        return idxes, gt_board, limit

    def create_board(self, filename='sample.txt'):
        board = []
        if filename=='':
            print("Input board size : ")
            self.size = int(input())
            print("Input your board row by row : ")
            for i in range(self.size):
                row = list(map(int, input().replace('*', '0').split(" ")))
                board.append(row)
        else:
            with open(filename, 'r') as f:
                self.size = int(f.readline())
                for i in range(self.size):
                    row = list(map(int, f.readline().replace('*', '0').split(" ")))
                    board.append(row)
        self.board = np.array(board)
        # self.idxes, self.gt_board, self.limit = self.get_final_state()

    def print(self, underline=True):
        # print(self.board)
        # out = ""
        for i in range(self.size):
            out = "|"
            for j in range(self.size):
                out += str(self.board[i][j]) + "|"
            # out += "\33[0m"
            if underline: print("\033[4m" + out + "\033[0m")
            else: print(out)
        print()

    def find_blank(self):
        # return (row, col) idx of 0. output is a list of list so need to get the first element
        return list(zip(*np.where(self.board == 0)))[0]

    def valid_idx(self, idx):
        # checks if idx is valid
        if(idx[0]>=self.size or idx[0]<0): return False
        if(idx[1]>=self.size or idx[1]<0): return False
        return True

    def valid_moves(self, idx):
        '''
        idx is position of 0. 
        This func returns valid indexes of next moves of 0        
        '''
        moves = [
            (-1, 0), #up
            (+1, 0), #down
            (0, +1), #right
            (0, -1), #left
        ]
        next_move_boards = []
        new_idxes = []
        for mv in moves:
            new_idx = (idx[0] + mv[0], idx[1] + mv[1])
            if self.valid_idx(new_idx):
                new_idxes.append(new_idx)
        return new_idxes

    def get_mask_linear(self):
        '''
        returns comparison mask for linear conflict
        e.g. 
        board : 1, 2, 3 => left limit : 1 and right limit : 3 
                4, 5, 6                 4                   6
                7, 8, 0                 7                   9
        '''
        # get mask
        left_limit = []
        right_limit = []
        for i in range(1, (self.size*self.size)+1, self.size):
            left_limit.append(i)
            right_limit.append(i+self.size-1)
        left_limit = np.array([left_limit]).T # need column vector for proper vectorization
        right_limit = np.array([right_limit]).T
        return (left_limit, right_limit)

    def hamming_distance(self, verbose=False):
        compared = (self.gt_board != self.board)
        compared[-1][-1] = False # dont count blank
        if verbose: print(compared, "\nHamming Distance: ", compared.sum())
        return compared.sum()

    def manhattan_distance(self, verbose=False):
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                num = self.board[i][j]
                if(num == 0): continue # dont consider blank
                i_gt, j_gt = self.idxes[num]
                if verbose: print("Number: ", num, " row dist: ", abs(i-i_gt), " col dist: ", abs(j-j_gt))
                distance += abs(i-i_gt) + abs(j-j_gt)
        if verbose: print("Manhattan Distance: ", distance)
        return distance

    def linear_conflict_vectorized(self, verbose=False):
        '''
        only considers row linear conflicts
        the conditions are :
            1) both tiles in target row and col. -> Values that should be considered are extracted through mask
            2) they must pass over each other. Meaning the larger value is in the front. 
        '''
        # extract the positions to be considered through mask. limit[0] is left limit, limit[1] is right limit
        mask = (self.board >= self.limit[0]) & (self.board <= self.limit[1])
        # no need to continue if first condition is false
        if int(mask.sum()) == 0: return 0

        conflicts = np.zeros(shape=mask.shape)
        # make values which shouldn't be considered larger than n. This will ensure they return 0 on comparison later
        masked_board = (self.board*mask) + (self.size**2)*(1-mask) 
        # print(masked_board)
        for col1 in range(self.size):
            for col2 in range(col1, self.size):
                # add all conflicts of col1 to its position
                conflicts[:, col1] += (masked_board[:, col1] > masked_board[:, col2])
        # get rid of the larger than n values which shouldnt be considered. (any better way?)
        conflicts *= mask
        if verbose: print("Final consideration: ", conflicts)
        if verbose: print("#Linear Conflicts : ", conflicts.sum())
        return 2*conflicts.sum()

    def get_heuristic(self, name, n_moves):
        # print("Using heurisitc : ", name)
        if(name.upper() == "HAMMING"): return self.hamming_distance() + n_moves
        if(name.upper() == "MANHATTAN"): return self.manhattan_distance() + n_moves
        if(name.upper() == "LINEAR"): return self.manhattan_distance() + self.linear_conflict_vectorized() + n_moves

    def count_inversions(self, verbose=False):
        seen_list = []
        count = 0
        if verbose: list_inversions = {k:0 for k in range(2, self.size*self.size)}

        for i in range(self.size):
            for j in range(self.size):
                num = self.board[i][j]
                if num==0: continue
                for k in seen_list:
                    if k>num:
                        if verbose: list_inversions[k] += 1
                        count += 1
                seen_list.append(num)
        if verbose: print(list_inversions)
        return count

    def solvable(self, verbose=False):
        # case: size is even
        if self.size%2 == 0:
            # get blank position row
            blank_pos = self.find_blank()[0]
            # blank is on even row from bottom
            if((self.size - blank_pos)%2 == 0):
                # if inversions is odd
                if self.count_inversions()%2 == 1:
                    if verbose: print("Case k even: Blank is on even row from bottom; #inversion is odd")
                    return True
            # blank is on odd row from bottom
            else:
                # if inversions is even
                if self.count_inversions()%2 == 0:
                    if verbose: print("Case k even: Blank is on odd row from bottom; #inversion is even")
                    return True
        # case: size is odd
        else:
            if self.count_inversions()%2 == 0:
                if verbose: print("Case k odd: #Inversion is even")
                return True
    
        return False

if __name__ == "__main__":
    temp = np.array([
        [7, 2, 4], [6, 0, 5], [8, 3, 1]
    ])
    
    board = Board(board=temp)
    # board.create_board()
    board.print()
    board.find_blank()
    board.hamming_distance(verbose=True)
    board.manhattan_distance(verbose=True)
    # board.linear_conflict(verbose=True)
    board.linear_conflict_vectorized(verbose=True)

    temp[0][0], temp[0][1] = temp[0][1], temp[0][0]
    board2 = Board(board=temp)
    # board2.create_board()
    board2.print()

    print(board == board2)

    # temp = np.array([
    #     [8, 1, 2], [0, 4, 3], [7, 6, 5]
    # ])
    # temp = np.array([
    #     [1, 3, 2], [7, 8, 6], [4, 5, 0]
    # ])
    temp = np.array([
        [9, 1, 10, 5], [14, 8, 13, 3], [2, 6, 12, 0], [15, 4, 11, 7]
    ])
    b = Board(size=4, board=temp)
    b.print()
    print("Inversions : ", b.count_inversions(verbose=True))
    print("Solvability : ", b.solvable())

    temp = np.array([
        [3, 2, 1], [6, 0, 5], [4, 7, 8]
    ])
    board = Board(board=temp)
    board.linear_conflict_vectorized(verbose=True)