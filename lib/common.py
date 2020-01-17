#!/usr/bin/env python3

import chess
import re
import os
import time
import datetime
import shutil
import cairosvg
import subprocess


def tryint(s):
    """Convert item to an integer if possible.
    Parameters:
        s (str): string to try to convert
    Returns:
        s (int or string): int of string if possible else input string
    """
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    """Turn a string into a list of string and number chunks.
    example:
        "z23a" -> ["z", 23, "a"]
    Parameters:
        s (str): string to split
    Returns:
        list[str, int]: list of mixed type containing string and numbers, chunked
    """
    splitlist = [tryint(c) for c in re.split('([0-9]+)', s)]
    cleanlist = list(filter(lambda a: a != '', splitlist))
    return cleanlist


def sort_nicely(l):
    """Sort the given list in the way that humans expect.
    Parameters:
        l (list[str]): unsorted list
    Returns:
        l (list[str,int]): list sorted by alphanumerics
    """
    return sorted(l, key=alphanum_key)


def cleanup(path):
        """Remove folder and its contents.
        Removes graph-associated temporary folder and all contents
        from filesystem.
        """
        shutil.rmtree(path)


def save_animation(directory, anim_file_name, fps=2):
        """Save output of run with graph into an animation.
        Saves an animation from using ffmpeg, based on graph output.
        Requres folder of ``.png`` such as those generated from
        ``ProcessGraph.run()`` in order to create the animation. Cleans
        up after creating the animation.
        Parameters:
            anim_file_name (str): name of the file to save
            fps (int, optional): frames-er second of the resulting animation
        """
        os.chdir(directory)
        filedir = os.getcwd()
        files = os.listdir(filedir)
        filelist = sort_nicely(files)
        for i, filename in enumerate(filelist):
            _, extension = os.path.splitext(filename)
            new_filename = str(i) + extension
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
        with open(os.devnull, 'w') as fnull:
            subprocess.call([
                'ffmpeg', '-y',
                          '-framerate', str(fps),
                          '-i', '%d.png',
                          '-pix_fmt', 'yuv420p',
                          '-vf', "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                '../' + anim_file_name + '.mp4'
            ], stdout=fnull, stderr=subprocess.STDOUT)
        os.chdir("../")
        cleanup(directory)


def who(player):
    return "White" if player == chess.WHITE else "Black"


def play_game(player1, player2, visual="svg", pause=0.1):
    """Generic game playing method. Player1 is white.

    parameters:
        player1 (obj) -- model object that takes board and options, has 'play' method
        player2 (obj) -- model object that takes board and options, has 'play' method
        visual (str) --  "simple" | "svg" | None
        pause (float) -- pause between moves
    
    returns:
        result (str) -- game result
        msg (str) -- game result message
        board (chess.Board) -- chess board object
    """
    use_svg = (visual == "svg")
    print_result = (visual == "simple")
    board = chess.Board()
    if use_svg:
        save_path = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(save_path)

    # play the game
    try:
        move_counter = 1
        while not board.is_game_over(claim_draw=True):
            if board.turn == chess.WHITE:
                uci = player1.play(board)
            else:
                uci = player2.play(board)
            name = who(board.turn)
            board.push_uci(uci)
            if visual is not None:
                if use_svg:
                    filepath = os.path.join(save_path, str(move_counter)+'.png')
                    cairosvg.surface.PNGSurface.convert(bytestring=str(board._repr_svg_()),write_to=filepath)
                if print_result:
                    print("Move", move_counter, "--", name, "plays", uci)
            time.sleep(pause)
            move_counter += 1
    # end conditions
    except KeyboardInterrupt:
        msg = "Game interrupted!"
        return (None, msg, board)
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + who(not board.turn) + " wins!"
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif board.can_claim_draw():
        msg = "draw: claim"
    if visual is not None:
        print(msg)
    if use_svg:
        save_animation(save_path, "animation", fps=2)
    player1.quit()
    player2.quit()
    return (result, msg, board)
    