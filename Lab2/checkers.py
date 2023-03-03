import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching!

class State:
    """
    Represents a state of the game
    board : a list of lists that represents the 8*8 board
    The coord system for the board has the top left corner as (0,0)
    """

    def __init__(self, board):
        """
        Initialize the state
        :param board: The board of the state
        :type board: list[list[str]]

        note: 
        - red_list, black_list : a list containing the coordinates (y, x) of the pieces on the board
            has boolean true if pawn, false if king
        """

        self.board = board
        self.width = 8
        self.height = 8
        self.parent = None
        # initialize the red and black lists containing the pieces on the board
        self.red_list = []
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 'r':
                    self.red_list.append(((i,j), True))
                if self.board[i][j] == 'R':
                    self.red_list.append(((i,j), False))
        self.black_list = []
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 'b':
                    self.black_list.append(((i,j), True))
                if self.board[i][j] == 'B':
                    self.black_list.append(((i,j), False))
        # db
        # print("Red list is: ", self.red_list)
        # print("Black list is: ", self.black_list)

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")
    
    def display_file(self, file):
        """
        Print out the current board to output file.
        This is the same as the display function, but it outputs the board to a file instead. 
        """
        for i in self.board:
            for j in i:
                file.write(j)
            file.write('\n')
        file.write('\n')

    def end_state_successors(self, turn):
        """
        Checks if the game has ended
        :param turn: The current turn
        :type turn: str
        :param ret_states: If True, return the successors
        :type ret_states: bool
        :return: True if the game has ended
        :rtype: bool
        """
        # if there are no more black or red pieces on the board, end of the game
        if self.red_list == [] or self.black_list == []:
                return True, []
            
        # if there are no more possible moves for the current player, end of the game
        next_moves = gen_successors(self, turn)
        if next_moves == []:
            return True, next_moves
        return False, next_moves
        
    
    def end_state(self, turn):
        """
        Checks if the game has ended
        """
        # db
        # print(self.end_state_successors(turn)[0])
        successors = gen_successors(self, turn)
        if self.red_list == [] or self.black_list == [] or not successors:
            return True
        return False
        
    def pawn2king(self, turn):
        """
        Checks if pawn should be promoted to a king
        :param turn: The current turn
        :type turn: str
        """

        for piece in self.red_list:
            (y,x), is_pawn = piece
            if is_pawn:
                if (turn == 'r' and y == 0) or (turn == 'b' and y == self.height - 1):
                    self.board[y][x] = turn.upper()
                    self.red_list.remove(piece)
                    piece = ((y,x), False)
                    self.red_list.append(piece)
        # db
        # print("Red list is: ", self.red_list)
        # print("Black list is: ", self.black_list)

def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def move_valid(y,x): 
    if x < 0 or x >= 8 or y < 0 or y >= 8:
        return False
    return True

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

def move(state, piece, turn): 
    """
    Generate the successor moves of the current state
    """
    # a list of list of successors
    successors = []
    (y,x), is_pawn = piece
    if is_pawn: 
        if turn == 'r': 
            pot_moves = [(y - 1, x - 1), (y - 1, x + 1)]
        elif turn == 'b': 
            pot_moves = [(y + 1, x - 1), (y + 1, x + 1)]
    else:
        pot_moves = [(y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)]

    for move in pot_moves:
        # print(move[0])
        # print(move[1])
        if move_valid(move[0], move[1]):
            # db
            # print (state.board[move[0]][move[1]])
            # state.display()
            if state.board[move[0]][move[1]] == '.':
                new_board = copy.deepcopy(state.board)
                # db 
                # will there be a problem because y and x are in a tuple? 
                new_board[y][x] = '.'
                # db
                # print(turn)
                if is_pawn:
                    new_board[move[0]][move[1]] = turn
                else:
                    new_board[move[0]][move[1]] = turn.upper()
                new_state = State(new_board)
                new_state.pawn2king(turn)
                successors.append(new_state)
    return successors
    
def jump(state, origin, piece, turn, successors):
    """
    Generate the successor jumps of the current state.
    """
    # True if a jump happens
    hop = False
    # a list of list of successors
    successors = pot_moves = []
    (y,x), is_pawn = piece

    if is_pawn: 
        if turn == 'r': 
            pot_moves = [(y - 1, x - 1, y - 2, x - 2), (y - 1, x + 1, y - 2, x + 2)]
        elif turn == 'b': 
            pot_moves = [(y + 1, x - 1, y + 2, x - 2), (y + 1, x + 1, y + 2, x + 2)]
    else:
        pot_moves = [(y - 1, x - 1, y - 2, x - 2), (y - 1, x + 1, y - 2, x + 2), (y + 1, x - 1, y + 2, x - 2), (y + 1, x + 1, y + 2, x + 2)]

    for move in pot_moves:
        if move_valid(move[0], move[1]) and move_valid(move[2], move[3]):
            if state.board[move[0]][move[1]] in get_opp_char(turn):
                if state.board[move[2]][move[3]] == '.':
                    hop = True
                    new_board = copy.deepcopy(state.board)
                    new_board[move[0]][move[1]] = '.'
                    new_board[y][x] = '.'
                    if is_pawn:
                        new_board[move[2]][move[3]] = turn
                    else:
                        new_board[move[2]][move[3]] = turn.upper()
                    new_state = State(new_board)
                    # recursive call to jump
                    successors += jump(new_state, origin, ((move[2], move[3]), is_pawn), turn, successors)
                    
                    new_state.pawn2king(turn)
                    successors.append(new_state)
        if state != origin:
            if not hop:    
                state.pawn2king(turn)
                return[state]
            else: 
                return []
    return successors


def gen_successors(state, turn): 
    """
    Generate the successors of the current state.
    :param state: The current state.
    :param turn: The current turn.
    :type state: State
    :return: The successors of the current state.
    :rtype: list[list[State]]
    """
    # a list of list of successors
    successors = []

    # if turn is red, generate successors for red
    if turn == 'r':
        pieces = state.red_list
    else:
        pieces = state.black_list
    
    for piece in pieces:
        successors += jump(state, state, piece, turn, [])
    
    # there are no jumps available
    if successors == []: 
        successors += move(state, piece, turn)

    # for s in successors:
    #     print ("st")
    #     s.display()
    return successors

def get_utility(state, turn, player, depth):
    """
    Get the utility of the current state
    """
    # calculating the performance of each player
    red_score = len(state.red_list)
    black_score = len(state.black_list)
    value = float('inf')

    if red_score == 0:
        if player == 'r':
            return - value
        else: 
            return value
    if black_score == 0:
        if player == 'b':
            return - value
        else: 
            return value
    if turn == player:
        return - value
    if turn != player:
        return value

def get_pieces_h(state, player, depth):
    """
    Get pieces heuristic value
    """
    red_score =  black_score = 0
    value = float('inf')

    # score calculation
    for piece in state.red_list:
        (y,x), is_pawn = piece
        if is_pawn:
            red_score += 1
        else:
            red_score += 2
    for piece in state.black_list:
        (y,x), is_pawn = piece
        if is_pawn:
            black_score += 1
        else:
            black_score += 2

    # end state situations
    if red_score == 0:
        if player == 'r':
            return - value
        else: 
            return value
    if black_score == 0:
        if player == 'b':
            return - value
        else: 
            return value

    # return the score difference    
    if player == 'r':
        return red_score - black_score
    elif player == 'b':
        return black_score - red_score


def heuristic(state, player, depth):
    """
    Get the heuristic value of the current state
    :param state: The current state.
    :type state: State
    :param player: The player of the game
    :type player: str
    """
    return get_pieces_h(state, player, depth)

def get_max(state, depth, turn, player, cache, alpha, beta):
    """
    Get the max value of the current state
    """
    
    if state in cache.keys():
        is_end, successors = cache[state]
    else:
        is_end, successors  = state.end_state_successors(turn)
        cache[state] = (is_end, successors)

    if is_end:
        return get_utility(state, turn, player, depth), state
    if depth == 0:
        return heuristic(state, player, depth), state
    v = (-float('inf'), None)
    successors = sorted(successors, key=lambda x: heuristic(x, player, depth), reverse=True)
    for successor in successors:
        successor.parent = state
        min_val = get_min(successor, depth - 1, get_next_turn(turn), player, cache, alpha, beta)
        if min_val[0] > v[0]:
            v = min_val
        if v[0] >= beta:
            return v
        alpha = max(alpha, v[0])
    return v

def get_min(state, depth, turn, player, cache, alpha, beta):
    """
    Get the min value of the current state
    """
    if state in cache.keys():
        is_end, successors = cache[state]
    else:
        is_end, successors  = state.end_state_successors(turn)
        cache[state] = (is_end, successors)

    if is_end:
        return get_utility(state, turn, player, depth), state
    if depth == 0:
        return heuristic(state, player, depth), state
    v = (float('inf'), None)
    successors = sorted(successors, key=lambda x: heuristic(x, player, depth))
    for successor in successors:
        successor.parent = state
        max_val = get_max(successor, depth - 1, get_next_turn(turn), player, cache, alpha, beta)
        if max_val[0] < v[0]:
            v = max_val
        if v[0] <= alpha:
            return v
        beta = min(beta, v[0])
    return v


def minimax(state, depth, turn, player, is_iter = False, cache = {}): 
    """
    Minimax algorithm
    :param state: The current state
    :type state: State
    :param depth: The depth of the search tree
    :type depth: int
    :param turn: The current turn
    :type turn: str
    :param player: The player of the game
    :type player: str
    :param is_iter: Whether the function is called by iterative deepening
    :type is_iter: bool
    """
    v = get_max(state, depth, turn, player, cache, -float('inf'), float('inf'))
    final_state = v[1]
    while final_state.parent != state and final_state != state:
        final_state = final_state.parent
    return final_state
    # print(final_state)
    # try:
    #     while final_state.parent != state and final_state != state:
    #         final_state = final_state.parent
    #     return final_state
    # except:
    #     print(v)
    #     print(state)
    #     exit()
    
def do_game(state, player, depth): 
    """
    Play the game
    """
    solution = [state]
    turn = player
    # db
    # print (flag)

    while state.end_state(turn) != True:
        state = minimax(state, depth, turn, player)
        solution.append(state)
        player = get_next_turn(player)
        turn = player
        # state.display()
    return solution[ : : -1]


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(board = initial_board)
    turn =  player = 'r'
    ctr = 0

    solution = do_game(state, player, 2)

    output_file = open(args.outputfile, "w")

    # state.display_file(output_file)
    for s in solution: 
        s.display_file(output_file)
        output_file.write('\n')
    output_file.close()
