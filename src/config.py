# Anjie Wang
# Config.py
# Description: 

# "lower" player: begPos-endPos, "UPPER" plaer: endPos-begPos
MoveRules={}
MoveRules["k"]=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
MoveRules["g"]=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,0]]
MoveRules["s"]=[[-1,-1],[-1,0],[-1,1],[1,-1],[1,1]]
MoveRules["p"]=[[-1,0]]

# move limit
MOVE_LIMIT=400

# msg
TIE_MSG='Tie game.  Too many moves.'
ILLEGAL_MSG='Illegal move.'
CHECK_MSG='Checkmate.'

