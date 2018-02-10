# coding: utf-8

import string
import random
# signum function
sign = lambda x: -1 if x < 0 else 0 if x==0 else 1
DIGITS = ['0','1','2','3','4','5','6','7','8','9']

class Game:
    WHITE_PIECES = ['P', 'N', 'B', 'R', 'Q', 'K']
    BLACK_PIECES = ['p', 'n', 'b', 'r', 'q', 'k']
    TICKS_CAP = 100
    def __init__(self, fen = 'none'):
        self.board = Board()
        self.winner = 'unknown'
        self.ticks = 0
        if fen == 'none':
            self.active_player = 'unknown'
            self.castling_availability = []
            self.en_passant = '-'
            self.turn = 1
        else:
            pos, active, c_a, e_p, turn = fen.split(' ')
            self.board.read_position_from(pos)
            self.active_player = active
            self.castling_availability = list(c_a)
            self.en_passant = e_p
            self.turn = int(turn)
    def ended(self):
        return self.winner != 'unknown'
    def restart(self, starting_position = 'standard'):
        black = 'rnbqkbnr'
        white = 'RNBQKBNR'
        if starting_position == 'random':
            black = list(black)
            random.shuffle(black)
            black = string.join(black,'')
            white = list(white)
            random.shuffle(white)
            white = string.join(white,'')
            self.castling_availability = []
        else:
            self.castling_availability = ['K','Q','k','q']
        self.board.read_position_from(black+'/pppppppp/8/8/8/8/PPPPPPPP/'+white)
        self.active_player = 'white'
        self.en_passant = '-'
        self.halfturns = 0
        self.turn = 1

    @staticmethod
    def matches(a,b):
        if b == 'white':
            if a in Game.WHITE_PIECES:
                return 1
        if b == 'black':
            if a in Game.BLACK_PIECES:
                return 1
        return 0

    # return info availible to the player of the chosen color
    def info(self, color):
        board = self.board
        my = {_:board[_] for _ in board if self.color(_) == color}
        his ={_:board[_] for _ in board if self.color(_) != color}
        vis = my.copy()
        for x in my:
            for y in his:
                if Piece(board, x).can_capture(y) or Piece(board, x).can_move(y):
                    vis[y] = his[y]
        v_e_p = '-'
        e_p = self.en_passant
        if e_p != '-':
            p = self.pawn_en_passant()
            for x in my:
                if my[x] in ['P','p'] and Piece(board,x).can_capture(e_p):
                    v_e_p = e_p
                    vis[p] = board[p]
        pos = Board.make_fen(vis)
        active = self.active_player
        c_a = [_ for _ in self.castling_availability if Game.matches(_,color)]
        c_a = string.join(c_a, '')
        if c_a == '': c_a = '-'
        turn = str(self.turn)
        return string.join([pos, active, c_a, v_e_p, turn])
    def pawn_en_passant(self):
        e_p = self.en_passant
        if e_p == '-':
            return '-'
        return e_p[0]+('5' if e_p[1] == '6' else '4')
    def make_move(self, move):
        # take care of:
        # 1) castling +
        # 2) pawn promotion +
        # 3) updating en_passant +
        # 4) castling availability +
        # 5) update ticks
        # 6) winning +
        # 7) swap active color +
        # 8) update turns +

        #dump all game attr to local var
        color = self.active_player
        c_a = self.castling_availability
        e_p = self.en_passant
        ticks = self.ticks + 1
        turn = self.turn
        board = self.board
        # new en passant
        n_e_p = '-'
        if not self.can_move(move):
            print 'illegal move',move
            return
        # 1) castling
        #king side castle
        if move == 'O-O':
            if color == 'white':
                board.move('e1','g1')
                board.move('h1','f1')
                c_a = [_ for _ in c_a if _ not in ['K','Q']]
            if color == 'black':
                board.move('e8','g8')
                board.move('h8','f8')
                c_a = [_ for _ in c_a if _ not in ['k','q']]
        #queen side castle
        elif move == 'O-O-O':
            if color == 'white':
                board.move('e1','c1')
                board.move('a1','d1')
                c_a = [_ for _ in c_a if _ not in ['K','Q']]
            if color == 'black':
                board.move('e8','c8')
                board.move('a8','d8')
                c_a = [_ for _ in c_a if _ not in ['k','q']]
        else:
            # parse the move into start pos and end pos
            sp,ep = move[0:2],move[2:4]
            # moving piece
            mp = Piece(board, sp)
            taken = board[ep]
            board.move(sp,ep)
            # 2) pawn promotion
            # 3) updating en_passant
            if mp.pic in ['p', 'P']:
                ticks = 0
                # capturing pawn en passant
                if ep == e_p:
                    pep = self.pawn_en_passant()
                    taken = board[pep]
                    del board[pep]
                if color == 'white':
                    # updating en passant
                    if sp[1] == '2' and ep[1] == '4':
                        n_e_p = sp[0]+'3'
                    # pawn promotion
                    if ep[1] == '8':
                        prom = 'Q' if len(move) < 6 else move[5]
                        if prom not in Game.WHITE_PIECES or\
                        prom == 'P':
                            prom = 'Q'
                        board[ep] = prom
                if color == 'black':
                    if sp[1] == '7' and ep[1] == '5':
                        n_e_p = sp[0]+'6'
                    if ep[1] == '1':
                        prom = 'q' if len(move) < 6 else move[5]
                        if prom not in Game.BLACK_PIECES or\
                        prom == 'p':
                            prom = 'q'
                        board[ep] = prom
            # 4) castling availability
            if color == 'white':
                if mp.pic == 'K':
                    c_a = [_ for _ in c_a if _ not in ['K','Q']]
                if mp.pic == 'R' and sp == 'a1':
                    c_a = [_ for _ in c_a if _ != 'Q']
                if mp.pic == 'R' and sp == 'h1':
                    c_a = [_ for _ in c_a if _ != 'K']
            if color == 'black':
                if mp.pic == 'k':
                    c_a = [_ for _ in c_a if _ not in ['k','q']]
                if mp.pic == 'r' and sp == 'a8':
                    c_a = [_ for _ in c_a if _ != 'q']
                if mp.pic == 'r' and sp == 'h8':
                    c_a = [_ for _ in c_a if _ != 'k']
            # 5) update ticks
            # 6) winning
            if taken != Board.EMPTY_SPACE:
                ticks = 0
                if taken in ['K', 'k']:
                    self.winner = color
                    color = 'none'
        if ticks >= Game.TICKS_CAP:
            self.winner = 'draw'
            color = 'none'
        # 7) swap active color
        color = 'white' if color == 'black' else \
        'black' if color == 'white' else color
        # 8) update turns
        if color == 'white':
            turn += 1
        self.active_player = color
        self.castling_availability = c_a
        self.en_passant = n_e_p
        self.ticks = ticks
        self.turn = turn
    def can_move(self, move):
        #dump all game attr to local var
        color = self.active_player
        c_a = self.castling_availability
        e_p = self.en_passant
        ticks = self.ticks
        turn = self.turn
        board = self.board
        #king side castle
        if move == 'O-O':
            if color == 'white':
                if 'f1' in board or 'g1' in board:
                    return 0
                return 'K' in c_a
            if color == 'black':
                if 'f8' in board or 'g8' in board:
                    return 0
                return 'k' in c_a
            return 0
        #queen side castle
        if move == 'O-O-O':
            if color == 'white':
                if 'b1' in board or 'c1' in board or 'd1' in board:
                    return 0
                return 'Q' in c_a
            if color == 'black':
                if 'b8' in board or 'c8' in board or 'd8' in board:
                    return 0
                return 'q' in c_a
            return 0
        # parse the move into start pos and end pos
        sp,ep = move[0:2],move[2:4]
        # cannot play in place
        if sp == ep:
            return 0
        # can only move our own pieces
        if self.color(sp) != color:
            return 0
        # moving piece
        mp = Piece(board, sp)
        # cannot eat our own pieces
        if self.color(ep) == color:
            return 0
        # en passant
        if ep == e_p and mp.pic in ['p', 'P']:
            return mp.can_capture(ep)
        if self.color(ep) == 'none':
            return mp.can_move(ep)
        else:
            return mp.can_capture(ep)
    def color(self, pos):
        piece = self.board[pos]
        if piece in Game.WHITE_PIECES:
            return 'white'
        if piece in Game.BLACK_PIECES:
            return 'black'
        return 'none'

class Piece:
    def __init__(self, board, pos):
        self.pic = board[pos]
        self.pos = pos
        self.file, self.rank = pos[0], pos[1]
        self.board = board
    # returns if this piece can move to the  given position
    # assuming there is nothing there
    def can_move(self, pos):
        offset = dx,dy = Board.offset(self.pos, pos)
        if self.pic == 'P':
            if offset == (0,1):
                if self.can_be_dragged_to(pos):
                    return 1
            if offset == (0,2) and self.rank == '2':
                if self.can_be_dragged_to(pos):
                    return 1
        if self.pic == 'p':
            if offset == (0,-1):
                if self.can_be_dragged_to(pos):
                    return 1
            if offset == (0,-2) and self.rank == '7':
                if self.can_be_dragged_to(pos):
                    return 1
        if self.pic in ['N', 'n']:
            offset = map(abs, offset)
            offset.sort()
            return offset == [1,2]
        if self.pic in ['K', 'k']:
            offset = map(abs, offset)
            return offset[0] < 2 and offset[1] < 2
        if self.pic in ['Q', 'q']:
            offset = map(abs, offset)
            if offset[0] == offset[1] or offset[0]*offset[1] == 0:
                return self.can_be_dragged_to(pos)
        if self.pic in ['R', 'r']:
            offset = map(abs, offset)
            if offset[0]*offset[1] == 0:
                return self.can_be_dragged_to(pos)
        if self.pic in ['B', 'b']:
            offset = map(abs, offset)
            if offset[0] == offset[1]:
                return self.can_be_dragged_to(pos)
        return 0
    # returns if this piece can capture the given position
    # assuming there is an enemy piece there
    def can_capture(self, pos):
        offset = dx,dy = Board.offset(self.pos, pos)
        if self.pic == 'P':
            return offset == (1,1) or offset == (-1,1)
        if self.pic == 'p':
            return offset == (1,-1) or offset == (-1,-1)
        return self.can_move(pos)
    # returns if this piece can be dragged to the given position
    # (in a straight way)
    def can_be_dragged_to(self, pos):
        for p in Board.get_straight_path(self.pos, pos):
            if self.board[p] != Board.EMPTY_SPACE:
                return 0
        return 1

class Board(dict):
    RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']
    FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    EMPTY_SPACE = '.'
    # @staticmethod
    # def get_coordinates(pos):
    #     return pos[0],pos[1]
    # @staticmethod
    # def get_position(x,y):
    #     return x+y
    # make an iterator through a striaght path from sp to ep
    # @staticmethod
    # def file(pos):
    #     return pos[0]
    # @staticmethod
    # def rank(pos):
    #     return pos[1]
    @staticmethod
    def get_straight_path(sp, ep):
        while 1:
            d = map(sign, Board.offset(sp,ep))
            np = map(lambda a,da: chr(ord(a)+da), sp, d)
            if np == list(ep): return
            sp = np[0]+np[1]
            yield sp
    @staticmethod
    def offset(p1, p2):
        return tuple(map(lambda a,b: ord(b)-ord(a), p1, p2))
    def move(self, sp, ep):
        if self[sp] != Board.EMPTY_SPACE:
            self[ep] = self[sp]
            del self[sp]
    def read_position_from(self, fen):
        self.clear()
        ranks = iter(fen.split('/'))
        tick = 0
        for r in reversed(Board.RANKS):
            cur = iter(ranks.next())
            for f in Board.FILES:
                if tick:
                    tick -= 1
                    continue
                symb = cur.next()
                if symb in DIGITS[1:]:
                    tick = ord(symb) - ord('1')
                    continue
                self[f+r] = symb
    @staticmethod
    def make_fen(pos):
        fen = []
        for r in reversed(Board.RANKS):
            cur = ''
            tick = 0
            for f in Board.FILES:
                if f+r not in pos:
                    tick += 1
                    continue
                if tick != 0:
                    cur += str(tick)
                    tick = 0
                cur += pos[f+r]
            if tick != 0:
                cur += str(tick)
            fen += [cur]
        return string.join(fen,'/')
    def __init__(self, fen = '8/8/8/8/8/8/8/8'):
        self.read_position_from(fen)
    def __getitem__(self, pos):
        if pos not in self.__dict__:
            return Board.EMPTY_SPACE
        return self.__dict__[pos]
    def __delitem__(self, pos):
        if pos in self: del self[pos]
    # def __repr__(self):
        #TODO mb change this to return FEN config
        # pos = []
        # for r in reversed(Board.RANKS):
        #     cur = ''
        #     tick = 0
        #     for f in Board.FILES:
        #         if f+r not in figures:
        #             tick += 1
        #             continue
        #         if tick != 0:
        #             cur += str(tick)
        #             tick = 0
        #         cur += figures[f+r]
        #     if tick != 0:
        #         cur += str(tick)
        #     pos += [cur]
        # return string.join(pos,'/')
    def __str__(self):
        s = ''
        for r in reversed(Board.RANKS):
            for f in Board.FILES:
                if f+r in self:
                    s += self[f+r]
                else:
                    s += Board.EMPTY_SPACE
            s += '\n'
        return s


# Forsyth-Edwards Notation (FEN)

# 1) Piece placement (from white's perspective).
# Each rank is described, starting with rank 8 and ending with rank 1;
# within each rank, the contents of each square are described
# from file "a" through file "h". Following the Standard Algebraic Notation,
# each piece is identified by a single letter taken from
# the standard English names
# White pieces are designated using upper-case letters ("PNBRQK")
# while black pieces use lowercase ("pnbrqk").
# Empty squares are noted using digits 1 through 8 (the number of empty squares),
# and "/" separates ranks.

# 2) Active colour.
# "w" means White moves next, "b" means Black.

# 3) Castling availability.
# If neither side can castle, this is "-".
# Otherwise, this has one or more letters: "K" (White can castle kingside),
# "Q" (White can castle queenside),
# "k" (Black can castle kingside), and/or "q" (Black can castle queenside).
# This only keeps track of whether king/rooks moved, so at the start of the game
# all castlings are availible, though not executable.

# 4) En passant target square in algebraic notation.
# If there's no en passant target square, this is "-".
# If a pawn has just made a two-square move, this is the position "behind" the pawn.
# Normally this is recorded regardless of whether there is a pawn
# in position to make an en passant capture, but not in our case.

# 5) Halfmove clock: This is the number of halfmoves since the last capture
# or pawn advance. This is used to determine if a draw can be claimed
# under the fifty-move rule.
# We do not share this cuz it gives away info if a pawn was moved.

# 6) Fullmove number: The number of the full move.
# It starts at 1, and is incremented after Black's move.
