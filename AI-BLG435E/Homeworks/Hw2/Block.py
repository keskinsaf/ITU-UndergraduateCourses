from constraint import *

class Block:
    def __init__(self, head, middle, tail):
        self.head   = head
        self.middle = middle
        self.tail   = tail
    
    def isVertical(self): # True if vertical, False if horizontal
        return self.middle.y - self.head.y != 0
    
    def onGround(self):
        return self.head.y == 0 or self.tail.y == 0
    
    def getCoordinatesAsArray(self):
        return [self.head, self.middle, self.tail]