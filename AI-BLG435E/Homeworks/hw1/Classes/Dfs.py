from Classes import Stack
from Classes import Search

class Dfs(Search.Search):
    def __init__(self, state):
        Search.Search.__init__(self, state)
        self.stack = Stack.Stack()
        self.stack.push(state)

    def dfs(self):
        state = self.stack.pop()
        self.path.append(state)
        # if there is an available move for a given state
        moves = self.ps_state_check(state)
        self.ext_cnt += 1
        if( len(moves) == 0 ):
            print("Final State!")
            return (state, self.stack, self.path)
        for move in moves:
            r = int(move[0])
            c = int(move[2])
            available_moves = moves[move]
            for a_move in available_moves:
                # push all available states into stack
                self.stack.push( state.move_peg(r,c, int(a_move)) )
                self.gen_cnt += 1
        return self.dfs()