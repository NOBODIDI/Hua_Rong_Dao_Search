class Piece: 
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal: bool, is_single: bool, coord_x: int, coord_y: int, orientation: str):
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

    def __repr__(self) -> str:
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)

    def move_valid(self, x_coord: int, y_coord: int) -> bool:
        """
        Check if the given coordinate is valid based on the piece type and orientation.

        :param x_coord: The x coordinate to check.
        :type x_coord: int
        :param y_coord: The y coordinate to check.
        :type y_coord: int
        :return: True if the move is valid, False otherwise.
        :rtype: bool
        """
        if self.is_single:
            return 0 <= x_coord <= 3 and 0 <= y_coord <= 4
        if self.is_goal:
            return 0 <= x_coord <= 2 and 0 <= y_coord <= 3
        if self.orientation == 'h':
            return 0 <= x_coord <= 2 and 0 <= y_coord <= 4
        if self.orientation == 'v':
            return 0 <= x_coord <= 3 and 0 <= y_coord <= 3
        return False