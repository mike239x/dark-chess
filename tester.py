import sys
from chess import *
game = Game()
game.restart()
# game.restart(starting_position = 'random')

# print game.board
# print game.castling_availability

def make_moves(moves):
    for m in moves.split(' '):
        game.make_move(m)
        # print game.board, game.active_player, game.en_passant, game.turn

# en passant
# make_moves('e2e4 a7a5 e4e5 f7f5 e5f6')
# pawn capture & promotion
# make_moves('e2e4 d7d5 e4d5 e7e6 d5e6 d8d7 e6d7 a7a5 d7e8=Q')
# Efim Bogoljubov vs Alexander Alekhine
# "The Triple Queen Sacrifice"
make_moves('d2d4')
make_moves('f7f5 c2c4 g8f6 g2g3 e7e6')
make_moves('f1g2')
make_moves('f8b4 c1d2 b4d2 b1d2 b8c6')
make_moves('g1f3')
# # king side castle
make_moves('O-O')
# # make_moves('e8g8 e1g1')
make_moves('O-O')
make_moves('d7d6 d1b3 g8h8 b3c3 e6e5')
make_moves('e2e3 a7a5 b2b3 d8e8 a2a3 e8h5')
make_moves('h2h4 f6g4 f3g5 c8d7 f2f3 g4f6')
#
make_moves('f3f4 e5e4 f1d1 h7h6 g5h3 d6d5')
# make_moves('d2f1 c6e7 a3a4 e7c6 d1d2 c6b4')


# make_moves('g2h1 h5e8 d2g2 d5c4 b3c4 d7a4')
# make_moves('h3f2 a4d7 f1d2 b7b5 f2d1 b4d3')
# make_moves('a1a5 b5b4 a5a8 b4c3 a8e8 c3c2')
# make_moves('e8f8 h8h7 d1f2 c2c1=q d2f1 d3e1')
# make_moves('g2h2 c1c4 f8b8 d7b5 b8b5 c4b5')
# make_moves('g3g4 e1f3 h1f3 e4f3 g4f5 b5e2')
# make_moves('d4d5 h7g8 h4h5 g8h7 e3e4 f6e4')
# make_moves('f2e4 e2e4 d5d6 c7d6 f5f6 g7f6')
# make_moves('h2d2 e4e2 d2e2 f3e2 g1f2 e2f1=q')
# make_moves('f2f1 h7g7 f1e2 g7f7 e2e3 f7e6')
# make_moves('e3e4 d6d5')
# make_moves('')
print game.board, game.active_player, game.en_passant, game.turn
b = Game(fen = game.info('black'))
w = Game(fen = game.info('white'))
print b.board
print w.board
sys.exit(0)
