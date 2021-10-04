import sys
import copy
import heapq

#Creates a Node class for storing the current state and its parents
#Two functoins, the first being the initializer where it sets up the state, the depth and parent will be updated after this is called
#The other function prints out the list of states that led up to the last one
class Node:
	def __init__(self, ste):
		self.state = ste
		self.depth = 0
		self.priority = 0
		self.parent = None

	def printL(self):
		nextN = self.parent
		print(self.state)
		while nextN is not None:
			print(nextN.state)
			nextN = nextN.parent

#This function expands the current node to all of the viable children nodes it could have according to the order form the assignemnt
#Takes in the current node, the current state, the list of nodes already expanded, a list of nodes on the queue, the index where the boat is, and the index where the boat isnt
#This funciton returns a list of the children node created form the expanded node
def expandNode(curState, exclusions, queue, bIn, nextIn, curNode):
	retArr = []

	if curState[bIn][0] > 0 and (curState[bIn][0] - 1 == 0 or (curState[bIn][0] - 1 >= curState[bIn][1] and curState[nextIn][0] + 1 >= curState[nextIn][1])):
		#Use the deepcopy method from the copy library to be able to modify the new list uniquely
		newState = copy.deepcopy(curState)
		newState[bIn][0] -= 1
		newState[nextIn][0] += 1
		newState[nextIn][2] = 1
		newState[bIn][2] = 0
		newNode = Node(newState)
		newNode.parent = curNode
		if (not inFrontier(queue, newState)) and (newState not in exclusions):#Only adds nodes that aren't in the frontier already
			retArr.append(newNode)
	if curState[bIn][0] > 1 and (curState[bIn][0] - 2 == 0 or curState[bIn][0] - 2 >= curState[bIn][1]):
		newState = copy.deepcopy(curState)
		newState[bIn][0] -= 2
		newState[nextIn][0] += 2
		newState[nextIn][2] = 1
		newState[bIn][2] = 0
		newNode = Node(newState)
		newNode.parent = curNode
		if (not inFrontier(queue, newState)) and (newState not in exclusions):
			retArr.append(newNode)
	if curState[bIn][1] > 0 and (curState[nextIn][0] == 0 or curState[nextIn][0] >= curState[nextIn][1] + 1):
		newState = copy.deepcopy(curState)
		newState[bIn][1] -= 1
		newState[nextIn][1] += 1
		newState[nextIn][2] = 1
		newState[bIn][2] = 0
		newNode = Node(newState)
		newNode.parent = curNode
		if not inFrontier(queue, newState) and newState not in exclusions:
			retArr.append(newNode)
	if curState[bIn][0] > 0 and curState[bIn][1] > 0 and curState[nextIn][0] + 1 >= curState[nextIn][1] + 1:
		newState = copy.deepcopy(curState)
		newState[bIn][1] -= 1
		newState[nextIn][1] += 1
		newState[bIn][0] -= 1
		newState[nextIn][0] += 1
		newState[nextIn][2] = 1
		newState[bIn][2] = 0
		newNode = Node(newState)
		newNode.parent = curNode
		if not inFrontier(queue, newState) and newState not in exclusions:
			retArr.append(newNode)
	if curState[bIn][1] > 1 and (curState[nextIn][0] == 0 or curState[nextIn][0] >= curState[nextIn][1] + 2):
		newState = copy.deepcopy(curState)
		newState[bIn][1] -= 2
		newState[nextIn][1] += 2
		newState[nextIn][2] = 1
		newState[bIn][2] = 0
		newNode = Node(newState)
		newNode.parent = curNode
		if not inFrontier(queue, newState) and newState not in exclusions:
			retArr.append(newNode)
	return retArr


#This function checks to see if the current state is already in the fronteir and returns true if it is and false otherwise
def inFrontier(queue, state):
	for item in queue:
		if item.state == state:
			return True

	return False


#This is the iterative depth first search algorithm for finding the goal state
#This function takes in the starting state of the problem and returns the node with the goal state. Also prints out number of expanded nodes
#This is very similar to the DFS algorithm except the depth is gradually increased. The limit I put on the dpeth is the number of chickens cubed which should be sufficient especially since this is an optimal algorithm
def IDFS(startState, endState):
	depth = 0 #starting depth of 0 will just check the initial state for being the goal which is a little impractical
	aCount = startState[1][0]
	expanded = 0
	endState = [startState[1], startState[0]]
	startS = Node(startState)

	#Max depth = chicken count = wolf count cubed
	while(depth < aCount * aCount * aCount):
		queue = [startS]
		exclusions = []

		#Within each depth iteration expand all possible nodes
		while(True):
			if(len(queue) == 0):#breaks out of iteration when all nodes have been exhausted
				break

			curNode = queue.pop(0)
			curState = curNode.state
			bIn = 0
			nextIn = 0

			if curState[0] == endState[0]:
				print("Expanded IDFS nodes:", expanded)
				return curNode

			exclusions.append(curState)

			if curState[0][-1] == 1:
				bIn = 0
				nextIn = 1
			else:
				bIn = 1
				nextIn = 0

			expanded += 1

			#Actual expansion part, but only for nodes that haven't reached the depth limit yet, and those not in the exclusion
			#if curState not in exclusions and curNode.depth < depth:
			if curNode.depth < depth:
				newNodes = expandNode(curState, exclusions, queue, bIn, nextIn, curNode)#Gets all possible children from current node
				newNodes.reverse()
				for item in newNodes:#For each node increase the depth, and add it to the queue, at the front since DFS
					parentN = item.parent
					item.depth = parentN.depth + 1
					queue.insert(0, item)
		depth += 1

	return


#This function is the depth first seach algorithm for this problem where a children is expanded as far as possible until it can't be anymore before moving on to the other children
#This funciton takes in the start state of the problem, returns the goal state node which includes the past states, and prints out the number of nodes expanded
#If the queue becomes empty that means there were no goal nodes found so it prints failure and returns nothign
def DFS(startState, endState):
	startS = Node(startState)
	queue = [startS]
	exclusions = []
	expanded = 0

	while(True): #Nonstop run through this loop, it will either end due to empty queue or becuase the found goal state
		if(len(queue) == 0):
			print("failed")
			return None

		curNode = queue.pop(0)
		curState = curNode.state
		bIn = 0
		nextIn = 0

		#Goal node found, print out expanded nodes and return final node to print out its successors
		if curState[0] == endState[0]:
			print("Expanded DFS nodes:", expanded)
			return curNode

		exclusions.append(curState)

		#Initalizes the indexing for where the boat is and where the destination is
		if curState[0][-1] == 1:
			bIn = 0
			nextIn = 1
		else:
			bIn = 1
			nextIn = 0

		expanded += 1

		#Expand current node if its not already been visited
		#if curState not in exclusions:
		newNodes = expandNode(curState, exclusions, queue, bIn, nextIn, curNode)
		newNodes.reverse()
		for item in newNodes:
			queue.insert(0, item)
	return


#This function is the breadth first search algorithm where it expands all nodes on the same level before moving down in depth
#This function takes in the starting state and the goal state of the search and returns the goal node with the corresponding path
#This function also prints out the number of nodes that are expanded during the search
def BFS(startState, endState):
	startS = Node(startState)
	queue = [startS]
	exclusions = []
	expanded = 0

	while(True):
		if(len(queue) == 0):
			print("failed")
			return None

		curNode = queue.pop(0)
		curState = curNode.state
		bIn = 0
		nextIn = 0

		if curState[0] == endState[0]:
			print("Expanded BFS nodes:", expanded)
			return curNode

		exclusions.append(curState)

		if curState[0][-1] == 1:
			bIn = 0
			nextIn = 1
		else:
			bIn = 1
			nextIn = 0

		expanded += 1

		#if curState not in exclusions:
		newNodes = expandNode(curState, exclusions, queue, bIn, nextIn, curNode)
		for item in newNodes:
			queue.append(item)
	return


def aStarSearch(startState, endState):
	startS = Node(startState)
	startPQV = (startState[1][0] + startState[1][1]) / 2
	priQ = [startPQV]
	nodesQueue = [startS]
	priQV = {startPQV: [startS]}
	exclusions = []
	expanded = 0

	while(True):
		if(len(priQ) == 0):
			print("failed")
			return None

		stateVal = heapq.heappop(priQ)
		curNode = priQV[stateVal].pop()
		curState = curNode.state
		bIn = 0
		nextIn = 0

		if curState[0] == endState[0]:
			print("Expanded A* Search nodes:", expanded)
			return curNode

		exclusions.append(curState)

		if curState[0][-1] == 1:
			bIn = 0
			nextIn = 1
		else:
			bIn = 1
			nextIn = 0

		expanded += 1

		#if curState not in exclusions:
		newNodes = expandNode(curState, exclusions, nodesQueue, bIn, nextIn, curNode)
		for item in newNodes:
			state = item.state
			nodesQueue.append(item)
			stateV = (state[1][0] + state[1][1]) / 2
			heapq.heappush(priQ, stateV)
			if stateV in priQV.keys():
				priQV[stateV].append(item)
			else:
				priQV[stateV] = [item]

	return


def parseFile(fileName):
	fI = open(fileName, "r")
	inStr = fI.read().split("\n")
	inStr.pop()
	a = inStr[0].split(",")
	b = inStr[1].split(",")

	for i in range(0, len(a)):
		a[i] = int(a[i])
	for j in range(0, len(b)):
		b[j] = int(b[j])
	startState = [a, b]
	fI.close()

	return startState


def main():
	args = sys.argv
	if len(args) < 5:
		print(args)
		print("Not enough command line arguments provided")
		print("Format: python HW1.py initial_state.txt goal_state.txt mode")
		print("     the format of both state files are chicken_num, wolf_num, is boat on this side (0 or 1)")
		print("     mode is either bfs, dfs, iddfs, astr")
		return 0

	iState = args[1]
	gState = args[2]
	mode = args[3]
	outFile = args[4]

	startState = parseFile(iState)
	endState = parseFile(gState)

        print(startState)
        print(endState)

	if mode == 'bfs':
		end = BFS(startState, endState)
	elif mode == 'dfs':
		end = DFS(startState, endState)
	elif mode == 'iddfs':
		end = IDFS(startState, endState)
	elif mode == 'astr':
		end = aStarSearch(startState, endState)
	else:
		print("Invalid search method given, acceptable inputs: 'dfs' 'iddfs' 'bfs' 'astr'")
		return 1

	for i in range(0, 2):
		if i == 1:
			sys.stdout = open(outFile, 'w')

	if end != None:
		print("End")
		end.printL()
		print("Start")

	return
main()
