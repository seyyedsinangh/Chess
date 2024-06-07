from numpy import flip
import datetime
import chess


def reverseArray(array):
    return flip(array)


pawnEvalWhite = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 6.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]

pawnEvalBlack = reverseArray(pawnEvalWhite);

knightEval = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
    [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
    [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
    [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
    [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

bishopEvalWhite = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
    [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

bishopEvalBlack = reverseArray(bishopEvalWhite)

rookEvalWhite = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
]

rookEvalBlack = reverseArray(rookEvalWhite)

queenEval = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

kingEvalWhite = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
]

kingEvalBlack = reverseArray(kingEvalWhite);


def evaluationBoard(board):
    totalEvaluation = 0
    i = 0
    s = -1
    while i <= 7:
        j = 0
        while j <= 7:
            s += 1
            totalEvaluation += (getPieceValue(str(board.piece_at(s)), i, j))
            j += 1

        i += 1

    return totalEvaluation


def getPieceValue(piece, x, y):
    if piece == None or piece == 'None':
        return 0

    absoluteValue = 0

    if piece == 'P':
        absoluteValue = 10 + pawnEvalWhite[x][y]
        return absoluteValue

    if piece == 'p':
        absoluteValue = 10 + pawnEvalBlack[x][y]
        return absoluteValue * -1

    if piece == 'n':
        absoluteValue = 30 + knightEval[x][y]
        return absoluteValue * -1

    if piece == 'N':
        absoluteValue = 30 + knightEval[x][y]
        return absoluteValue

    if piece == 'b':
        absoluteValue = 30 + bishopEvalBlack[x][y]
        return absoluteValue * -1

    if piece == 'B':
        absoluteValue = 30 + bishopEvalWhite[x][y]
        return absoluteValue

    if piece == 'r':
        absoluteValue = 50 + rookEvalBlack[x][y]
        return absoluteValue * -1

    if piece == 'R':
        absoluteValue = 50 + rookEvalWhite[x][y]
        return absoluteValue

    if piece == 'q':
        absoluteValue = 90 + queenEval[x][y]
        return absoluteValue * -1

    if piece == 'Q':
        absoluteValue = 90 + queenEval[x][y]
        return absoluteValue

    if piece == 'k':
        absoluteValue = 9000 + kingEvalBlack[x][y]
        return absoluteValue * -1

    if piece == 'K':
        absoluteValue = 9000 + kingEvalWhite[x][y]
        return absoluteValue

    print(f'unknow pice: {piece} in the interval: [{x}],[{y}]')
    return absoluteValue


def checkmate_status(board: chess.Board, turn):
    node_evaluation = 0
    is_checkmate = board.is_checkmate()
    # turn = "black" if currently_player == False else "white"

    if turn == "black":
        if is_checkmate:
            node_evaluation += float("inf")
    else:
        if is_checkmate:
            node_evaluation += float("-inf")

    return node_evaluation


def check_status(board: chess.Board, turn):
    black_evaluation = 0
    is_check = board.is_check()
    # turn = "black" if currently_player == False else "white"

    if turn == "black":
        if is_check:
            # print('check status white: True')
            black_evaluation += 10  # * node_evaluation
    else:
        if is_check:
            # print('check status black: True')
            black_evaluation -= 10  # * node_evaluation

    return black_evaluation


def good_square_moves(board: chess.Board, turn):
    node_evaluation = 0
    # turn = "black" if currently_player == False else "white"
    square_values = {"e4": 1, "e5": 1, "d4": 1, "d5": 1, "c6": 0.5, "d6": 0.5, "e6": 0.5, "f6": 0.5,
                     "c3": 0.5, "d3": 0.5, "e3": 0.5, "f3": 0.5, "c4": 0.5, "c5": 0.5, "f4": 0.5, "f5": 0.5}

    possible_moves = board.legal_moves
    for possible_move in possible_moves:
        move = str(possible_move)
        if turn == "black":
            if move[2:4] in square_values:
                node_evaluation += square_values[move[2:4]]
        else:
            if move[2:4] in square_values:
                node_evaluation -= square_values[move[2:4]]

    return node_evaluation
