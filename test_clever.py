import copy

'''
state = {
"board" : "r.b...b.rpppppppp................................PPPPPPPPR.B..B.R"
}
'''
'''
state = {
"board" : "r.......b........................................................"
}

state1 = {
"board" : "....r...b........................................................"
}
'''
'''
state = {
"board" : "............................b...................................."
}
'''


'''
state = {
"board" : "p......P........................................................"
}
'''
WHITE = 1
BLACK = -1
NONE = 0

#Inverte o tabuleiro fazendo o oponente ter visao de jogador
#Como testar: ?
def str_reverse(str):
	return "".join(map(lambda x : x.upper() if x.islower() else x.lower(), str[::-1]))	

#TODO verify
def pos_to_coord(aNumber):
	return (aNumber / 8 , aNumber % 8)

def diff(str1 , str2):
	position = -1
	firstTime = True
	f = 0
	t = 0
	for pair in zip(list(str1), list(str2)):
		position += 1
		if pair[0] != pair[1] and firstTime:
			f = position
			firstTime = False
			continue
		if pair[0] != pair[1] and not firstTime:
			t = position
	return pos_to_coord(f) , pos_to_coord(t)


class Board(object):
	def __init__(self, state):
		self.state = state


	def get_piece_lst(self,state):
		piece_lst = []
		str_pos = 0
		for char in state["board"]:
			if char != '.' and char != 'x':
				piece_lst.append( self.select_piece(char,state['board'], str_pos))
			str_pos += 1
		return piece_lst

	def select_piece(self,char, board, str_pos):
	
		PIECES = {
			'r': Rook,
			'p': Pawn,
			'b': Bishop
			#'q': Pawn,
			#'n': Pawn,
		}

		the_piece = PIECES[char.lower()]
		if char.lower() == char:
			color = WHITE
		else:
			color = BLACK
		return the_piece(color,board,str_pos)
		

class Piece(object):
	def __init__(self):
		self.board = None
		self.team = None
		self.position = None
		self.type = None

	def generate(self):
		pass

	def is_opponent(self, piece):
		return piece is not None and piece.team != self.team
	
	def is_enemy(self, my_piece, other_piece):
		if other_piece == '.':
			return False
		if my_piece.islower() and other_piece.islower():
			return False 
		else: 
			return True	


class Pawn(Piece):
	def __init__(self, piece_color, board, position):
		self.piece_color = piece_color
		self.board = board
		self.pos = position

	def __str__(self):
		print board

	def	generate(self):
		board = list(self.board)
		color = self.piece_color
		pos = self.pos
		board_lst = []
		
		if (color == BLACK):
			board = list(str_reverse("".join(board)))
			pos = 64 - pos

		x = pos + 8
		
		if board[x] == '.':
			work_board = copy.deepcopy(board)
			work_board[pos] = '.'    
			work_board[x] = 'p'
			board_lst.append(''.join(work_board))
		
		#It's not only subtract the position because the piece
		#could be in an edge, e. g, 8
		if self.is_enemy(board[pos],board[x+1]):
		#	print pos_to_coord(pos)
		#	print pos_to_coord(x+1)	
			work_board = copy.deepcopy(board)
			work_board[pos] = '.'    
			work_board[x+1] = 'p'
			board_lst.append(''.join(work_board))


		if self.is_enemy(board[pos],board[x-1]):
			print "x-1"
			work_board = copy.deepcopy(board)
			work_board[pos] = '.'    
			work_board[x-1] = 'p'
			board_lst.append(''.join(work_board))

		if (color == BLACK):
			board_lst = map(str_reverse, board_lst)
		
		return board_lst

class Rook(Piece):
	def __init__(self, piece_color, board, position):
		self.piece_color = piece_color
		self.board = board
		self.pos = position

	def __str__(self):
		print board

	def	generate(self):
		board = list(self.board)
		pos = self.pos
		board_lst = []
	
		#Vertical movement
		for x in range(pos+8,64,8):
			if board[x] == '.' or self.is_enemy(board[pos],board[x]):
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
			else:
				break #there's a piece in the way.
				
		#find out how many positions I have to move -> 8 - (pos % 8)
		for x in range(pos+1, pos +  8 - (pos % 8), 1):
			if board[x] == '.' or self.is_enemy(board[pos],board[x]):
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
			else:
				break

		for x in range(pos - (pos % 8), pos, 1):
			if board[x] == '.' or self.is_enemy(board[pos],board[x]):
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
			else:
				break

		return board_lst

class Bishop(Piece):
	def __init__(self, piece_color, board, position):
		self.piece_color = piece_color
		self.board = board
		self.pos = position

	def __str__(self):
		print board

	#Stub
	def	generate(self):
		
		board = list(self.board)
		pos = self.pos
		board_lst = []

		#Upper right diag
		for x in xrange(pos,64,9):
			if board[x] == '.' or self.is_enemy(board[pos],board[x]):
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
		#Upper left diag
		for x in xrange(pos,64,7):
			if board[x] == '.' or self.is_enemy(board[pos],board[x]):
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))	

		#Lower left(?) diag
		for x in xrange(pos,0,-7):
			print x
			if board[x] == '.' or self.is_enemy(board[pos],board[x]):
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))

		#Lower right(?) diag
		for x in xrange(pos,0,-9):
			print x
			if board[x] == '.' or self.is_enemy(board[pos],board[x]):
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
				
		
		return board_lst
'''
board = Board(state)
p_lst = board.get_piece_lst(state)
for b in p_lst:
	print b.piece_color
	for newBoard in b.generate():
		print newBoard
'''
def print_board(str):
	print str[0:7]
	print str[8:15]
	print str[16:23]
	print str[24:31]
	print str[32:39]
	print str[40:47]
	print str[48:55]
	print str[56:63]
	
def test_diff():
	str1 = "........p........................................................"
	str2 = "................p................................................"
	print diff(str1,str2)
	
def test_pawn():
	#Caso do primeiro movimento do peao
	state = {"board" : "........p........................................................"}

	r1 = "................p................................................"
	r2 = "........................p........................................"
	
	
	'''
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		print b.piece_color
		for newBoard in b.generate():
			print newBoard
			state['board'] = newBoard
			print r1
	
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		print b.piece_color
		for newBoard in b.generate():
			print newBoard
			print r2
	
	#Nao pode ir pra frente -> vazio
	state = {"board" : "........p.......P................................................"}
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		print b.piece_color
		for newBoard in b.generate():
			print newBoard
	'''		
	state = {"board" : "........p.......P..............................................."}
	print_board(state['board'])
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		print b.piece_color
		for newBoard in b.generate():
			print_board(newBoard)
			print " "
			#print state['board']

def test_bishop():
	state = {"board" : "........b......................................................."}
	print_board(state['board'])
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		print b.piece_color
		for newBoard in b.generate():
			print_board(newBoard)
			print " "
			#print state['board']
		
test_bishop()

