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
				str_pos += 1
				piece_lst.append( self.select_piece(char.lower(),state['board'], str_pos))

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
		board = self.board
		pos = self.pos
		board_lst = []
		work_board = board[:]

		x = pos + 8
		if board[pos] == 'p' :
			if board[x] == '.':
				print board[pos] , board[x] , pos, x
				aux_list = list(board) #Perfomance issues, strings are immutable in python
				aux_list[pos] = '.'    #TODO swap strings function
				aux_list[x] = 'p'
				work_board = ''.join(aux_list)

			board_lst.append(work_board)
			work_board = copy.deepcopy(board)
			if board[x-1] == self.is_enemy(board[pos],board[x]):
				aux_list = list(board)
				aux_list[pos] = '.'
				aux_list[x-1] = 'p'
				work_board = ''.join(aux_list)
	
			board_lst.append(work_board)

			if board[x+1] == self.is_enemy(board[pos],board[x]):
				aux_list = list(board)
				aux_list[pos] = '.'
				aux_list[x+1] = 'p'
				work_board = ''.join(aux_list)
		
		
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
		
		board = self.board
		pos = self.pos
		board_lst = []
		work_board = board[:]
		thereturn = board_lst.append(work_board)

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




