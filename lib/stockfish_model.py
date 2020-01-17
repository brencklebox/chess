import chess
import chess.engine
import os


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


class stockfishPlayer:
    """Wrapper for stockfish player."""

    def __init__(self, time=0.1, skill=1):
        self.levels = STOCKFISH_LEVELS
        self.path = os.environ.get("STOCKFISH_PATH")
        self.time = time
        self.skill = skill
        self.engine = chess.engine.SimpleEngine.popen_uci(self.path)

    def play(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=self.time), options={"Skill Level": self.skill})
        return result.move.uci()
    
    def quit(self):
        self.engine.quit()
        return True
