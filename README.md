# darkchess
server.py

  The game server. The only thing that knows the true state of the board.
  Initializes game, sends responses to players, updates the game.

chess.py

  The game module. Contains Game, Board and Piece classes. Contains all the info on how can pieces move.
  Also provides which info can each of the players see.

client.py

  Yet to be done. I think this will be the game itself (with GUI and such).
protocol.py

  Contains some basic info on how to communicate. Maybe I'll make this part a bit more convoluted, but right now it just has the names for commands that client and server can send each other.

TODO list

  My list of things to do.

tester.py and temp folder

  Some testing files. Will be removed eventually.


mike239x, Feb 2018
