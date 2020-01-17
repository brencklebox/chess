import chess
import chess.engine
from lib import minimax_model, stockfish_model, common


if __name__ == "__main__":

    minimax_player = minimax_model.minimaxPlayer(depth=2)
    stockfish_player = stockfish_model.stockfishPlayer(time=0.01, skill=1)
    result = common.play_game(minimax_player, stockfish_player, visual="svg", pause=0.001)
    print(result)
