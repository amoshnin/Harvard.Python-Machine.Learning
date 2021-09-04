"""
Tic Tac Toe Player
"""
import math
from copy import deepcopy

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
    return X if non_free_cells(board) % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range((len(board[0]))):
            if (board[i][j] is EMPTY):
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if (board[i][j] is not EMPTY):
        raise ValueError

    new_board = deepcopy(board)
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one, or None.
    """
    win_ways = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],

        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],

        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    
    for a, b, c in win_ways:
        player = board[a[0]][a[1]]

        if (player is not EMPTY and player == board[b[0]][b[1]] and player == board[c[0]][c[1]]):
            return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) is not None):
        return True

    return non_free_cells(board) == 9


def utility(board):
    """
    Given a terminal board, returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (not terminal(board)):
        raise ValueError
    
    winner_player = winner(board)
    if (winner_player == X): return 1
    if (winner_player == O): return -1
    if (winner_player == None): return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if (terminal(board)):
        return None

    curr_player = player(board)
    best_value = -math.inf if curr_player == X else math.inf
    best_action = ()

    for action in actions(board):
        # The X player want maximize it.
        if curr_player == X:
            value = min_value(result(board, action))
            if (value > best_value):
                best_value = value
                best_action = action
        # The O player want minimize it.
        else:
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
            
    return best_action


min_value_memo = {}
def min_value(board):
    """
    Current player: O.
    """
    if terminal(board):
        return utility(board)

    memo_key = repr(board)
    if memo_key in min_value_memo:
        return min_value_memo[memo_key]
    
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    min_value_memo[memo_key] = v
    return v


max_value_memo = {}
def max_value(board):
    """
    Current player: X.
    """
    if terminal(board):
        return utility(board)
    
    memo_key = repr(board)
    if memo_key in max_value_memo:
        return max_value_memo[memo_key]

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    
    max_value_memo[memo_key] = v
    return v


def non_free_cells(board):
    """
    Returns the quantity of non empty cells on board.
    """
    count = 0
    
    for i in range(len(board)):
        for j in range((len(board[0]))):
            if board[i][j] is not EMPTY:
                count += 1

    return count