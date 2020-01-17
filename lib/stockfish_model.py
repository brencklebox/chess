import chess
import chess.engine


STOCKFISH_LEVELS = {0: 1231,
                    1: 1341,
                    2: 1443,
                    3: 1538,
                    4: 1678,
                    5: 1823,
                    6: 1881,
                    7: 1976,
                    8: 2067,
                    9: 2129,
                    10: 2221,
                    11: 2320,
                    12: 2406,
                    13: 2483,
                    14: 2571,
                    15: 2657,
                    16: 2761,
                    17: 2815,
                    18: 2872,
                    19: 2905,
                    20: 3450}

STOCKFISH_PATH = "/Users/brenckle mark/Downloads/stockfish-10-mac/Mac/stockfish-10-64"

def stockfish_player(board, path=STOCKFISH_PATH, time=0.1, skill=1):
    engine = chess.engine.SimpleEngine.popen_uci(path)
    result = engine.play(board, chess.engine.Limit(time=time), options={"Skill Level": skill})
    engine.quit()
    return result.move.uci()