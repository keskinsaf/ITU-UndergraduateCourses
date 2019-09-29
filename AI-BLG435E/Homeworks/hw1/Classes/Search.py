class Search:
    def __init__(self, state):
        self.path   = []
        self.gen_cnt = 0
        self.ext_cnt = 0
    
    # Peg solitare state check function that will check whether its final state
    #  or not. Here, "state" is a Board object
    def ps_state_check(self, state ):
        # for each peg, available move will be checked.
        # 2 indicates it can jump over the peg below it
        # 4 indicates it can jump over the peg left to it
        # 6 indicates it can jump over the peg right to it
        # 8 indicates it can jump over the peg above it
        # no available move for peg in that cell
        moves = {}
        for r in range( state.get_sob() ):
            for c in range( state.get_sob() ):
                if state.is_peg_check(r, c):
                    move = state.is_move_check(r, c)
                    # if there is an available move
                    if len(move) > 0:
                        moves[ str(r) + ":" + str(c) ] = move
        return moves
    
    def get_ext_cnt(self):
        return self.ext_cnt
    
    def get_gen_cnt(self):
        return self.gen_cnt