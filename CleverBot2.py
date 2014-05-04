import time
import sys
import random
import copy

from base_client import LiacBot

WHITE = 1
BLACK = -1
NONE = 0


 # INTERFACE
''' 
def send_move(self, from_, to_)
def on_move(self, state)
def on_game_over(self, state):
def start(self):
'''
'''
 Json send in the def on_move(self, state)
{
    "board"             : STRING,
    "enpassant"         : COORDENADA,
    "who_moves"         : -1 OU 1,
    "bad_move"          : BOOLEAN,
    "white_infractions" : INTEGER,
    "black_infractions" : INTEGER,
    "winner"            : -1, 0 OU 1,
    "50moves"           : BOOLEAN,
    "draw"              : BOOLEAN
}

'''

def make_value(color):

	def value(theBoard):
		whites = 0
		blacks = 0
		maior_dist_w = -sys.maxint
		maior_dist_b = 0
		pos = 0
		wr = 0 
		br = 0
		wb = 0
		bb = 0
		wp = 0
		bp = 0
		for c in theBoard:
			if c == "p":
				#(x , y) = pos_to_coord(pos)
				(x , y) = (pos / 12 , pos % 10)
				if (x-10) > maior_dist_w:
					#print (x-10)  , "update" , x , "x"
					maior_dist_w = x-10
			if c == "P":
				(x , y) = (pos / 12 , pos % 10)
				if (10-x) > maior_dist_b:
					maior_dist_b = 10-x
			wr = wr + 1 if c == 'r' else wr
			br = br + 1 if c == 'R' else br
			wb = wb + 1 if c == 'b' else wb
			bb = bb + 1 if c == 'B' else bb
			wp = wp + 1 if c == 'p' else wp
			bp = bp + 1 if c == 'P' else bp
			
			if c.islower(): 
				whites += 1
			if c.isupper(): 
				blacks += 1
			pos += 1
		
		if(color == WHITE):
			material = 0.5*(wr - br)/float(2)  + 0.20*(wb - bb)/float(2) + 0.05*(bb - wp)/float(12)
		else:
			aux = maior_dist_w
			maior_dist_w = maior_dist_b
			maior_dist_b = aux
			material = 0.5*(br - wr)/float(2) + 0.20*(bb - wb)/float(2) + 0.05*(wp - bp)/float(12)
		
		delta = (whites - blacks) if color == WHITE else (blacks - whites)
		#print 0.5*(material/float(3)) + 0.5*((maior_dist_w/float(8)) - (maior_dist_b/float(8)))
		#print (10 + maior_dist_w)
		return 0.8*(material/float(3)) + 0.2*(( ( 10 +  maior_dist_w)/float(10)) - (maior_dist_b/float(10)))
		#return material + maior_dist * maior_dist
	
	return value
	
def max_move(this_board, value, my_color, depth, alpha , beta):

	if depth < 1:
		return (value(this_board) , this_board)
	else:

		best_move = (-sys.maxint , this_board)
		board  = Board(this_board)

		pieces = board.get_piece_lst(my_color)
		aux_lst = [p.generate() for p in pieces]
		move_lst = [item for sublist in aux_lst for item in sublist]
		#print "max's board" , "depth" , depth , "possible moves" , len(move_lst) , "my color" , my_color

		for move in move_lst:
			current_best = min_move(move, make_value(my_color * (-1)), my_color * (-1), depth-1, alpha , beta)
	
			if (current_best[0] > best_move[0]):
				best_move = (current_best[0] , move)
			
			if(best_move[0] >= beta):
				return best_move
			
			alpha = max(alpha, best_move[0])
			
	return best_move
			
def min_move(this_board, value, my_color , depth , alpha, beta):
	
	best_move = (sys.maxint, this_board) # empty
	
	#Gerando filhos
	board  = Board(this_board)
	pieces = board.get_piece_lst((-1) * my_color)
	aux_lst = [p.generate() for p in pieces]
	move_lst = [item for sublist in aux_lst for item in sublist]
	#print "min's board" , "depth",  depth , "possible moves" , len(move_lst)  , "my color" , my_color

	for move in move_lst:
		current_best = max_move(move,make_value(my_color * (-1)), my_color * (-1), depth-1, alpha, beta)
		if (current_best[0] < best_move[0]):
			best_move = (current_best[0] , move)
		
		if(best_move[0] <= alpha):
			return best_move
			
		beta = min(beta, best_move[0])
	return best_move
 
def minimax(aBoard, color):
	value = make_value(color)
	return max_move(aBoard, value, color, 4, -sys.maxint, sys.maxint)



def str_case(str):
	aux = ""
	for c in str:
		if c.islower() and c != '*' and c != '.':
			print c
			aux = aux + c.upper()
		if c.isupper() and c != '*' and c != '.':
			aux = aux + c.lower()
		if c == '*' or c == '.':
			aux = aux + c 
		
	return "".join(aux)

def str_mirror(str):
	return(inv(str[0:10])
	+ inv(str[10:20])
	+ inv(str[20:30])
	+ inv(str[30:40])
	+ inv(str[40:50])
	+ inv(str[50:60])
	+ inv(str[60:70])
	+ inv(str[70:80])
	+ inv(str[80:90])
	+ inv(str[90:100])
	+ inv(str[100:110])
	+ inv(str[110:120]) )
	
	
def print_mirror_board(str):
	print inv(str[0:10])
	print inv(str[10:20])
	print inv(str[20:30])
	print inv(str[30:40])
	print inv(str[40:50])
	print inv(str[50:60])
	print inv(str[60:70])
	print inv(str[70:80])
	print inv(str[80:90])
	print inv(str[90:100])
	print inv(str[100:110])
	print inv(str[110:120])

def inv(str):
	return str[::-1]
# BOT
class CleverBot(LiacBot):
	name = 'CleverBot'

	def __init__(self):
		super(CleverBot, self).__init__()
		self.last_move = None
		self.counter = 0

	def on_move(self, state): # state = json
	
		the_board = str_mirror(str_reverse(enrich_str(state['board'])))
		my_color = state['who_moves']
		board = Board(the_board)

		if state['bad_move']:
			print state['board']
			raw_input()
	
		if(self.counter == 0):
			(f,b) = ((1,3),(3,3)) if my_color == WHITE else ((6,3),(5,3))
		elif(self.counter == 1):
			(f,b) = ((1,6),(3,6)) if my_color == WHITE else ((6,6),(5,6))
		else:
			the_score , the_move = minimax(the_board, my_color)
			(f , b )= diff(derich_str(the_board), derich_str(the_move), my_color)
		self.counter += 1 
		print f , b
		self.send_move(f,b)


	def on_game_over(self, state):
		self.counter = 0
		print 'Game Over.'

# ==============================================================

#Inverte o tabuleiro fazendo o oponente ter visao de jogador
def str_reverse(str):
	return "".join(map(lambda x : x.upper() if x.islower() else x.lower(), str[::-1]))

def pos_to_coord(aNumber):
	return (aNumber / 8 , aNumber % 8)


def diff(str1 , str2 , color):
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
	
	if (str2[f].islower()) and str2[f].isalpha() and color == WHITE:
		#print "swap"
		aux = t
		t = f
		f = aux
	
	if (str2[f].isupper()) and str2[f].isalpha() and color == BLACK:
		#print "swap BLACK"
		aux = t
		t = f
		f = aux
		
	print f , t
	return pos_to_coord(f) , pos_to_coord(t)


class Board(object):
	def __init__(self, state):
		self.state = state

	def get_piece_lst(self,color):
		piece_lst = []
		str_pos = 0
		state = self.state
		def test(c):
			if color == BLACK : 
				return c.isupper()
			else:
				return c.islower()
		
		for char in state:
			if char != '.' and char != '*' and test(char):
				#print char
				piece_lst.append( self.select_piece(char,state, str_pos, color))
			str_pos += 1
		
		piece_lst.sort(key = lambda x: x.precedence)
		return piece_lst

	def select_piece(self,char, board, str_pos, color):
	
		PIECES = {
			'r': Rook,
			'p': Pawn,
			'b': Bishop
			#'q': Queen,
			#'n': Knight,
		}
		the_piece = PIECES[char.lower()]

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
		if other_piece == '.' or other_piece == '*':
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
		self.precedence = 1

	def __str__(self):
		print board

	def	generate(self):
		board = list(self.board)
		color = self.piece_color
		pos = self.pos
		board_lst = []
		
		if (color == BLACK):
			#print "black move"
			board = list(str_reverse("".join(board)))
			#print_board("".join(board))
			pos = 119 - pos
			#print board[pos]

		#print_board("".join(board))
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
		self.precedence = 3
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
		self.precedence = 2
		
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

def derich_str(str):
	return (str[21:29] 
	+ str[31:39] 
	+ str[41:49]
	+ str[51:59]
	+ str[61:69]
	+ str[71:79]
	+ str[81:89]
	+ str[91:99] )
	
def print_derich_str(str):
	print str[21:29] 
	print str[31:39] 
	print str[41:49]
	print str[51:59]
	print str[61:69]
	print str[71:79]
	print str[81:89]
	print str[91:99]
	
# ==============================================================

if __name__ == '__main__':
    color = 0
    port = 50100
	

    if len(sys.argv) > 1:
        if sys.argv[1] == 'black':
            color = 1
            port = 50200

    bot = CleverBot()
    bot.port = port

    bot.start()

