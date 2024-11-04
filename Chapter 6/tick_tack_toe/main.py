def is_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(len(board[0])):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(len(board))):
        return True
    if all(board[i][len(board) - i - 1] == player for i in range(len(board))):
        return True
    return False


def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)


def evaluate(board):
    if is_winner(board, 'X'):
        return 1
    elif is_winner(board, 'O'):
        return -1
    else:
        return 0


def minimax(board, depth, isMaximizing):
    score = evaluate(board)
    if score == 1 or score == -1 or is_draw(board):
        return score
    if isMaximizing:
        bestScore = -float('inf')
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    bestScore = max(
                        bestScore, minimax(board, depth + 1, False)
                    )
                    board[row][col] = ' '
        return bestScore
    else:
        bestScore = float('inf')
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    bestScore = min(bestScore, minimax(board, depth + 1, True))
                    board[i][j] = ' '
        return bestScore


def find_best_move(board):
    bestMove = (-1, -1)
    bestValue = -float('inf')

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                moveValue = minimax(board, 0, False)
                board[i][j] = ' '
                if moveValue > bestValue:
                    bestMove = (i, j)
                    bestValue = moveValue
    return bestMove


def print_board(board):
    for row in board:
        print(row)
    print()


if __name__ == '__main__':
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print_board(board)
    while True:
        row, col = find_best_move(board)
        board[row][col] = 'X'
        print_board(board)
        if is_winner(board, 'X'):
            print('X wins!')
            break
        elif is_draw(board):
            print('Draw!')
            break
        row = int(input('Enter row: '))
        col = int(input('Enter column: '))
        board[row][col] = 'O'
        print_board(board)
        if is_winner(board, 'O'):
            print('O wins!')
            break
        elif is_draw(board):
            print('Draw!')
            break
