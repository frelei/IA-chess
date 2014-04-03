
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
			'r': Pawn,
			'p': Pawn,
			'b': Pawn,
			'q': Pawn,
			'n': Pawn,
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
		work_board = board.copy() #Str dont have copy

		#Current position is pos
		for x in xrange(pos,64,8):
			if board[x] == '.':
				work_board[pos] = '.'
				work_board[x] = 'p'

			board_lst.append(work_board)
			work_board = board.copy()
			if board[x-1] == is_enemy(board[x]):
				work_board[x-1] = 'p'
		
			board_lst.append(work_board)

			if board[x+1] == is_enemy(board[x]):
				work_board[x+1] = 'p'

		return board_lst

board = Board(state)
for x in  board.get_piece_lst(state):
	for y in x.generate():
		print y