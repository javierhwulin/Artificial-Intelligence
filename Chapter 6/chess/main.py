import chess
import chess.engine
import math

def evaluate_board(board):
    """A simple evaluation based on material"""
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # King's value is not relevant
    }
    value = 0
    for piece_type in piece_values:
        value += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        value -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return value


def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    """Minimax algorithm with alpha-beta pruning"""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    if is_maximizing:
        best_score = -math.inf
        for move in legal_moves:
            board.push(move)
            best_score = max(best_score, minimax(board, depth - 1, False, alpha, beta))
            board.pop()
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in board.legal_moves:
            board.push(move)
            best_score = min(best_score, minimax(board, depth - 1, True, alpha, beta))
            board.pop()
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def find_best_move(board, depth, player):
    """Find the best move for the current player"""
    best_move = None
    best_score = -math.inf
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, player)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


if __name__ == "__main__":
    board = chess.Board()
    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            move = find_best_move(board, 10, chess.WHITE)
            board.push(move)
        else:
            move = find_best_move(board, 10, chess.BLACK)
            board.push(move)
        input("Press Enter to continue...")
    print(board.result())