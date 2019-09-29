from constraint import *
import itertools as it

class Block:
	# x,y,z are 2d coordinate tuples
	# False is horizontal, True is vertical block 
	def __init__(self,x,y,z):
		self.start = x
		self.middle = y
		self.end = z
		self.orientation = self.calcOrientation()

	def calcOrientation(self):
		return (self.start[0] - self.middle[0]) == 0

	def isGround(self):
		return self.start[1] == 0 or self.end[1] == 0


	def __lt__(self, otherBlock):
	    return True


def checkMiddle(blockList,middlePoint):
	belowMiddlePoint = (middlePoint[0], middlePoint[1] - 1)
	for block in blockList:
		if belowMiddlePoint in [block.start, block.middle, block.end]:
			return True
	return False

def checkEdges(blockList,currentBlock):
	possiblePoints = []

	for block in blockList:
		possiblePoints.append(block.start)
		possiblePoints.append(block.middle)
		possiblePoints.append(block.end)

	flag = 0
	if (currentBlock.start[0],currentBlock.start[1]-1) in possiblePoints:
		flag += 1

	if (currentBlock.middle[0],currentBlock.middle[1]-1) in possiblePoints:
		flag += 1

	if (currentBlock.end[0],currentBlock.end[1]-1) in possiblePoints: 
		flag += 1

	if flag < 2:
		return False
	return True

def verticalCheck(blockList,index):
	currentBlock = blockList[index]
	flag = False
	for j in range(index):
		bottomCoordinate = (0,0)
		if currentBlock.start[1]-currentBlock.end[1] > 0:
			bottomCoordinate = currentBlock.end
		else:
			bottomCoordinate = currentBlock.start

		if (bottomCoordinate[0],bottomCoordinate[1]-1) in [blockList[j].start,blockList[j].middle,blockList[j].end]:
			flag = True
			break

	return flag

def horizontalCheck(blockList, index):
	currentBlock = blockList[index]
	middleCoordinate = currentBlock.middle
	
	prevCoordinatesList = blockList[:index]
	middleCheck = checkMiddle(prevCoordinatesList, middleCoordinate)
	edgeCheck = checkEdges(prevCoordinatesList,currentBlock)
	return middleCheck or edgeCheck

def isSupported(blockList,index):
	currentBlock = blockList[index]
	if currentBlock.orientation: # Vertical
	    return verticalCheck(blockList,index)
	else:
		return horizontalCheck(blockList,index)		


def checkConstraint(*args):
	i=0
	flag = False
	while i < len(args):
		flag = args[i].isGround() or isSupported( args,i )
		if not flag:
			return flag 
		i+=1
	return flag


b0 = Block((0,0),(2,0),(4,0))
b1 = Block((2,2),(2,4),(2,6))	
b2 = Block((6,0),(6,2),(6,4))	
b3 = Block((12,0),(12,2),(12,4))	
b4 = Block((4,6),(6,6),(8,6))	
b5 = Block((10,6),(12,6),(14,6))	
b6 = Block((2,8),(4,8),(6,8))	
b7 = Block((8,8),(10,8),(12,8))	
b8 = Block((5,10),(7,10),(9,10))	

domain = [b0,b1,b2,b3,b4,b5,b6,b7,b8]
variables = range(len(domain))
problem = Problem()
problem.addVariables(variables,domain)
problem.addConstraint(AllDifferentConstraint())
problem.addConstraint(checkConstraint,variables)
print(len(problem.getSolutions()))
