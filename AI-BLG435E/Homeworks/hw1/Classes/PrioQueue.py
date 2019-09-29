from Classes import Queue

class PrioQueue(Queue.Queue):
    def __init__( self, prio_queue=[], heuristic=None ):
        Queue.Queue.__init__(self, prio_queue)
        
        if heuristic is None:
            self.sorter = None
        else:
            self.sorter = heuristic
    
    def enqueue(self, elem):
        self.queue.append(elem)
    
    def dequeue(self):
        if  self.is_empty():
            print("All elements are dequeued before.")
            return None
        if self.sorter is not None:
            self.queue = self.sorter( self.queue )
        fst = self.queue[0]
        self.queue = self.queue[1:]
        return fst
    
    def is_empty(self):
        return True if len(self.queue) == 0 else False
    
    def get_queue(self):
        return self.queue