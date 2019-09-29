from Block import Block
from constraint import *

class CSP:
    def __init__(self, blockList):
        self.blocks = self.buildDomain( blockList )
        self.csp    = Problem()
        # variables are numbers (orders) and domain is blocks
        problem.addVariables( range(len(self.blocks)), self.blocks )
        # from constraint documentation, makes all variables different
        problem.addConstraint(AllDifferentConstraint())
        problem.addConstraint( self.checkConstraints )
    
    def buildDomain(self, blockList):
        domain = []
        i = 0
        for i in range( 0, len(blockList), 3 ):
            domain.append( Block( (blockList[i], blockList[i+1], blockList[i+2]) )  )
        return domain

    def run(self):
        self.results = self.csp.getSolution()

    def isSupported(self, index):
        if block.isVertical():
            self.checkVerticalConstraints(index)
        else:
            self.checkHorizontalConstraints(index)

    def getPreviousBlockPoints(self, blocksLength):
        previousBlockPoints = []
        for index in range(blocksLength):
            previousBlockPoints += self.blocks[index].getCoordinatesAsArray
        return previousBlockPoints

    def checkVerticalConstraints(self, index):
        block = self.blocks[index]
        bottomPoint = block.tail if block.head.y > block.tail.y else block.head

        return (bottomPoint.x, bottomPoint.y - 2) in self.getPreviousBlockPoints(index)
    
    def checkHorizontalConstraints(self, index):
        def middleSupported():
            belowMiddlePoint = (middlePoint.x, middlePoint.y - 2)
            return belowMiddlePoint in previousBlockPoints
        
        def edgeSupported():
            def getBelowPoint(point):
                return (point.x, point.y - 2)
            belowPoints = map(getBelowPoint, block.getCoordinatesAsArray())
            return sum( point in belowPoints for point in previousBlockPoints ) > 1
            

        block = self.blocks[index]
        middlePoint = block.middle
        previousBlockPoints = self.getPreviousBlockPoints(index)
        return middleSupported() or edgeSupported()

    def checkConstraints(self, *args):
        for i in range(len(args)):
            if args[i].onGround() or self.isSupported(i):
                return True
        return False