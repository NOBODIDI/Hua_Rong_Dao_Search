## Solving Hua Rong Dao Using Search

This project implements a solution to the [Hua Rong Dao puzzle](https://chinesepuzzles.org/huarong-pass-sliding-block-puzzle/)using search algorithms. The main program, `hrd.py`, reads an initial board configuration from a file, applies either Depth-First Search (DFS) or A\* search algorithm to find a solution, and writes the solution to an output file.

### Example puzzle board

```
^^<>
vv<>
<>22
11.2
11.2
```

![alt text](huaRongDao.png)

### Files

- `hrd.py`: The main program that runs the search algorithms.
- `board.py`: Contains the `Board` class for setting up the playing board.
- `piece.py`: Contains the `Piece` class representing a piece on the board.
- `state.py`: Contains the `State` class wrapping a `Board` with extra state information.
- `const.py`: Contains constants used in the program.

### Usage

To run the program, use the following command:

```sh
python hrd.py --inputfile <inputfile> --outputfile <outputfile> --algo <algorithm>
```

#### Arguments

- `--inputfile`: The input file that contains the initial board configuration.
- `--outputfile`: The output file that will contain the solution.
- `--algo`: The search algorithm to use (`astar` or `dfs`).

#### Example

```sh
python hrd.py --inputfile puzzle.txt --outputfile solution.txt --algo astar
```

This command reads the initial board configuration from `puzzle.txt`, uses the A\* search algorithm to find a solution, and writes the solution to `solution.txt`.

### Input File Format

The input file should contain the initial board configuration, where each character represents a piece on the board:

- `1`: Goal piece (2x2)
- `2`: Single piece (1x1)
- `^`: Vertical piece (top part)
- `v`: Vertical piece (bottom part)
- `<`: Horizontal piece (left part)
- `>`: Horizontal piece (right part)
- `.`: Empty space

### Output File Format

The output file will contain the sequence of board configurations leading to the solution. Each configuration is separated by a blank line.

### Notes

- The program measures the time taken to find the solution and prints it to the console.
- The A\* search algorithm uses the Manhattan distance heuristic to guide the search.
