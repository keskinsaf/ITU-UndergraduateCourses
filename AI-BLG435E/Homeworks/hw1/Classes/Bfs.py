from Classes import Search
from Classes import Queue

class Bfs(Search.Search):
    def __init__(self, state):
        Search.Search.__init__(self, state)
        self.queue  = Queue.Queue()
        self.queue.enqueue(state)

    def bfs(self):
        state = self.queue.dequeue()
        if state is None:
            return None
        self.path.append(state)
        # if there is an available move for a given state
        moves = self.ps_state_check(state)
        self.ext_cnt += 1
        if( len(moves) == 0 ):
            print("Final State!")
            return (state, self.queue, self.path)
        for move in moves:
            r = int(move[0])
            c = int(move[2])
            available_moves = moves[move]
            for a_move in available_moves:
                # push all available states into queue
                self.queue.enqueue( state.move_peg(r,c, int(a_move)) )
                self.gen_cnt += 1
        return self.bfs()
    
    def iterative_bfs(self):
        # version without emptying queue
        # while self.queue.is_ended() == False:
        # version with emptying queue
        while not self.queue.is_empty():
            state = self.queue.dequeue()
            self.path.append(state)
            moves = self.ps_state_check(state)
            self.ext_cnt += 1
            if( len(moves) == 0 ):
                print("Final State!")
                return (state, self.queue, self.path)
            for move in moves:
                r = int(move[0])
                c = int(move[2])
                available_moves = moves[move]
                for a_move in available_moves:
                    # push all available states into queue
                    self.queue.enqueue( state.move_peg(r,c, int(a_move)) )
                    self.gen_cnt += 1
        return None