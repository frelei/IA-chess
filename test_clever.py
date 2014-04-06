import copy

state = {
"board" : "r.b...b.rpppppppp................................PPPPPPPPR.B..B.R"
}

WHITE = 1
BLACK = -1
NONE = 0

class Board(object):
	def __init__(self, state):
		self.state = state
		#self.cells = [[None for j in xrange(8)] for i in xrange(8)]
		#self.my_pieces = []
		#self.piece_color =  piece_color

	def get_piece_lst(self,state):
		piece_lst = []
		str_pos = 0
		for char in state["board"]:
			if char != '.':
				piece_lst.append( self.select_piece(char.lower(),state['board'], str_pos))
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
		the_piece = PIECES[char]
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
	
	#Prob/ is with problems
	def is_enemy(self, my_piece, other_piece):
		if my_piece.islower() and other_piece.islower():
			return True 
		else: 
			return False	


class Pawn(Piece):
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

		x = pos + 8 #If is the other side subtract
		if board[x] == '.':
			work_board = copy.deepcopy(board)
			work_board[pos] = '.'    
			work_board[x] = 'p'
			board_lst.append(''.join(work_board))
		
	
		if self.is_enemy(board[pos],board[x]):
			work_board = copy.deepcopy(board)
			work_board[pos] = '.'    
			work_board[x-1] = 'p'
			board_lst.append(''.join(work_board))


		if self.is_enemy(board[pos],board[x]):
			work_board = copy.deepcopy(board)
			work_board[pos] = '.'    
			work_board[x+1] = 'p'
			board_lst.append(''.join(work_board))

		
		return board_lst

class Rook(Piece):
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
	
		#Vertical movement
		for x in range(pos,64,8):
			if board[x] == '.': # or self.is_enemy(board[pos],board[x])
				print "r", pos, x
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
			else:
				print "break"
				break #The there's a piece in the way.
				
		#Horizontal TODO
			
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
		
		board = self.board
		pos = self.pos
		board_lst = []
		work_board = board[:]
		thereturn = board_lst.append(work_board)

		return board_lst

board = Board(state)
p_lst = board.get_piece_lst(state)
for b in p_lst:
	for newBoard in b.generate():
		print newBoard


