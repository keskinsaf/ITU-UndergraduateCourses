from Classes import PrioQueue
from Classes import Search

def h1(queue):
    return sorted(queue, key=hole_distance, reverse=True)

def h2(queue):
    return sorted(queue,key=peg_distance)

def hole_distance(state):
    hole_list    = state.find_indexes_of('o')
    # print("len of peg_list: ", len(peg_list))
    hole_cnt     = state.count_of('o')
    if hole_cnt == 1 or hole_cnt == 0:
        print("only 1 hole")
        return 0
    def one_distance(p1, p2):
        return pow(p1[0]-p2[0], 2) + pow( p1[1]-p2[1], 2 )
    
    total_distance = 0
    r_cnt = 0
    h_length = len(hole_list)
    while r_cnt < h_length - 1:
        c_cnt = r_cnt + 1
        while c_cnt < h_length:
            total_distance += one_distance( hole_list[r_cnt], hole_list[c_cnt] )
            c_cnt += 1
        r_cnt += 1
    # print("avg distance: ", float(total_distance) / peg_cnt - 1)
    return float(total_distance) / hole_cnt - 1

def peg_distance(state):
    peg_list    = state.peg_indexes()
    # print("len of peg_list: ", len(peg_list))
    peg_cnt     = state.count_pegs()
    if peg_cnt == 1 or peg_cnt == 0:
        print("only 1 peg")
        return 0
    def one_distance(p1, p2):
        return pow(p1[0]-p2[0], 2) + pow( p1[1]-p2[1], 2 )
    
    total_distance = 0
    r_cnt = 0
    h_length = len(peg_list)
    while r_cnt < h_length - 1:
        c_cnt = r_cnt + 1
        while c_cnt < h_length:
            total_distance += one_distance( peg_list[r_cnt], peg_list[c_cnt] )
            c_cnt += 1
        r_cnt += 1
    # print("avg distance: ", float(total_distance) / peg_cnt - 1)
    return float(total_distance) / peg_cnt - 1

class AStar(Search.Search):
    def __init__(self, state, heuristic=0):
        Search.Search.__init__(self, state)
        
        if heuristic == 1:
            self.prio_queue = PrioQueue.PrioQueue(heuristic=h1)
        elif heuristic == 2:
            self.prio_queue = PrioQueue.PrioQueue(heuristic=h2)
        else:
            self.prio_queue = PrioQueue.PrioQueue()
        self.prio_queue.enqueue(state)

    def a_star(self):
        state = self.prio_queue.dequeue()
        if state is None:
            return None
        self.path.append(state)
        # if there is an available move for a given state
        moves = self.ps_state_check(state)
        self.ext_cnt += 1
        if( len(moves) == 0 ):
            print("Final State!")
            return (state, self.prio_queue, self.path)
        for move in moves:
            r = int(move[0])
            c = int(move[2])
            available_moves = moves[move]
            for a_move in available_moves:
                # push all available states into queue
                self.prio_queue.enqueue( state.move_peg(r,c, int(a_move)) )
                self.gen_cnt += 1
        return self.a_star()