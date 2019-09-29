import copy

class Board:
    possible_sizes = [ 3, 7, 11, 15, 19 ]
    def __init__(self,sob):
        self.board = self.init_board(sob) # size of board
    
    def init_board(self, sob):
        self.init_borders(sob)
        board = []
        board += self.init_rows( sob, self.fil_size, self.empty_size )
        board += self.init_rows( sob, self.fil_size )
        board += self.init_rows( sob, self.fil_size, self.empty_size )
        board[self.fil_size][self.fil_size] = 'o'
        return board
    
    def init_borders(self, sob ):
        if sob % 2 == 0:
            sob += 1
        if sob not in Board.possible_sizes:
            sob += 2
        
        self.fil_size   = ( sob - 1 ) // 2
        self.empty_size = (self.fil_size + 1 ) // 2
        self.sob        = sob

    # creates rows
    def init_rows(self, sob, fil, mis=0 ):
        rows = []
        for i in range(mis) if mis != 0 else range(fil):
            row = []
            for i in range( sob ):
                if mis != 0 and (i < mis or i >= mis + fil):
                    row.append(" ")
                else:
                    row.append(".")
            rows.append(row)
        return rows
    
    def print(self, board=None):
        def reduce_to_str(ls):
            def add_tabs(l):
                return l + "\t"
            row = ""
            for l in ls:
                row += add_tabs(l)
            return row

        if board is None:
            board = self.board
        for i in board:
            print( reduce_to_str(i) )
        print("\n\n")
    
    def get_board(self):
        return self.board

    def get_sob(self):
        return self.sob

    # whether indexes indicates board cell or not
    def in_board_check(self,rctr, cctr):
        # indexes should be within board indexes
        if rctr < 0 or rctr >= self.sob or cctr < 0 or cctr >= self.sob:
            return False
        if (rctr < self.empty_size or rctr >= self.empty_size + self.fil_size ) and (
            cctr < self.empty_size or cctr >= self.empty_size + self.fil_size):
            return False
        return True

    # whether there is a peg at given location or not
    def is_peg_check(self, rctr, cctr):
        return True if self.in_board_check(rctr,cctr) and self.board[rctr][cctr] == "." else False
    
    # whether there is a hole at given location or not
    def is_hole_check(self, rctr, cctr):
        return True if self.in_board_check(rctr,cctr) and self.board[rctr][cctr] == "o" else False

    # determine whether there is an available move for the peg at given index 
    # or not
    def is_move_check(self, rctr, cctr):
        def right_check(r, c):
            return "6" if self.in_board_check(r, c+1) and self.is_hole_check(r, c+1) else ""
        def left_check(r, c):
            return "4" if self.in_board_check(r, c-1) and self.is_hole_check(r, c-1) else ""
        def below_check(r, c):
            return "2" if self.in_board_check(r+1, c) and self.is_hole_check(r+1, c) else ""
        def above_check(r, c):
            return "8" if self.in_board_check(r-1, c) and self.is_hole_check(r-1, c) else ""
        
        result = ""
        # if there is a peg above
        if self.is_peg_check(rctr-1, cctr):
            result += above_check( rctr-1, cctr )
        # if there is a peg below
        if self.is_peg_check(rctr+1, cctr ):
            result += below_check( rctr+1, cctr )
        # if there is a peg at right
        if self.is_peg_check(rctr, cctr+1 ):
            result += right_check( rctr, cctr+1 )
        # if there is a peg at left
        if self.is_peg_check(rctr, cctr-1 ):
            result += left_check( rctr, cctr-1 )
        return result

    # take peg indexes and move direction, apply move in the given direction
    def move_peg(self, rctr, cctr, dir):
        new_state = copy.deepcopy(self)
        new_state.board[rctr][cctr] = "o"
        # print("dir: ",dir)
        if dir == 8:
            new_state.board[rctr-1][cctr] = "o"
            new_state.board[rctr-2][cctr] = "."
        elif dir == 2:
            new_state.board[rctr+1][cctr] = "o"
            new_state.board[rctr+2][cctr] = "."
        elif dir == 4:
            new_state.board[rctr][cctr-1] = "o"
            new_state.board[rctr][cctr-2] = "."
        elif dir == 6:
            new_state.board[rctr][cctr+1] = "o"
            new_state.board[rctr][cctr+2] = "."
        return new_state

    def count_pegs(self):
        peg_cnt = 0
        for row in self.board:
            for col in row:
                if col == '.':
                    peg_cnt += 1
        return peg_cnt
    
    def peg_indexes(self):
        peg_indexes = []
        r_ind = 0
        c_ind = 0
        while r_ind < self.sob:
            c_ind = 0
            while c_ind < self.sob:
                if  self.board[r_ind][c_ind] == '.':
                    peg_indexes.append( (r_ind, c_ind) )
                c_ind += 1
            r_ind += 1
        return peg_indexes
    
    def find_indexes_of(self, p):
        indexes = []
        r_ind   = 0
        c_ind   = 0
        while r_ind < self.sob:
            c_ind = 0
            while c_ind < self.sob:
                if  self.board[r_ind][c_ind] == p:
                    indexes.append( (r_ind, c_ind) )
                c_ind += 1
            r_ind += 1
        return indexes
    
    def count_of(self, ch):
        ch_cnt = 0
        for row in self.board:
            for col in row:
                if col == ch:
                    ch_cnt += 1
        return ch_cnt

if __name__ == "__main__":
    board = Board(7)
    board.print()