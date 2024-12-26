import const

class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

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

        for i in range(const.HEIGHT):
            line = []
            for j in range(const.WIDTH):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = const.CHAR_GOAL
                self.grid[piece.coord_y][piece.coord_x + 1] = const.CHAR_GOAL
                self.grid[piece.coord_y + 1][piece.coord_x] = const.CHAR_GOAL
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = const.CHAR_GOAL
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = const.CHAR_SINGLE
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = const.CHAR_HOR_LEFT
                    self.grid[piece.coord_y][piece.coord_x + 1] = const.CHAR_HOR_RIGHT
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = const.CHAR_VER_UP
                    self.grid[piece.coord_y + 1][piece.coord_x] = const.CHAR_VER_DOWN

    def construct_hash(self) -> str:
        """
        Construct a unique value to hash for a state.
        This value is made from the current board characters. 
        """
        hash = ''
        for i, line in enumerate(self.grid):
            for ch in line:
                hash += ch
        return hash

    def display(self):
        """
        Print out the current board.
        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()
    
    def display_file(self, file):
        """
        Print out the current board to output file.
        This is the same as the display function, but it outputs the board to a file instead. 
        """
        for i, line in enumerate(self.grid):
            for ch in line:
                file.write(ch)
            file.write('\n')

