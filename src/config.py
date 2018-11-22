# Author: Anjie Wang
# File: config.py
# Description: 

# "lower" player: begPos-endPos, "UPPER" plaer: endPos-begPos
MoveRules={}
MoveRules['k']=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
MoveRules['g']=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,0]]
MoveRules['s']=[[-1,-1],[-1,0],[-1,1],[1,-1],[1,1]]
MoveRules['p']=[[-1,0]]
MoveRules['r']=[[-1,0],[-2,0],[-3,0],[-4,0],[1,0],[2,0],[3,0],[4,0],[0,-1],[0,-2],[0,-3],[0,-4],[0,1],[0,2],[0,3],[0,4]]
MoveRules['b']=[[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-1,1],[-2,2],[-3,3],[-4,4],[1,-1],[2,-2],[3,-3],[4,-4],[1,1],[2,2],[3,3],[4,4]]
MoveRules['+s']=MoveRules['g']
MoveRules['+b']=MoveRules['b']+[[-1,0],[1,0],[0,-1],[0,1]]
MoveRules['+r']=MoveRules['r']+[[-1,-1],[-1,1],[1,-1],[1,1]]
MoveRules['+p']=MoveRules['g']

# move limit
MOVE_LIMIT=400

# msg
TIE_MSG='Tie game.  Too many moves.'
ILLEGAL_MSG='Illegal move.'
CHECK_MSG='Checkmate.'

DEFAULT_STATE_FILEPATH='defaultState.in'

PIECE_TYPE=['p','g','k','s','b','r']
LOWER_PLAYER='lower'
UPPER_PLAYER='UPPER'
