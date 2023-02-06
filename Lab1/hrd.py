import copy
from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys


#====================================================================================

char_goal = '1'
char_single = '2'

class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)

    def move_valid(self, x_coord, y_coord): 
        """
        Check if the given coordinate is valid.
        """
        if(self.is_single):
            if (x_coord < 0 or x_coord > 3 or y_coord < 0 or y_coord > 4):
                return False
        if (self.is_goal):
            if (x_coord < 0 or x_coord > 2 or y_coord < 0 or y_coord > 3):
                return False
        if (self.orientation == 'h'):
            if (x_coord < 0 or x_coord > 2 or y_coord < 0 or y_coord > 4):
                return False
        if (self.orientation == 'v'): 
            if (x_coord < 0 or x_coord > 3 or y_coord < 0 or y_coord > 3):
                return False
        return True


class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()


    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def construct_hash(self):
        hash = ''
        for i, line in enumerate(self.grid):
            for ch in line:
                hash += ch
        #db
        #print (hash)
        return hash

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                
                print(ch, end='')
            print()
        

class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, f, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.f = f
        self.depth = depth
        self.parent = parent
        self.id = self.board.construct_hash()
        # self.id = hash(board)  # The id for breaking ties.

    def test_goal(self):
        """
        Test if the current state is the goal state.

        :return: True if the current state is the goal state and False otherwise.
        :rtype: bool
        """

        for piece in self.board.pieces:
            if piece.is_goal:
                if (self.board.grid[3][1] == char_goal 
                    and self.board.grid[3][2] == char_goal
                    and self.board.grid[4][1] == char_goal 
                    and self.board.grid[4][2] == char_goal):
                    return True
        return False

def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):

            if ch == '^': # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == '<': # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == char_single:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == char_goal:
                if g_found == False:
                    pieces.append(Piece(True, False, x, line_index, None))
                    g_found = True
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)
    
    return board

def man_dist(state): 
    """
    Calculate the Manhattan distance of the current state.

    :param state: The current state.
    :type state: State
    :return: The manhattan distance of the current state.
    :rtype: int
    """

    distance = 1
    for piece in state.board.pieces:
        if piece.is_goal:
            distance = abs(3 - piece.coord_y) + abs(1 - piece.coord_x)

    return distance

def add_succesor(state, successors, i, x_coord, y_coord):
    """
    Add a new successor to the successor list.
    """
    new_pieces = copy.deepcopy(state.board.pieces)
    is_goal = state.board.pieces[i].is_goal
    is_single = state.board.pieces[i].is_single
    orientation = state.board.pieces[i].orientation
    new_pieces.pop(i)
    new_pieces.append(Piece(is_goal, is_single, x_coord, y_coord, orientation))
    new_board = Board(new_pieces)
    new_state = State(new_board, 0, state.depth + 1, state)
    successors.append(new_state)
    #db
    # print('BOARD check\n')
    # state.board.display()
    # print('successors after 1 board added\n')
    # for new_states in successors:
    #     new_states.board.display()



def gen_successors(state): 
    """
    Generate the successors of the current state.

    :param state: The current state.
    :type state: State
    :return: The successors of the current state.
    :rtype: list[State]
    """

    successors = []
    i = 0
    for piece in state.board.pieces:

        # single piece
        if piece.is_single:
            # space above
            if piece.move_valid(piece.coord_x, piece.coord_y - 1):
                if state.board.grid[piece.coord_y - 1][piece.coord_x] == '.':
                    add_succesor(state, successors, i, piece.coord_x, piece.coord_y - 1)

            # space below    
            if piece.move_valid(piece.coord_x, piece.coord_y + 1):
                if state.board.grid[piece.coord_y + 1][piece.coord_x] == '.': 
                    add_succesor(state, successors, i, piece.coord_x, piece.coord_y + 1)
                    
            # space left    
            if piece.move_valid(piece.coord_x - 1, piece.coord_y):
                if state.board.grid[piece.coord_y][piece.coord_x - 1] == '.': 
                    add_succesor(state, successors, i, piece.coord_x - 1, piece.coord_y)
                    
            # space right
            if piece.move_valid(piece.coord_x + 1, piece.coord_y):
                if state.board.grid[piece.coord_y][piece.coord_x + 1] == '.':
                    add_succesor(state, successors, i, piece.coord_x + 1, piece.coord_y)
                    
        
        # vertical piece
        if piece.orientation == 'v': 
            # space above
            if piece.move_valid(piece.coord_x, piece.coord_y - 1):
                if state.board.grid[piece.coord_y - 1][piece.coord_x] == '.':
                    add_succesor(state, successors, i, piece.coord_x, piece.coord_y - 1)

            # space below    
            if piece.move_valid(piece.coord_x, piece.coord_y + 1):
                if state.board.grid[piece.coord_y + 2][piece.coord_x] == '.': 
                    add_succesor(state, successors, i, piece.coord_x, piece.coord_y + 1)
                    
            # space left    
            if piece.move_valid(piece.coord_x - 1, piece.coord_y):
                if (state.board.grid[piece.coord_y][piece.coord_x - 1] == '.'
                and state.board.grid[piece.coord_y + 1][piece.coord_x - 1] == '.'): 
                    add_succesor(state, successors, i, piece.coord_x - 1, piece.coord_y)
                    
            # space right
            if piece.move_valid(piece.coord_x + 1, piece.coord_y):
                if (state.board.grid[piece.coord_y][piece.coord_x + 1] == '.'
                and state.board.grid[piece.coord_y + 1][piece.coord_x + 1] == '.'):
                    add_succesor(state, successors, i, piece.coord_x + 1, piece.coord_y)

        # horizontal piece
        if piece.orientation == 'h':
            # space above
            if piece.move_valid(piece.coord_x, piece.coord_y - 1):
                if (state.board.grid[piece.coord_y - 1][piece.coord_x] == '.'
                and state.board.grid[piece.coord_y - 1][piece.coord_x + 1] == '.'):
                    add_succesor(state, successors, i, piece.coord_x, piece.coord_y - 1)

            # space below    
            if piece.move_valid(piece.coord_x, piece.coord_y + 1):
                if (state.board.grid[piece.coord_y + 1][piece.coord_x] == '.'
                and state.board.grid[piece.coord_y + 1][piece.coord_x + 1] == '.'):
                    add_succesor(state, successors, i, piece.coord_x, piece.coord_y + 1)
                    
            # space left 
            if piece.move_valid(piece.coord_x - 1, piece.coord_y):
                if state.board.grid[piece.coord_y][piece.coord_x - 1] == '.': 
                    add_succesor(state, successors, i, piece.coord_x - 1, piece.coord_y)
                    
            # space right
            if piece.move_valid(piece.coord_x + 1, piece.coord_y):
                if state.board.grid[piece.coord_y][piece.coord_x + 2] == '.':
                    add_succesor(state, successors, i, piece.coord_x + 1, piece.coord_y)
        
        # goal piece 
        if piece.is_goal: 
            # space above
            if piece.move_valid(piece.coord_x, piece.coord_y - 1):
                if (state.board.grid[piece.coord_y - 1][piece.coord_x] == '.'
                and state.board.grid[piece.coord_y - 1][piece.coord_x + 1] == '.'):
                    add_succesor(state, successors, i, piece.coord_x, piece.coord_y - 1)

            # space below    
            if piece.move_valid(piece.coord_x, piece.coord_y + 1):
                if (state.board.grid[piece.coord_y + 2][piece.coord_x] == '.'
                and state.board.grid[piece.coord_y + 2][piece.coord_x + 1] == '.'): 
                    add_succesor(state, successors, i, piece.coord_x, piece.coord_y + 1)
                    
            # space left    
            if piece.move_valid(piece.coord_x - 1, piece.coord_y):
                if (state.board.grid[piece.coord_y][piece.coord_x - 1] == '.'
                and state.board.grid[piece.coord_y + 1][piece.coord_x - 1] == '.'): 
                    add_succesor(state, successors, i, piece.coord_x - 1, piece.coord_y)
                    
            # space right
            if piece.move_valid(piece.coord_x + 1, piece.coord_y):
                if (state.board.grid[piece.coord_y][piece.coord_x + 2] == '.'
                and state.board.grid[piece.coord_y + 1][piece.coord_x + 2] == '.'):
                    add_succesor(state, successors, i, piece.coord_x + 1, piece.coord_y)

        i += 1
    
    # for new_states in successors:
    #      print(new_states.id)
    #      print(" ")
    #      new_states.board.display()
    return successors

def get_solution(state):
    """
    Returns a list of states that lead to a solution
    """
    solution = []
    while state.parent:
        solution.append(state)
        state = state.parent
    solution.append(state)
    return solution[::-1]

def dfs(state):
    """
    Depth-first search algorithm 
    
    rq: implement pruning later
    """
    frontier = [state] # keep this a list
    explored = [] # make this a set
    while frontier:
        state = frontier.pop()
        explored.append(state)
        if state.test_goal():
            return state
        successors = gen_successors(state)

        for successor in successors:
            unique = True
            for explored_state in explored:
                # print(successor.id)
                # print(explored_state.id)
                # print('')
                if successor.id == explored_state.id:
                    unique = False
            if unique:
                frontier.append(successor)
    return None


if __name__ == "__main__":
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()


    # read the board from the file
    board = read_from_file(args.inputfile)
    '''
    board = read_from_file('test1.txt')
    state = State(board, 0, 0)
    #db
    # for piece in board.pieces:
    #      print(piece)
    
    fin_state = dfs(state)
    solution = get_solution(fin_state)
    i = 0
    for state in solution:
        print(i)
        state.board.display()
        print(' ')
        i += 1
    #board.construct_hash()
    #print(state.id)
    # str = str(board.display())
    # print(str)
    #gen_successors(state)

    #print(state.test_goal())
    #print(man_dist(state))



