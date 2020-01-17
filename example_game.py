import chess
import chess.engine
from lib import minimax_model, stockfish_model, common


if __name__ == "__main__":

    minimax_player = minimax_model.minimax_player
    minimax_options = {"depth": 2, "color": chess.WHITE}

    stockfish_player = stockfish_model.stockfish_player
    stockfish_options = {"path": stockfish_model.STOCKFISH_PATH,
                        "time": 0.01,
                        "skill": 1}

    result = common.play_game(minimax_player, stockfish_player, minimax_options, stockfish_options, visual="svg", pause=0.001)
    print(result)