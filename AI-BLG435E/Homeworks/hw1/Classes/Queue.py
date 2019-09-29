class Queue:
    def __init__(self, queue=[]):
        self.queue = queue
        self.index = 0
    
    def enqueue(self, elem):
        # print("Enqueue to queue.")
        self.queue.append(elem)
    
    def dequeue(self):
        # print("Dequeue from queue.")
        # version without emptying queue
        # if len( self.queue ) == self.index:

        # version with emptying queue
        if  len(self.queue) == 0:
            print("All elements are dequeued before.")
            return None
        
        # version without emptying queue
        # fst = self.queue[self.index]
        # self.index += 1

        # version with emptying queue
        fst = self.queue[0]
        self.queue = self.queue[1:]
        return fst
    
    def is_ended(self):
        return True if self.index == len(self.queue) else False
    
    def is_empty(self):
        return True if len(self.queue) == 0 else False

    def get_queue(self):
        return self.queue
