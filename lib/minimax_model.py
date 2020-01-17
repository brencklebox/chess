#!/usr/bin/env python3

import chess
import numpy as np

def evaluateBoard(board, color):
    """Board evaluation model for minimax."""
    score = 0
    score_map = {chess.PAWN: [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 
                              15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0,
                              11.0, 11.0, 12.0, 13.0, 13.0, 12.0, 11.0, 11.0, 
                              10.5, 10.5, 11.0, 12.5, 12.5, 11.0, 10.5, 10.5,
                              10.0, 10.0, 10.0, 12.0, 12.0, 10.0, 10.0, 10.0,
                              10.5, 9.5, 9.0, 10.0, 10.0, 9.0, 9.5, 10.5, 
                              10.5, 11.0, 11.0, 8.0, 8.0, 11.0, 11.0, 10.5, 
                              10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
                 chess.KNIGHT: [25.0, 26.0, 27.0, 27.0, 27.0, 27.0, 26.0, 25.0,
                                26.0, 28.0, 30.0, 30.0, 30.0, 30.0, 28.0, 26.0,
                                27.0, 30.0, 31.0, 31.5, 31.5, 31.0, 30.0, 27.0,
                                27.0, 30.5, 31.5, 32.0, 32.0, 31.5, 30.5, 27.0,
                                27.0, 30.0, 31.5, 32.0, 32.0, 31.5, 30.0, 27.0,
                                27.0, 30.5, 31.0, 31.5, 31.5, 31.0, 30.5, 27.0,
                                26.0, 28.0, 30.0, 30.5, 30.5, 30.0, 28.0, 26.0,
                                25.0, 26.0, 27.0, 27.0, 27.0, 27.0, 26.0, 25.0],
                 chess.BISHOP: [28.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0,
                                29.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 29.0, 
                                29.0, 30.0, 30.5, 31.0, 31.0, 30.5, 30.0, 29.0,
                                29.0, 30.5, 30.5, 31.0, 31.0, 30.5, 30.5, 29.0,
                                29.0, 30.0, 31.0, 31.0, 31.0, 31.0, 30.0, 29.0,
                                29.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 29.0,
                                29.0, 30.5, 30.0, 30.0, 30.0, 30.0, 30.5, 29.0,
                                28.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0],
                 chess.ROOK:  [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0,
                               50.5, 51.0, 51.0, 51.0, 51.0, 51.0, 51.0, 50.5,
                               49.5, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.5,
                               49.5, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.5,
                               49.5, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.5,
                               49.5, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.5,
                               49.5, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.5,
                               49.0, 49.0, 49.0, 50.5, 50.5, 50.0, 49.0, 49.0],
                 chess.QUEEN: [88.0, 89.0, 89.0, 89.5, 89.5, 89.0, 89.0, 88.0,
                               89.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 89.0,
                               89.0, 90.0, 90.5, 90.5, 90.5, 90.5, 90.0, 89.0,
                               89.5, 90.0, 90.5, 90.5, 90.5, 90.5, 90.0, 89.5,
                               90.0, 90.0, 90.5, 90.5, 90.5, 90.5, 90.0, 89.5,
                               89.0, 90.5, 90.5, 90.5, 90.5, 90.5, 90.0, 89.0,
                               89.0, 90.0, 90.5, 90.0, 90.0, 90.0, 90.0, 89.0,
                               88.0, 89.0, 89.0, 89.5, 89.5, 89.0, 89.0, 88.0],
                 chess.KING:  [897.0, 896.0, 896.0, 895.0, 895.0, 896.0, 896.0, 897.0,
                               897.0, 896.0, 896.0, 895.0, 895.0, 896.0, 896.0, 897.0,
                               897.0, 896.0, 896.0, 895.0, 895.0, 896.0, 896.0, 897.0,
                               897.0, 896.0, 896.0, 895.0, 895.0, 896.0, 896.0, 897.0,
                               898.0, 897.0, 897.0, 896.0, 896.0, 897.0, 897.0, 898.0,
                               899.0, 898.0, 898.0, 898.0, 898.0, 898.0, 898.0, 899.0,
                               902.0, 902.0, 900.0, 900.0, 900.0, 900.0, 902.0, 902.0,
                               902.0, 903.0, 901.0, 900.0, 900.0, 901.0, 903.0, 902.0]}
    for piecetype in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
        for pc_color in [chess.WHITE, chess.BLACK]:
            pcs = list(board.pieces(piecetype, pc_color))
            if pc_color == chess.WHITE:
                pc_map = list(reversed(score_map[piecetype]))
            else:
                pc_map = list(score_map[piecetype])
            for pc in pcs:
                if pc_color == color:
                    score += pc_map[pc]
                else:
                    score -= pc_map[pc]
        
    if board.turn == color:
        if board.is_checkmate():
            score -= 9999
        if board.is_check():
            score -= 10
    if board.turn != color:
        if board.is_stalemate():
            score -= 1000
        if board.can_claim_threefold_repetition():
            score -= 1000
    return score

def minimaxRoot(depth, board, color):
    """
    Returns the best minimax _move_ for a given board and player
    """
    bestMove = ""
    bestMoveScore = -9000
    
    for move in board.legal_moves:
        board.push_uci(move.uci())
        value = minimax(depth-1, board, -10000, 10000, color)
        board.pop()
        if value > bestMoveScore:
            bestMoveScore = value
            bestMove = move
        
    return bestMove.uci()


def minimax(depth, board, alpha, beta, color):
    """
    Returns the minimax _value_ for a given board and player
    """
    if depth == 0:
        return evaluateBoard(board, color)
    
    if color == chess.WHITE:
        bestMoveScore = -9000
        for move in board.legal_moves:
            board.push_uci(move.uci())
            bestMoveScore = np.max([bestMoveScore, 
                                    minimax(depth - 1, board, 
                                            alpha, beta, 
                                            chess.BLACK)])
            board.pop()
            alpha = np.max([alpha, bestMoveScore])
            if beta <= alpha:
                return bestMoveScore
        
        return bestMoveScore
    elif color == chess.BLACK:
        bestMoveScore = 9000
        for move in board.legal_moves:
            board.push_uci(move.uci())
            bestMoveScore = np.min([bestMoveScore, 
                                    minimax(depth - 1, board, 
                                            alpha, beta,
                                            chess.WHITE)])
            board.pop()
            beta = np.min([beta, bestMoveScore])
            if beta <= alpha:
                return bestMoveScore
        
    return bestMoveScore


def minimax_player(board, depth=1, color=chess.WHITE):
    """Play game with Minimax."""

    bestmove = minimaxRoot(depth, board, color)
    return bestmove