# Project Overview
This project implements a MiniShogi game with two modes: file mode ('-f') and interactive mode ('-i'). Details about Minishogi game and the two modes can be found in `MiniShogi Specification.md`.

# Architecture
This project is implemented using Python. All scripts are stored in `/src` directory:
- `board.py` implements a MiniShogi game board, which stores the state of each square.
- `captures.py` implements "lower" and "UPPER" players' capture lists and related methods.
- `verification.py` implements verification methods for the input game moves.
- `checkmateHandler.py` implements methods related to checkmate condition (detecting and solving).
- `minishogi.py` implements a MiniShogi game.
- `minishogi_driver.py` is the driver that processes command line arguments and launches the Minishogi game based on the arguments.
- `config.py` stores general configurations for the game.
- `utils.py` implements methods that handle input and output.
- `defaultState.in` stores the default beginning game state in interactive mode.

# Run the project
- Change directory to `/src`
- To run in interactive mode: `python minishogi_driver.py -i`
- To run in file mode: `python minishogi_driver.py -f <input file path>`

# Testing
- Change directory to `/test`
- The `.command` file is already set. Simply run the test program corresponding to your system. (e.g. `./test-runner-mac`)
- Details about customizing the testing program can be found in `Minishogi Specification.md`.
