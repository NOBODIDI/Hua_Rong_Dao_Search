import const

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
        self.id = hash(self.board.construct_hash())
        # self.id = hash(board)  # The id for breaking ties.

    def test_goal(self):
        """
        Test if the current state is the goal state.
        :return: True if the current state is the goal state and False otherwise.
        :rtype: bool
        """

        for piece in self.board.pieces:
            if piece.is_goal:
                if (self.board.grid[3][1] == const.CHAR_GOAL 
                    and self.board.grid[3][2] == const.CHAR_GOAL
                    and self.board.grid[4][1] == const.CHAR_GOAL 
                    and self.board.grid[4][2] == const.CHAR_GOAL):
                    return True
        return False