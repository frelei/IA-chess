import copy

'''
state = {
"board" : "r.b...b.rpppppppp................................PPPPPPPPR.B..B.R"
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
	#return (aNumber / 8 , aNumber % 8)
	return ((aNumber / 12), (aNumber % 10) )

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
	print f , t
	return pos_to_coord(f) , pos_to_coord(t)


class Board(object):
	def __init__(self, state):
		self.state = state


	def get_piece_lst(self,state):
		piece_lst = []
		str_pos = 0
		for char in state["board"]:
			if char != '.' and char != '*':
				piece_lst.append( self.select_piece(char,state['board'], str_pos))
			str_pos += 1
		return piece_lst

	def select_piece(self,char, board, str_pos):
	
		PIECES = {
			'r': Rook,
			'p': Pawn,
			'b': Bishop
			#'q': Queen,
			#'n': Knight,
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
			#print_board("".join(board))
			pos = 119 - pos
			#print board[pos]

		x = pos + 10
		
		if board[x] == '.':
			work_board = copy.deepcopy(board)
			work_board[pos] = '.'    
			work_board[x] = 'p'
			board_lst.append(''.join(work_board))
		
		if self.is_enemy(board[pos],board[x+1]) and board[x+1] != '*':
			work_board = copy.deepcopy(board)
			work_board[pos] = '.'    
			work_board[x+1] = 'p'
			board_lst.append(''.join(work_board))


		if self.is_enemy(board[pos],board[x-1]) and board[x-1] != '*':
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
		color = self.piece_color
		
		if (color == BLACK):
			board = list(str_reverse("".join(board)))
			pos = 119 - pos
	
		#Vertical movement
		for x in range(pos+10,99,10):
			if board[x] == '.' and board[x] != '*':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
				
			elif self.is_enemy(board[pos],board[x]) and board[x] != '*' :
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
				break
			else:
				break #there's a piece in the way.
					  #Or a boundary
				

		for x in range(pos+1, pos +  10 - (pos % 10), 1):
			#print x , pos_to_coord(x) , (x % 10)
			if board[x] == '.' and board[x] != '*':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
				
			elif self.is_enemy(board[pos],board[x]) and board[x] != '*' :
	
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
				break
			else:
				break

		for x in xrange( pos-1 , pos + 1 - (pos % 10),  -1):
			if board[x] == '.' and board[x] != '*':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
			elif self.is_enemy(board[pos],board[x]) and board[x] != '*'  :
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'r'
				board_lst.append(''.join(work_board))
				break
			else:
				break

		if (color == BLACK):
			board_lst = map(str_reverse, board_lst)
			
		return board_lst

class Bishop(Piece):
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
		color = self.piece_color

		if (color == BLACK):
			board = list(str_reverse("".join(board)))
			#print_board("".join(board))
			pos = 119 - pos
			#print board[pos]
		
		#Upper right diag
		for x in xrange(pos+11,120,11):
			if board[x] != '*' and board[x] == '.':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
			elif self.is_enemy(board[pos],board[x]) and board[x] != '*':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
				break
			else:
				break
		
		#Upper left diag
		for x in xrange(pos+9,120,9):
			if board[x] != '*' and board[x] == '.':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
			elif self.is_enemy(board[pos],board[x]) and board[x] != '*':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
				break
			else:
				break

		
		#Lower left(?) diag
		for x in xrange(pos-9,0,-9):
			if board[x] != '*' and board[x] == '.':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
			elif self.is_enemy(board[pos],board[x]) and board[x] != '*':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
				break
			else:
				break
				
		
		#Lower right(?) diag
		for x in xrange(pos-11,0,-11):
			if board[x] != '*' and board[x] == '.':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
			elif self.is_enemy(board[pos],board[x]) and board[x] != '*':
				work_board = copy.deepcopy(board)
				work_board[pos] = '.'    
				work_board[x] = 'b'
				board_lst.append(''.join(work_board))
				break
			else:
				break
				
		if (color == BLACK):
			board_lst = map(str_reverse, board_lst)
			
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
	print str[0:10]
	print str[10:20]
	print str[20:30]
	print str[30:40]
	print str[40:50]
	print str[50:60]
	print str[60:70]
	print str[70:80]
	print str[80:90]
	print str[90:100]
	print str[100:110]
	print str[110:120]

def enrich_str(str):
	return ("********************" 
	+ "*" + str[0:8]   + "*" 
	+ "*" + str[8:16]  + "*"
	+ "*" + str[16:24] + "*"
	+ "*" + str[24:32] + "*"
	+ "*" + str[32:40] + "*"
	+ "*" + str[40:48] + "*"
	+ "*" + str[48:56] + "*"
	+ "*" + str[56:64] + "*" + "********************"  )
	
	
def test_diff():
	str1 = "........p........................................................"
	str2 = "................p................................................"
	print diff(str1,str2)
	
def test_pawn():
	#Caso do primeiro movimento do peao
	#state = {"board" : "........p........................................................"}
	
	str = enrich_str("........p.......P...............................................")
	state = {"board" : str}
	
	print_board(state['board'])
	print "board printed"
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		for newBoard in b.generate():
			print_board(newBoard)
			print " "
			
	str = enrich_str("........p........P..............................................")
	state = {"board" : str}
	
	print_board(state['board'])
	print "board printed"
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		for newBoard in b.generate():
			print_board(newBoard)
			print " "

def test_bishop():
	state = {"board" : enrich_str("..............B.................................................")}
	#print enrich_str(state['board'])
	print_board(state['board'])
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		for newBoard in b.generate():
			print_board(newBoard)

def test_rook():
	state = {"board" : enrich_str("..........P...r.................................................")}
	#print enrich_str(state['board'])
	print_board(state['board'])
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		for newBoard in b.generate():
			print_board(newBoard)
			
	state = {"board" : enrich_str("...........................................................r....")}
	#print enrich_str(state['board'])
	print_board(state['board'])
	board = Board(state)
	p_lst = board.get_piece_lst(state)
	for b in p_lst:
		for newBoard in b.generate():
			print_board(newBoard)


def test_diff():
	
	str1 = enrich_str("p...............................................................")
	str2 = enrich_str("b...............................................................")
	print diff(str1,str2)
	
	str1 = enrich_str("p...............................................................")
	str2 = enrich_str(".p..............................................................")
	print diff(str1,str2) , "(0,0) (0,1)"

	str1 = enrich_str("..............................................................p.")
	str2 = enrich_str("...............................................................p")
	print diff(str1,str2) , " (7,1) (7,0)"

	str1 = enrich_str("r.b...b.rpppppppp................................PPPPPPPPR.B..B.R")
	str2 = enrich_str("r.b...br.pppppppp................................PPPPPPPPR.B..B.R")

	print str1[28] , str1[31]
	print diff(str1,str2)  , "(0,7) (0,6)"
	
test_diff()	