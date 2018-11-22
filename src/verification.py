'''
Author: Anjie Wang
File: verification.py
Descrition: implement game move verification methods
'''

from board import Board
from captures import Captures
import checkmateHandler
import config

# check if a move is valid
def validMove(move,player,board,captures):
	# format validation - same for 'move' and 'drop'
	if not moveFormatCheck(move):
		return False
	# type-specific validations
	if move[0]=='move':
		return typeSpecificCheck_move(player,move[1],move[2],len(move)==4,board)
	else:
		return typeSpecificCheck_drop(player,move[1],move[2],board,captures)

# check if the general format of a move is correct
def moveFormatCheck(move):
	if len(move)!=3 and len(move)!=4:
		return False
	if move[0] not in ('move','drop'):
		return False
	if len(move)==4 and move[3]!='promote':
		return False
	if len(move)==4 and move[0]!='move':
		return False
	return True

# check if a 'move'-type move is legal
def typeSpecificCheck_move(player,begPos,endPos,promote,board):
	'''
	1) beg and end position are valid
	2) piece belong to the right player
	3) endPos does not already have another piece of the same player
	'''
	if not board.inRange(begPos) or not board.inRange(endPos):
		return False
	if not ownPiece(player,board.get(begPos)):
		return False
	if board.get(endPos)!='' and ownPiece(player,board.get(endPos)):
		return False
	'''
	Promotion checks
	1) promoted piece cannot be promoted again
	2) promotion must happen when piece moves into/ within/ out of promotion zone
	3) king and gold general cannot be promoted
	'''
	if promote:
		if len(board.get(begPos))>=2:
			return False
		if not board.inPromotionZone(begPos,player) and not board.inPromotionZone(endPos,player):
			return False
		if board.get(begPos).lower() in ('k','g'):
			return False

	# move rules check based on piece type
	if not canMove(begPos,endPos,board):
		return False

	# cannot move into check
	return not checkmateHandler.movingIntoCheck(begPos,endPos,player,board)

# check if a 'drop'-type move is legal
def typeSpecificCheck_drop(player,piece,endPos,board,captures):
	'''
	1) one can only drop a piece in its capture
	2) drop position should be in range
	3) drop position should not have another piece
	'''
	if not captures.inCapture(piece,player):
		return False
	if not board.inRange(endPos):
		return False
	if board.get(endPos)!='':
		return False
	'''
	4) pawn may not be dropped into promotion zone
	5) pawn may not be dropped into a square that results in immediate checkmate
	6) two unpromoted pawns from the same player may not lie in the same colunm
	'''
	if piece=='p':
		if board.inPromotionZone(endPos,player):
			return False
		
		board.set(endPos,piece)
		if len(checkmateHandler.checkmate(opponent(player),board))>0:
			board.set(endPos,'')
			return False
		board.set(endPos,'')

		j=board.getCol(endPos)
		for i in range(0,config.BOARD_SIZE):
			piece=board.get_ij(i,j)
			if piece.lower()=='p' and ownPiece(player,piece):
				return False
	return True

# check if the piece on begPos can be moved to endPos in one step, based on move rules for the piece
def canMove(begPos,endPos,board):
	piece=board.get(begPos)
	piece_type=piece.lower()

	# calculate relative position between endPos and begPos
	diff=[]
	if piece.islower():
		diff=[ord(begPos[1])-ord(endPos[1]),ord(endPos[0])-ord(begPos[0])]
	else:
		diff=[ord(endPos[1])-ord(begPos[1]),ord(endPos[0])-ord(begPos[0])]

	# check move rules based on piece type
	if piece_type=='k':
		return canMove_k(begPos,endPos,diff)
	elif piece_type=='g':
		return canMove_g(begPos,endPos,diff)
	elif piece_type=='s':
		return canMove_s(begPos,endPos,diff)
	elif piece_type=='p':
		return canMove_p(begPos,endPos,diff)
	elif piece_type=='r':
		return canMove_r(begPos,endPos,diff,board)
	elif piece_type=='b':
		return canMove_b(begPos,endPos,diff,board)
	elif piece_type=='+s':
		return canMove_g(begPos,endPos,diff)
	elif piece_type=='+b':
		return canMove_b(begPos,endPos,diff,board) or canMove_k(begPos,endPos,diff)
	elif piece_type=='+r':
		return canMove_r(begPos,endPos,diff,board) or canMove_k(begPos,endPos,diff)
	elif piece_type=='+p':
		return canMove_g(begPos,endPos,diff)

# verify move based on specific type's move rules
def canMove_k(begPos,endPos,diff):
	return diff in config.MoveRules['k']

def canMove_g(begPos,endPos,diff):
	return diff in config.MoveRules['g']

def canMove_s(begPos,endPos,diff):
	return diff in config.MoveRules['s']

def canMove_p(begPos,endPos,diff):
	return diff in config.MoveRules['p']

def canMove_r(begPos,endPos,diff,board):
	if diff[0]!=0 and diff[1]!=0:
		return False;
	return canMove_rb(begPos,endPos,diff,board)

def canMove_b(begPos,endPos,diff,board):
	if abs(diff[0])!=abs(diff[1]):
		return False
	return canMove_rb(begPos,endPos,diff,board)

def canMove_rb(begPos,endPos,diff,board):
	piece=board.get(begPos)
	di=0 if diff[0]==0 else diff[0]/abs(diff[0])
	dj=0 if diff[1]==0 else diff[1]/abs(diff[1])
	di=-di if piece.islower() else di
	
	i=board.getRow(begPos)+di
	j=board.getCol(begPos)+dj
	
	while i!=board.getRow(endPos) or j!=board.getCol(endPos):
		if board.get_ij(i,j)!='':
			return False
		i+=di
		j+=dj
	return True

# get the opponent of the player
def opponent(player):
	return config.LOWER_PLAYER if player==config.UPPER_PLAYER else config.UPPER_PLAYER

# check if the piece is owned by the player
def ownPiece(player,piece):
	return piece.islower()==(player==config.LOWER_PLAYER)