import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching!

class State:
    """
    This class is used to represent a state.
    board : a list of lists that represents the 8*8 board
    The coord system for the board has the top left corner as (0,0)
    """

    def __init__(self, board, depth):
        """
        Initialize the state.
        :param board: The board of the state.
        :type board: list[list[str]]
        :param depth: The depth of the state.
        :type depth: int

        red_list, black_list : a list containing the coordinates (y, x) of the pieces on the board
                                true if paw, false if king
        """

        self.board = board
        self.width = 8
        self.height = 8
        self.parent = None
        self.depth = depth
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
    
    def  end_state(self):
        """
        Checks if the game has ended
        :return: True if the game has ended, False otherwise
        :rtype: bool
        """
        if self.red_list == [] or self.black_list) == [] or :
            return True
        return False

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

def move_valid(x,y): 
    if x < 0 or x > 8 or y < 0 or y > 8:
        return False
    return True

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

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
    successors_list = []

    player = ['r', 'R']
    # red turn 
    if turn == 'r':
        for i in range(len(state.board)):
            if state.board[i] in player:
                # if normal piece 
                if state.board[i] == 'r':
                    # check if jump would be possible in 2 dir

                        # generate possible jump sequences
                        successors_list.append(gen_helper(state, i, 1, 1, turn))
                        successors_list.append(gen_helper(state, i, -1, 1, turn))

                    # check if move would be valid in 2 dir


                # if king piece
                else:
                    # check if move would be valid in 4 dir 

                    # check if jump would be possible in 4 dir
                    successors_list.append(gen_helper(state, i, 1, 1, turn))
                    successors_list.append(gen_helper(state, i, 1, -1, turn))
                    successors_list.append(gen_helper(state, i, -1, 1, turn))
                    successors_list.append(gen_helper(state, i, -1, -1, turn))
    # black turn
    elif turn == 'b':
        player = get_opp_char(player)

    

    return successors_list

def gen_helper(state, i, x, y, turn):
    """
    Gets the jump sequences for the current state iteratively
    :param state: The current state.

    :return: The successors of the current state for a possible jump.
    :rtype: list[State]
    """
    if state.board[i + x * 8 + y] == '-':
        new_board = copy.deepcopy(state.board)
        new_board[i + x * 8 + y] = new_board[i]
        new_board[i] = '-'
        return State(new_board)
    elif state.board[i + x * 8 + y] in get_opp_char(turn):
        if state.board[i + x * 8 + y * 2] == '-':
            new_board = copy.deepcopy(state.board)
            new_board[i + x * 8 + y * 2] = new_board[i]
            new_board[i + x * 8 + y] = '-'
            new_board[i] = '-'
            return State(new_board)
    else:
        return None

if __name__ == '__main__':
    '''
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
    state = State(initial_board)
    turn = 'r'
    ctr = 0

    sys.stdout = open(args.outputfile, 'w')

    sys.stdout = sys.__stdout__
    '''
    initial_board = read_from_file("test1.txt")
    state = State(board = initial_board, depth = 0)
    turn = 'r'
    ctr = 0

    state.display()
    # print(len(state.board))
    # char = ['r', 'R']
    # print(get_opp_char(char))
