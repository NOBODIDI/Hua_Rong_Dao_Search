import copy
from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys

import const
from board import Board
from piece import Piece
from state import State

#====================================================================================

start = time.time() 


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

            if ch == const.CHAR_VER_UP: # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == const.CHAR_HOR_LEFT: # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == const.CHAR_SINGLE:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == const.CHAR_GOAL:
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
    Man distance is the distance of the 2*2 piece to the exit
    :param state: The current state.
    :type state: State
    :return: The Manhattan distance of the current state.
    :rtype: int
    """

    dist = 1
    for piece in state.board.pieces:
        if piece.is_goal:
            distance = abs(3 - piece.coord_y) + abs(1 - piece.coord_x)
    return dist

def add_succesor(state, successors, i, x_coord, y_coord):
    """
    Add a new successor to the successor list.
    """
    # creating a deep copy of the board pieces
    new_pieces = copy.deepcopy(state.board.pieces)
    # copying attributes of the piece to be moved
    is_goal = state.board.pieces[i].is_goal
    is_single = state.board.pieces[i].is_single
    orientation = state.board.pieces[i].orientation
    # pop the old piece
    new_pieces.pop(i)
    # add the new piece
    new_pieces.append(Piece(is_goal, is_single, x_coord, y_coord, orientation))
    # create a new board
    new_board = Board(new_pieces)
    new_state = State(new_board, 0, state.depth + 1, state)
    # calculate the f value if astar
    if args.algo == 'astar':
        new_state.f = man_dist(new_state) + new_state.depth
    successors.append(new_state)


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
    """
    frontier = [state] # keep this a list
    explored = set() # make this a set
    # is frontier empty? 
    while frontier:
        # select and remove state Curr from frontier
        state = frontier.pop()
        # is Curr in explored? 
        if (state.id not in explored):
            # add Curr to explored
            explored.add(state.id)
            # is Curr a goal state? 
            if state.test_goal():
                # return Curr
                return state
            # add Curr's successors to frontier
            successors = gen_successors(state)
            for successor in successors:
                frontier.append(successor)
    return None

def astar(state):
    """
    A* search algorithm
    """
    frontier = [state] # keep this a list
    explored = set() # make this a set
    # is frontier empty? 
    while frontier:
        # select and remove state Curr from frontier
        state = frontier.pop(0)
        # is Curr in explored? 
        if (state.id not in explored):
            # add Curr to explored
            explored.add(state.id)
            # is Curr a goal state? 
            if state.test_goal():
                # return Curr
                return state
            # add Curr's successors to frontier
            successors = gen_successors(state)
            for successor in successors:
                frontier.append(successor)
            # sort frontier by function value 
            frontier.sort(key=lambda x: x.f)
    return None

if __name__ == "__main__":

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

    if args.algo == 'dfs':
        state = State(board, 0, 0)
        fin_state = dfs(state)
    elif args.algo == 'astar':
        state = State(board, 0, 0)
        # do we need to give a f value to the initial state?
        state.f = man_dist(state)
        fin_state = astar(state)

    # get the solution
    solution = get_solution(fin_state)

    # output solution to file
    output_file = open(args.outputfile, "w")
    #db 
    # i = 0
    for state in solution:
        # output_file.write(str(i) + '\n')
        state.board.display_file(output_file)
        output_file.write('\n')
        # i += 1
    output_file.close()

    end = time.time()
    total_time = round(end - start, 4)
    print("Found solution to " + args.inputfile + " using " + args.algo + " in " + str(total_time) + " seconds.")



