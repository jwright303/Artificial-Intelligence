'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
    

    #This is the successor function that I came up with
    #This takes in the board (b), and the current player symbol
    #This function returns an array of moves that will create all the possible successor boards
    def gen_successors(self, b, current):
	valMoves = []

	for i in range(0, 4):
	    for j in range(0, 4):
		if b.is_legal_move(j, i, current):
		    valMoves.append([j, i])
	
	return valMoves
    
    #This is the Result(a, state) function from the pseudo code
    #This funciton takes in the action to preform, the baord to perform it on ,and the symbol that is going to be used
    #This function returns a new Othello board with the given action taken
    def boardRes(self, action, board, sym):
	newOthello = board.cloneOBoard()
	newOthello.play_move(action[0],action[1], sym)
	
	return newOthello
    
    #This is the utility funciton that takes in the board, and returns the utility of it. In this case it has large positive utility for more O on the boards
    #This fucntion takes in the board to check the utility of and returns a number corresponding to the utility
    def eval_terminal(self, board):
	util = 0
	for row in board.grid:
	    for i in range(0, len(board.grid)):
		    if row[i] == 'O':
			util += 1
		    else:
			util -= 1
	return util



    #This is the maximizing recursive function
    #THis takes in the current state and returns the value that will maximize the results from this stage
    def getMaxNodes(self, state):
	if not state.has_legal_moves_remaining('X'):#Returns utility if a terminal node
		#print("ev term", self.eval_terminal(state))
	    return self.eval_terminal(state)
    	
    	v = 1000001#Sets current value to bigger than anything possible
	actions = self.gen_successors(state, 'X')
	for a in actions:
	    v = min(v, self.getMinNodes(self.boardRes(a, state, 'X')))
	return v

    #This function is the minimizing recursive funciton for the minMax algorithm
    #This fucntion takes in the board and returns the value that will produce to the least cost
    def getMinNodes(self, board):
	if not board.has_legal_moves_remaining('O'):
		#print("ev_term", self.eval_terminal(board))
	    return self.eval_terminal(board)

	v = -1000001
	actions = self.gen_successors(board, 'O')
	for a in actions:
	    v = max(v, self.getMaxNodes(self.boardRes(a, board, 'O')))
	return v

    #This is the minMax algorithm implementation
    #This function takes in the current board and returns the action that corresponds to the greatest utility for player 2 (the algorithm)
    #This function iterates through all the possible actions from this state and searches for the possible utility for each, maximizing that for the algorithm
    def get_move(self, board):
	minNodeV = -1000001
	minAction = None
	curSymbol = 'O'
	#find actions by calling the gen_successors here
	actions = self.gen_successors(board, curSymbol)
	
	for action in actions:
	    curVal = self.getMaxNodes(self.boardRes(action, board, 'O'))
	    #print(curVal)
	    if curVal > minNodeV:
		minNodeV = curVal
		minAction = action
	
	return (minAction[0], minAction[1])
