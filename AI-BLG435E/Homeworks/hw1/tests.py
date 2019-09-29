from Classes import Board
from Classes import Stack
from Classes import Dfs
from Classes import Bfs
from Classes import Queue
from Classes import PrioQueue
from Classes import AStar
import sys

def print_results(result, sch):
    result.print()
    print( result.count_pegs(), " pegs on the result board")
    print( sch.get_gen_cnt(), " nodes are generated")
    print( sch.get_ext_cnt(), " nodes are extended" )

def available_move_test(board, r, c):
    d = board.is_move_check(r,c)
    print( "available moves for " + str(r) + ":" + str(c) + " are ---->", d )
    return d

def big_move_test(r=3, c=1):
    states = []
    board = Board.Board(7)
    print("Initial board:")
    board.print()
    states.append(board)

    # available_move_test
    print("available move test")
    d = available_move_test(board, r, c)

    # move_test
    print("move test")
    if( len(d) != 0):
        print(d)
        b = move_test( board,int(d[0]), r,c )
        states.append(b)
        # b.print()
    else:
        print("no move")
    b = move_test( b, 4,3,4 )
    states.append(b)
    # b.print()

    path_print(states)
    print("in")
    sted = AStar.h2(states)
    path_print(sted)

def move_test(board, d, r=0, c=0 ):
    return board.move_peg(r, c, d)

def main():
    r = int(sys.argv[1])
    c = int(sys.argv[2])
    big_move_test(r,c)

def path_print(pth):
    print("Path is: ")
    for i in pth:
        i.print()

def a_star_test(hn):
    sys.setrecursionlimit(10000)
    board   = Board.Board(7)
    a_star  = AStar.AStar(board, hn)
    result, queue, path = a_star.a_star()
    print_results(result, a_star)

def dfs_test():
    board   = Board.Board(7)
    dfs     = Dfs.Dfs(board)
    result, stack, path = dfs.dfs()
    print_results( result, dfs )

def bfs_test():
    sys.setrecursionlimit(10000)
    board   = Board.Board(7)
    bfs     = Bfs.Bfs(board)
    result, queue, path = bfs.bfs()
    print_results(result, bfs)
    # print("Path is: ")
    # for i in path:
    #     i.print()

def prio_queue_test():
    a   = [3,2,4,5]
    pq  = PrioQueue.PrioQueue(prio_queue=a, heuristic=AStar.h1)
    pq.dequeue()
    pq.enqueue(-1)
    pq.dequeue()
    pq.dequeue()
    pq.dequeue()
    pq.dequeue()
    pq.dequeue()
    pq.dequeue()

def peg_indexes_test():
    m = Board.Board(7)
    print(m.peg_indexes())

def iterative_bfs_test():
    board   = Board.Board(7)
    bfs     = Bfs.Bfs(board)
    result, queue, path = bfs.iterative_bfs()
    print("Final state: ")
    result.print()
    print("Peg count is: ", result.count_pegs() )
    # print("Path is: ")
    # for i in path:
    #     i.print()
    
    print( bfs.get_gen_cnt(), " nodes are generated")
    print( bfs.get_ext_cnt(), " nodes are extended" )

if __name__ == '__main__':
    # dfs_test()
    # iterative_bfs_test()
    # bfs_test()
    # prio_queue_test()
    a_star_test(1)
    # peg_indexes_test()
    # big_move_test()