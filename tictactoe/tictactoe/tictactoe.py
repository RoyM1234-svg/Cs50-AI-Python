"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0


    if board == initial_state():
        return X
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_x +=1
            elif board[i][j] == O:
                count_o +=1
    if count_x > count_o:
        return O
    else:
        return X

            

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("not valid action")
    b = copy.deepcopy(board)
    if player(b) == X:
        b[action[0]][action[1]] = X
    elif player(b) == O:
        b[action[0]][action[1]] = O
    return b
    
    # raise NotImplementedError

def check_diag(board):
    if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[1][1]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[1][1]
    else:
        return None

def check_horiz(board):
    for i in range(3):
        count_horiz = 0
        temp = board[i][0]
        for j in range(3):
            if board[i][j] == temp:
                count_horiz +=1
            temp = board[i][j]
            if count_horiz == 3:
                return board[i][j]
    return None

def check_vert(board):
    for i in range(3):
        count_vert = 0
        temp = board[0][i]
        for j in range(3):
            if board[j][i] == temp:
                count_vert +=1
            temp = board[j][i]
            if count_vert == 3:
                return board[j][i]
    return None

    
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    if check_diag(board):
        return check_diag(board)
    elif check_horiz(board):
        return check_horiz(board)
    else:
        return check_vert(board)







    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board):
        return True
    for i in range(3):
        if EMPTY in board[i]:
            return False
    return True
        
         # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


    # raise NotImplementedError

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -100
    for action in actions(board):
        v = max(v,min_value(result(board,action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = 100
    for action in actions(board):
        v = min(v,max_value(result(board,action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == O:
        for action in actions(board):
            if max_value(result(board,action)) == min_value(board):
                return action
    else:
        for action in actions(board):
            if min_value(result(board,action)) == max_value(board):
                return action

    


    # raise NotImplementedError
