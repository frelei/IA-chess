import time
import sys
import random

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

# BOT
class CleverBot(LiacBot):
    name = 'CleverBot'

    def __init__(self):
        super(CleverBot, self).__init__()
        self.last_move = None

    def on_move(self, state): # state = json
        print 'Generating a move...',
        board = Board(state)

        if state['bad_move']:
            print state['board']
            raw_input()

        pieces = board.get_piece_lst(state)
	moves = random.choice(pieces).generate()
       	the_move = random.choice(moves)
        #self.last_move = move
        #print move
        self.send_move(diff(state['board'], the_move))

    def on_game_over(self, state):
        print 'Game Over.'

# ==============================================================

#Inverte o tabuleiro fazendo o oponente ter visao de jogador
def str_reverse(str):
	return "".join(map(lambda x : x.upper() if x.islower() else x.lower(), str[::-1]))

def pos_to_coord(aNumber):
	#return (aNumber / 8 , aNumber % 8)
	return ((aNumber / 12) - 1 , (aNumber % 10) - 1)

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

