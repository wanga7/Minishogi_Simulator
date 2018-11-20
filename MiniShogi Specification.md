
# MiniShogi Specification

## Game Rules

### Overview

[MiniShogi](https://en.wikipedia.org/wiki/Minishogi) is a variant of Japanese chess played on a 5x5 board between two players. Over the next two weeks, you will be building a simplified version of this game.

### Objective

The game has two players, **lower** and **UPPER**. Each player aims to capture their opponent's king.

### The Players

The  **lower** player starts on the bottom side of the board, and their pieces are represented by lower-case characters.

The **UPPER** player starts on the top side of the board, and their
pieces are represented by upper-case characters.

The  **lower** player always moves first.

### The Pieces

Each player starts with six pieces, each with different movement capabilities.

A **king (k/K)** can move one square in any direction:
![king](https://cloud.box.com/shared/static/c4t4jv8rx0rdpghmqh79ll5p73aqp0qh.png)

A **rook (r/R)** can move any number of squares along rows or columns (orthogonal directions):
![rook](https://cloud.box.com/shared/static/0i2nnwxq33de2pilxcccn03uyw0diop4.png)

A **bishop (b/B)** can move any number of squares along diagonal directions:
![bishop](https://cloud.box.com/shared/static/8os7qcj460m7xlemuza79x73qj5kswcp.png)

A **gold general (g/G)** can move one square in any direction except its backward diagonals:
![gold general](https://cloud.box.com/shared/static/hsgw8dzhjoomg02iztkpmiazihh25nzz.png)

A **silver general (s/S)** can move one square in any direction except sideways or directly backward:
![silver general](https://cloud.box.com/shared/static/o3so3mxenqrxfgu10de0548jncah3eei.png)

A **pawn (p/P)** can move one space forward:
![pawn](https://cloud.box.com/shared/static/e5yy8btndh8vu6qm988sra52corqhudi.png)

*Note: a rook or bishop cannot jump over pieces in its path of movement.*

### The Board

The board is a grid of 5 rows by 5 columns. We will call each location on the board a *square*.

This is the starting board state:
```
5 | R| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p|__|__|__|__|
1 | k| g| s| b| r|
    a  b  c  d  e
```

We read the board via a combination of the letters on the x-axis and numbers on the y-axis. For instance, piece *p* is at location *a2* while piece *P* is at location *e4*.

### Capturing

A player can capture an opponent's piece by moving their piece onto the same square as an opponent's piece. The captured piece leaves the board, and can be later dropped onto the board by the player who captured it (more on this under *Drops* below). A player cannot capture their own pieces (this is an illegal move).

### Promotion

A piece may (but does not have to) be **promoted** when it moves into, within, or out of the **promotion zone**.

The promotion zone is the row of the board furthest from each player's starting position:
* For the lower player, the promotion zone is the top row of the board.
* For the UPPER player, the promotion zone is the bottom row of the board.

A piece that has been promoted should gain a plus symbol "+" before its letter showing on the board.

Pieces promote as follows:
* A **king** cannot be promoted.
* A **gold general** cannot be promoted.
* A **promoted silver general** (+s/+S) moves the same way as a **gold general**.
* A **promoted bishop** (+b/+B) can move like a **bishop** or a **king**.
* A **promoted rook** (+r/+R) can move like a **rook** or a **king**.
* A **promoted pawn** (+p/+P) moves like a **gold general**.

*Note: Pawns **must** be promoted once they reach the furthest row (otherwise they would not have any legal moves on the next turn).*

### Drops

Pieces that a player has captured can be dropped back onto the board under the capturing player's control. Dropping a piece takes your entire turn.

You cannot drop a piece onto a square that contains another piece.

All dropped pieces must start unpromoted (even if they were captured as promoted pieces and/or are dropped into the promotion zone).

A pawn may not be dropped into the promotion zone or onto a square that results in an immediate checkmate.
* Note: other pieces *can* be dropped into the promotion zone or onto a square that results in an immediate checkmate.

Two unpromoted pawns may not lie in the same column when they belong to the same player (e.g. If you already have a pawn in the third column, you cannot drop another pawn into that column).

### Game End

#### Move Limit

For simplicity, the game ends in a tie once each player has made 200 moves. When a game ends in a tie, output the message "Tie game.  Too many moves." instead of the move prompt.

#### Checkmate

When a player is in a position where their king could be captured on their opponent's next move, they are in **check**.
That player **must** make a move to get out of check by doing one of the following:
* remove their king from danger
* capture the piece that threatens their king
* put another piece between the king and the piece that threatens it

If a player has no moves that they could make to avoid capture, they are in **checkmate** and lose the game.

When a player wins via checkmate, output the message "<UPPER/lower> player wins.  Checkmate." instead of the move prompt.

#### Illegal Moves

If a player makes a move that is not legal, the game ends immediately and the other player wins. When a player loses via an illegal move, output the message "<UPPER/lower> player wins.  Illegal move." instead of the move prompt.

## Game Interface

Your program should accept command line flags to determine which mode to play in:
```
$ myShogi -i
```
In **interactive mode**, two players enter keyboard commands to play moves against each other.

```
$ myShogi -f <filePath>
```
In **file mode**, the specified file is read to determine the game state and which moves to make.

### Interactive Mode

#### Output

At the beginning of each turn, your program should output the following:
1. The current board state, using the utility function provided to generate the text representation of the board
2. An empty line
3. The space-separated list of pieces captured by **UPPER** (in the order that they were captured)
4. The space-separated list of pieces captured by **lower** (in the order that they were captured)
5. An empty line
6. An input prompt for the next player to enter their move, followed by a space

For example, this is how a game would begin:
```
$ myShogi -i
5 | R| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p|__|__|__|__|
1 | k| g| s| b| r|
    a  b  c  d  e

Captures UPPER: 
Captures lower: 

lower> 
```

**NOTE:** You should use the provided utility function `stringifyBoard()` to get the string representation of the board state.

#### Move Format

The **lower** player would then enter a move using the following formats:

**move <from> <to> [promote]**
To move a piece, enter `move` followed by the location of the piece to be moved, the location to move to, and (optionally) the word `promote` if the piece should be promoted at the end of the turn.
* `move a2 a3` moves the piece at square a2 to square a3.
* `move a4 a5 promote` moves the piece at square a4 to square a5 and promotes it at the end of the turn.

**drop <piece> <to>**
To drop a piece, enter `drop` followed by the lowercase character representing the piece to drop and the location to drop the piece.  Pieces are always lower-case, no matter which player is performing the drop.
* `drop g c3` drops a captured **gold general** at square c3.
* `drop b a1` drops a captured **bishop** at square a1.

Once a player enters their move, your program should display the move made, update the game state, and proceed to the next turn. For example:
```
lower> move b1 b2
lower player action: move b1 b2
5 | R| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p| g|__|__|__|
1 | k|__| s| b| r|
    a  b  c  d  e

Captures UPPER: 
Captures lower: 

UPPER> move a5 a2
UPPER player action: move a5 a2
5 |__| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | R| g|__|__|__|
1 | k|__| s| b| r|
    a  b  c  d  e

Captures UPPER: P
Captures lower: 

lower> 
```

#### Check Detection

Before a player's turn, you should also determine if they are in check. If so, output a line stating that they are in check, and output all available moves for them to get out of check (one move per line):
```
5 |__|__|__| K|__|
4 |__|__|__|__|__|
3 |__|__|__|__|__|
2 |__| G|__|__|__|
1 | k|__|__|__|__|
    a  b  c  d  e

Captures UPPER: R B G S P
Captures lower: b p s r

lower player is in check!
Available moves:
move a1 b2
lower> 
```

If a player is in check and performs an action which is not one of the outputted available moves out of check, we consider it an illegal move. Also, moving oneself into check is considered an illegal move.

*Note: If your moves out of check are a different ordering than the test case output, alphabetizing the moves should result in the same ordering as expected test output.*

#### Game End

When the game ends, output which player won and the reason they won. Examples:
* UPPER player wins.  Checkmate.
* lower player wins.  Illegal move.
* Tie game.  Too many moves.

### File Mode

**File mode** is very similar to **interactive mode**, except the input can be a partial game.

The input file will contain:
* each piece's current position
* an array of pieces captured by UPPER
* an array of pieces captured by lower
* moves to make with one move per line

Your program should output the board state after the list of moves have been made, or immediately if one player wins in the middle of the input.

File mode will be used by a provided test runner to compare your output against the expected output. (See `Testing your program`)

Running the test cases manually is not required, but can be helpful when starting file mode.
If you'd like to run a test case individually outside of the test runner:
1. use the .in files as the inputs to file mode
2. compare the output to the corresponding .out file.  

For example, using the `diff` tool on a Python solution:

```
$ python mini_shogi.py -f ~/tests/initialMove.in | diff -u ~/tests/initialMove.out -
```

For example, this file begins in the middle of a game and does not complete the game:
```
k a1
g b1
s c1
b d1
r e1
p a2
K e5
G d5
S c5
B b5
R a5
P e4

[]
[]

move a2 a3
move e4 e3
```

**NOTE:** You should use the provided utility function `parseTestCase()` to read in the test case.  This function will read in the file for you and produce an object with the relevant information.

The expected output is the same output as **interactive mode** after the last move is made:
```
UPPER player action: move e4 e3
5 | R| B| S| G| K|
4 |__|__|__|__|__|
3 | p|__|__|__| P|
2 |__|__|__|__|__|
1 | k| g| s| b| r|
    a  b  c  d  e

Captures UPPER: 
Captures lower: 

lower> 
```

In the following example, the game ends after the third move and your program does not need to read the last move.

Input:
```
k a1
K e5

[]
[]

move a1 a2
move e5 e4
move a2 e4
move e4 e5
```

Expected output:
```
lower player action: move a2 e4
5 |__|__|__|__|__|
4 |__|__|__|__| K|
3 |__|__|__|__|__|
2 | k|__|__|__|__|
1 |__|__|__|__|__|
    a  b  c  d  e

Captures UPPER: 
Captures lower: 

UPPER player wins.  Illegal move.
```

## Resources

### Utility Functions

We are providing some utility functions in each language (Python, Java, or Javascript). You should use these functions to handle some of the tedious input and output so that you don't need to implement it yourself. The utility functions can be modified to suit your needs. They are also optional; not required to be used.
https://cloud.box.com/v/minishogiutilities 

### Testing your program

We have created a collection of test cases along with a test runner that you can use to determine the correctness of your solution. We will also use the test runner when evaluating your program.

The test runner is provided as a binary, and supports macOS, Windows 10, and Ubuntu Linux. Other flavors of these operating systems may work, but are not tested.

The test runner can be downloaded from this folder: https://cloud.box.com/v/testrunner
The test cases can be found here: https://cloud.box.com/v/minishogitests

#### Setting up the test runner
1. To invoke the test runner, execute the version for your operating system. e.g. `./test-runner-mac`, or on Windows, `cmd /K test-runner-windows.exe`
**Notes:** 
- On windows, pass the `/K` option to keep the runner open after execution
- Make sure the runner is executable via the terminal by running `chmod a+x test-runner-mac` or `chmod a+x test-runner-linux`. On Windows, right click the file and navigate the `properties` menu
2. On first run, the test runner will ask you to enter the command you use to run your program in file mode. **Note:** make sure that you are correctly referencing your program relative to your current directory.
e.g. `python ./src/Minishogi.py -f`
3. This will create a file called `.command`, make sure to commit and submit this file as part of your repo/solution so we can run your tests later!

#### Supported flags
`-r` reset: this resets the `.command` file in case the path/way you run your program in file mode changes
`-v` verbose: this will print out the difference in the expected output and actual output of failed tests, along with an explanation of the differences/errors
`-f` filter: filters test cases based on a string. e.g. `./test-runner-mac -f "bishop"` will run tests that have bishop in their name.
    **Note:** If using windows, make sure to use double quotes "" or no quotes. Single quotes will not work.
`-b` break: stops execution of tests after the first encountered failure

**Note:** You can combine flags, although if you're using the filter flag, the filter string must be right after. For example, both of these would work equivalently:
- `./test-runner-mac -b -f 'bishop'`
- `./test-runner-mac -f 'bishop' -b`

Note: the test cases aren't completely exhaustive — there are too many variations of illegal moves for creating a totally exhaustive set to be feasible — but for the purposes of evaluating your solution, you don't need to consider anything not covered by the provided test cases.

### Reference Reading

* https://en.wikipedia.org/wiki/Minishogi
* https://en.wikipedia.org/wiki/Shogi#Rules