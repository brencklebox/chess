import math
import chess
import chess.engine
from lib import minimax_model, stockfish_model, common
import argparse


STOCKFISH_THINK_TIME = 1
STOP_GAMES = 25


def elo_win_probability(rating1, rating2):
    """Calculate the probability of player1 beating player2 given current ELO."""
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


def EloRating(Ra, Rb, win):
    """Update ELO.

    parameters:
        Ra -- rating, player A
        Rb -- rating, player B
        win -- decision for player A
    returns:
        Ea -- new ELO of player A
        Eb -- new ELO of player B
    """

    Pb = elo_win_probability(Ra, Rb)
    Pa = elo_win_probability(Rb, Ra)

    if win == 1:
        Ea = Ra + 40 * (1 - Pa)
        Eb = Rb + 40 * (0 - Pb)
    else:
        Ea = Ra + 40 * (0 - Pa)
        Eb = Rb + 40 * (1 - Pb)
    Ea = round(Ea, 0)
    Eb = round(Eb, 0)
    return (Ea, Eb)


def is_win_benchmark(decision, white):
    """Determine if model defeats benchmark in test game.

    Parameters:
        decision (bool): decision of game
        white (bool): is model playing white
    Returns:
        wl (str): win | loss
    """
    wl = None
    white_white_win = decision & white
    black_black_win = (decision == False) & (white == False)
    if white_white_win | black_black_win:
        wl = "win"
    else:
        wl = "loss"
    return wl


def update_elo_benchmark(results, elo):
    """Calculate update for ELO from game result.
    
    Parameters:
        results(dict or list): list of results to use for update, requires keys:
            white -- whether model played white
            decision -- whether white won the game
            skill -- skill played by benchmark model
    Returns:
        elo (int) -- updated elo value
    """
    if ~isinstance(results, list):
        results = [results]
    for result in results:
        benchmark_skill = stockfish_model.STOCKFISH_LEVELS[result["skill"]]
        if result["white"]:
            if result["decision"][0] == True:
                ratings = EloRating(elo, benchmark_skill, 1)
            elif result["decision"][0] == False:
                ratings = EloRating(elo, benchmark_skill, 0)
        else:
            if result["decision"][0] == True:
                ratings = EloRating(elo, benchmark_skill, 0)
            elif result["decision"][0] == False:
                ratings = EloRating(elo, benchmark_skill, 1)
        elo = ratings[0]
        print("elo updated to:", elo)
    return elo


def benchmark_elo(model, elo=1000, games_per_skill=10):
    """Subroutine for running ELO benchmark tests on model.
    
    Parameters:
        model(player): model function to test
        modelargs(dict): options for model
        elo(int): initial ELO rating to update
        games_per_skill(int): number of games to iterate per skill level for benchmark
    
    Returns:
        results (dict): outcome of benchmark games
        new_elo (int): updated ELO
    """
    results = []
    idx = 0
    new_elo = elo
    if ~isinstance(new_elo, int):
        new_elo = int(new_elo)
    for skill in range(20):
        try:
            for game in range(games_per_skill):
                print("playing game", idx + 1, "of", games_per_skill * 20)
                white = game % 2 == 0
                benchmark_player = stockfish_model.stockfishPlayer(
                    time=STOCKFISH_THINK_TIME, skill=skill
                )
                if white:
                    decision = common.play_game(model, benchmark_player, visual=None)
                else:
                    decision = common.play_game(benchmark_player, model, visual=None)
                win = is_win_benchmark(decision[0], white)
                result = {"skill": skill, "white": white, "model_win": win, "decision": decision}
                results.append(result)
                new_elo = update_elo_benchmark(result, new_elo)
                idx += 1
                # stop if last 10 were all losses
                stop = False
                if len(results) >= STOP_GAMES:
                    stop = True
                    for game in results[-STOP_GAMES:]:
                        if game["model_win"] == "win":
                            stop = False
                            break
                if stop:
                    break
        except KeyboardInterrupt:
            print("Measurement interrupted!")
            return None
        if stop:
            print("stopped early due to losses")
            break
    return results, new_elo


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", default=False, action="store_true", help="test the minimax model")
    parser.add_argument("-md", "--depth", type=int, default=3, help="depth of minimax")
    parser.add_argument("-e", "--elo", default=1000, help="initial ELO guess to use for model")
    args = parser.parse_args()

    if args.m:
        print("testing minimax")
        model = minimax_model.minimaxPlayer(depth=args.depth)
    else:
        print("testing stockfish")
        model = stockfish_model.stockfishPlayer()

    _, new_elo = benchmark_elo(model, elo=args.elo, games_per_skill=25)
    print("Estimated minimax ELO:", new_elo)
