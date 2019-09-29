class Stack:
    def __init__(self, stack=[]):
        self.stack = stack
    
    def push(self, elem):
        # print("Push to stack.")
        self.stack.append(elem)
    
    def pop(self):
        # print( "Pop from stack." )
        if len(self.stack) == 0:
            print("Stack is empty.")
            return None
        return self.stack.pop()
    
    def get_stack(self):
        return self.stack
    
    def is_empty(self):
        return True if len(self.stack) == 0 else False

    def print_stack(self):
        print("from down to top")
        for i in self.stack:
            i.print()