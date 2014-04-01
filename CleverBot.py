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


# BOT
class CleverBot(LiacBot):
    name = 'CleverBot'

    def __init__(self):
        super(CleverBot, self).__init__()
        self.last_move = None

    def on_move(self, state):
        print 'Generating a move...',
        board = Board(state)

        if state['bad_move']:
            print state['board']
            raw_input()

        moves = board.generate()

        move = random.choice(moves)
        self.last_move = move
        print move
        self.send_move(move[0], move[1])

    def on_game_over(self, state):
        print 'Game Over.'


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
