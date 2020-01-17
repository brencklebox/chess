#!/usr/bin/env python3

import chess
import numpy as np


class minimaxPlayer:

    def __init__(self, depth=3):
        self.depth = depth
        self.color = chess.WHITE

    def _findcolor(self, board):
        """determine current color of minimax."""
        self.color = board.turn

    def _evaluateBoard(self, board):
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
                    if pc_color == self.color:
                        score += pc_map[pc]
                    else:
                        score -= pc_map[pc]
        if board.turn == self.color:
            if board.is_checkmate():
                score -= 9999
            if board.is_check():
                score -= 10
        if board.turn != self.color:
            if board.is_stalemate():
                score -= 1000
            if board.can_claim_threefold_repetition():
                score -= 1000
        return score

    def _minimax(self, depth, board, alpha, beta):
        """
        Returns the minimax _value_ for a given board and player.
        """
        if depth == 0:
            return self._evaluateBoard(board)
        
        if self.color == chess.WHITE:
            bestMoveScore = -9000
            for move in board.legal_moves:
                board.push_uci(move.uci())
                new_depth = depth - 1
                bestMoveScore = np.max([bestMoveScore, 
                                        self._minimax(new_depth, board, 
                                                alpha, beta)])
                board.pop()
                alpha = np.max([alpha, bestMoveScore])
                if beta <= alpha:
                    return bestMoveScore
        
            return bestMoveScore
    
        elif self.color == chess.BLACK:
            bestMoveScore = 9000
            for move in board.legal_moves:
                board.push_uci(move.uci())
                new_depth = depth - 1
                bestMoveScore = np.min([bestMoveScore, 
                                        self._minimax(new_depth, board, 
                                                alpha, beta)])
                board.pop()
                beta = np.min([beta, bestMoveScore])
                if beta <= alpha:
                    return bestMoveScore
            
        return bestMoveScore


    def _minimaxRoot(self, board):
        """
        Returns the best minimax _move_ for a given board and player
        """
        bestMove = ""
        bestMoveScore = -9000
        
        for move in board.legal_moves:
            board.push_uci(move.uci())
            value = self._minimax(self.depth-1, board, -10000, 10000)
            board.pop()
            if value > bestMoveScore:
                bestMoveScore = value
                bestMove = move
            
        return bestMove.uci()
    
    def play(self, board):
        """play a move."""
        self._findcolor(board)
        bestmove = self._minimaxRoot(board)
        return bestmove

    def quit(self):
        """quit player."""
        return True