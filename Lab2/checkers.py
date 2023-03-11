import argparse
import copy
from copy import deepcopy
import sys
import time

class State:
    """
    Represents a state of the game
    board : a list of lists that represents the 8*8 board
    The coord system for the board has the top left corner as (0,0)
    """
    def __init__(self, board=None, red_list=None, black_list=None):
        """
        Initialize the state
        :param board: The board of the state
        :type board: list[list[str]]

        note: 
        - red_list, black_list : a list containing the coordinates (y, x) of the pieces on the board
            has boolean true if pawn, false if is_king
        """
        self.board = None
        self.width = 8
        self.height = 8
        self.parent = None

        if board != None:
            self.board = board
            if red_list != None:
                self.red_list = red_list
            else:
                self.red_list = []
                for i in range(self.height):
                    for j in range(self.width):
                        if self.board[i][j] == 'r':
                            self.red_list.append((False,i, j))
                        if self.board[i][j] == 'R':
                            self.red_list.append((True,i, j))
            if black_list != None:
                self.black_list = black_list
            else:
                self.black_list = []
                for i in range(self.height):
                    for j in range(self.width):
                        if self.board[i][j] == 'b':
                            self.black_list.append((False,i, j))
                        if self.board[i][j] == 'B':
                            self.black_list.append((True,i, j))

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
        # file.write('\n')

    def is_end(self, turn):
        """
        Checks if the game has ended
        :param turn: The current turn
        :type turn: str
        :param ret_states: If True, return the successors
        :type ret_states: bool
        :return: True if the game has ended
        :rtype: bool
        """
        successors = gen_successors(self, turn)
        if self.red_list == [] or self.black_list == [] or successors == []:
            return True, successors
        return False, successors
    
    def is_end_simple(self, turn):
        """
        Checks if the game has ended
        """
        successors = gen_successors(self, turn)
        if self.red_list == [] or self.black_list == [] or successors == []:
            return True
        successors = gen_successors(self, get_next_turn(turn))
        if successors == []:
            return True
        return False

    def pawn2king(self, turn):
        """
        Checks if pawn should be promoted to a king
        :param turn: The current turn
        :type turn: str
        """
        if turn == 'r':
            for piece in self.red_list:
                is_king, y, x = piece
                if not is_king and y == 0:
                    self.board[y][x] = turn.upper()
                    self.red_list.remove(piece)
                    piece = (True,y,x)
                    self.red_list.append(piece)
        elif turn == 'b':
            for piece in self.black_list:
                is_king, y, x = piece
                if not is_king and y == (self.height-1):
                    self.board[y][x] = turn.upper()
                    self.black_list.remove(piece)
                    piece = (True,y,x)
                    self.black_list.append(piece)
        

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def move_valid(x): 
    if x < 0 or x >= 8:
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
    is_king, y, x = piece
    if is_king:
        pot_moves = [(y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)]
    elif turn=='r':
        pot_moves = [( y - 1, x + 1), (y - 1, x - 1)]
    else:
        pot_moves = [(y + 1, x + 1), (y + 1, x - 1)]

    for mo in pot_moves:
        if move_valid(mo[0]) and move_valid(mo[1]):
                if state.board[mo[0]][mo[1]] == '.':
                    new = copy.deepcopy(state.board)
                    new[y][x] = '.'
                    if is_king:
                        new[mo[0]][mo[1]] = turn.upper()
                    else:
                        new[mo[0]][mo[1]] = turn
                    new_state = State(new)
                    new_state.pawn2king(turn)
                    successors.append(new_state)
    return successors


def jump(state, piece, turn, suc, origin):
    """
    Generate the successor jumps of the current state.
    """
    hop = False
    successors = pot_moves = []
    is_king, y, x = piece
    if is_king:
        pot_moves = [(y - 1, x - 1, y - 2, x - 2), (y - 1, x + 1, y - 2, x + 2), (y + 1, x - 1, y + 2, x - 2), (y + 1, x + 1, y + 2, x + 2)]
    elif turn=='r':
        pot_moves = [(y - 1, x - 1, y - 2, x - 2), (y - 1, x + 1, y - 2, x + 2)]
    else:
        pot_moves = [(y + 1, x - 1, y + 2, x - 2), (y + 1, x + 1, y + 2, x + 2)]
    for mo in pot_moves:
        go = False
        for x in mo:
            if not move_valid(x):
                go = True
        if go:
            continue
        if state.board[mo[0]][mo[1]] in get_opp_char(turn):
            if state.board[mo[2]][mo[3]] == '.':
                hop = True
                new = copy.deepcopy(state.board)
                new[mo[0]][mo[1]]='.'
                if is_king:
                    new[mo[2]][mo[3]] = turn.upper()
                else:
                    new[mo[2]][mo[3]] = turn
                new[y][x] = '.'
                new_state = State(new)
                suc+=jump(new_state,(is_king, mo[2], mo[3]), turn, suc, origin)
                
    if state != origin:
        if not hop:
            state.pawn2king(turn)
            return [state]
        else:
            return []
    return suc
    

def gen_successors(state, turn):
    """
    Generate the successors of the current state.
    :param state: The current state.
    :param turn: The current turn.
    :type state: State
    :return: The successors of the current state.
    :rtype: list[list[State]]
    """
    successors = []
    if turn == 'r':
        pieces = state.red_list
    else:
        pieces = state.black_list

    for piece in pieces:
        successors += jump(state, piece, turn, [], state) 
    if successors == []:
        for piece in pieces:
            successors += move(state, piece, turn)
    return successors



def get_utility(state, turn, player, depth):
    """
    Get the utility of the current state
    """
    red_score = len(state.red_list)
    black_score = len(state.black_list)
    value = 100000  * (depth + 1)
    if red_score == 0:
        if player == 'r':
            return -value
        else:
            return value
        
    if black_score == 0:
        if player == 'b':
            return -value
        else:
            return value
        
    if turn == player:
        return -value
    if turn != player:
        return value
    

def get_heuristic(state, player, depth):
    """
    Get the heuristic value of the current state
    :param state: The current state.
    :type state: State
    :param player: The player of the game
    :type player: str
    """
    red_score = black_score = 0
    value = 100000 * (depth+1)

    for piece in state.red_list:
        if piece[0]:
            red_score+=2
        else:
            red_score+=1

    for piece in state.black_list:
        if piece[0]:
            black_score +=2
        else:
            black_score +=1

    if red_score == 0:
        if player == 'r':
            return -value
        else:
            return value
        
    if black_score == 0:
        if player == 'b':
            return -value
        else:
            return value
        
    if player == 'r':
        return red_score - black_score
    elif player == 'b':
        return black_score - red_score
 

def minimax(state, depth, turn, player):
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
    """
    v_val = get_max(state, depth, turn, player, -float('inf'), float('inf'))
    return v_val[1]


def get_max(state, depth, turn, player, alpha, beta):
    """
    Get the max value of the current state
    """ 
    end, next_st = state.is_end(turn)
    if end:
        return get_utility(state, turn, player, depth), state
    if depth == 0:
        return get_heuristic(state,player,depth), state
    v_val = (-float('inf'),None)
    next_st = sorted(next_st, key=lambda x:get_heuristic(x, player, depth), reverse=True)
    for st in next_st:
        st.parent = state
        m_val = get_min(st, depth - 1, get_next_turn(turn), player, alpha, beta)
        if m_val[0] > v_val[0]:
            v_val = m_val
        if v_val[0] >= beta:
            return v_val
        alpha = max(alpha, v_val[0])
    return v_val

def get_min(state, depth, turn, player, alpha, beta):
    """
    Get the min value of the current state
    """
    end, next_st = state.is_end(turn)
    if end:
        return get_utility(state, turn, player,depth), state
    if depth == 0:
        return get_heuristic(state,player,depth),state
    v_val = (float('inf'),None)
    next_st = sorted(next_st, key=lambda x:get_heuristic(x, player, depth), reverse=False)
    for st in next_st:
        st.parent = state
        m_val = get_max(st, depth - 1, get_next_turn(turn), player, alpha, beta)
        if m_val[0] < v_val[0]:
            v_val = m_val
        if v_val[0] <= alpha:
            return v_val
        beta = min(beta, v_val[0])
    return v_val

def play_game(state, player, depth):
    """
    Play the game
    """
    c = depth
    turn = player
    temp_state = state
    while temp_state.is_end_simple(turn) == False:
        temp_state = minimax(state, c, turn, player)
        if c >= 8:
            c += 1
        else:
            c += 3
        
    solution = []
    while temp_state != None:
            solution.append(temp_state)
            temp_state = temp_state.parent  
    return solution[:: -1]

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

    solution = play_game(state, player, 5)

    # db
    # suc = gen_successors(state, 'b')

    output_file = open(args.outputfile, "w")

    # state.display_file(output_file)
    for st in solution: 
        st.display_file(output_file)
        output_file.write('\n')
    output_file.close()