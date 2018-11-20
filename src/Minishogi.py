# Anjie Wang
# Minishogi.py
# Description: 

import utils
import config
import sys
import string

# game state variables
State=dict(Board=[],Cap_U=[],Cap_l=[],Moves=[],Mode="")
DEFAULT_STATE_FILEPATH='defaultState.in'

# verify and process arguments
def processArgv(argv):
	if len(argv)==2 and argv[1]=="-i":
		#interactive mode
		State['Mode']="i"
		initialize(utils.parseTestCase(DEFAULT_STATE_FILEPATH))
		return True
	elif len(argv)==3 and argv[1]=="-f":
		# file mode
		State['Mode']="f"
		initialize(utils.parseTestCase(argv[2]))
		return True
	else:
		# invalid argvs
		return False

# intialize GameState
def initialize(info):
	for i in range(0,5):
		row=[]
		for j in range(0,5):
			row.append("")
		State['Board'].append(row)

	for p in info['initialPieces']:
		set(p['position'],p['piece'])

	State['Cap_U']=info['upperCaptures']
	State['Cap_l']=info['lowerCaptures']
	State['Moves']=info['moves']

# play the game (read in move, verify & update, check result)
def play():
	validGame=True
	player="UPPER"
	move_idx=0
	if State['Mode']=='i':
		display()

	endReason=''
	stepCnt=0
	while validGame:
		# check checkmate situation
		'''
		if checkmate(player):
			print 'checkmate for %s' % player
			# find available moves
		'''

		# switch side
		player='lower' if player=='UPPER' else 'UPPER'

		# read in next move (-i,-f)
		if State['Mode']=="i":
			move=raw_input(player+'> ').split(' ')
			displayAction(player,move)
		else:
			move=State['Moves'][move_idx].split(' ')
			move_idx+=1
			if move_idx>=len(State['Moves']):
				validGame=False

		# verify validity of the move
		if validMove(move,player):
			# execute the move
			executeMove(move,player)
			stepCnt+=1
			if State['Mode']=='i':
				display()
		else:
			# game over
			endReason=config.ILLEGAL_MSG
			validGame=False

		# check move limit
		if (validGame or endReason=='') and stepCnt==config.MOVE_LIMIT:
			endReason=config.TIE_MSG
			validGame=False
			
	
	if State['Mode']=='f':
		displayAction(player,move)
		display()
		if endReason==config.TIE_MSG:
			print endReason
		elif endReason!='':
			print '%s player wins.  %s' % (opponent(player),endReason)
		else:
			print '%s> ' % opponent(player)
	else:
		print 'Illegal Move'


# validate a move
def validMove(move,player):
	# format validation - same for 'move' and 'drop'
	if not moveFormatCheck(move):
		return False
	
	# type-specific checks
	moveType=move[0]
	if moveType=="move":
		# for "move"
		#print 'debug: move check'
		begPos=move[1]
		endPos=move[2]
		promote=len(move)==4

		# beg and end position are valid
		if not inRange(begPos) or not inRange(endPos):
			return False
		# piece belong to the right player
		if pieceOwner(begPos)!=player:
			#print '>>debug: player error'
			return False
		# endPos does not already have another piece of the same player
		if get(endPos)!='' and get(endPos).islower()==(player=="lower"):
			#print '>>debug: endPos error'
			return False
		'''
		Promotion checks
		1) promoted piece cannot be promoted again
		2) promotion must happen when piece moves into/ within/ out of promotion zone
		//3) pawns must be promoted when entering promotion zone
		4) king and gold general cannot be promoted
		'''
		#print 'debug: promote check'
		if promote and len(get(begPos))>=2:
			return False
		if promote and not inPromotionZone(begPos,player) and not inPromotionZone(endPos,player):
			return False
		# if get(begPos).lower()=='p' and inPromotionZone(endPos,player) and not promote:
		# 	return False
		if promote and get(begPos).lower() in ('k','g'):
			return False

		# piece can move to endPos based on rules for specific piece
		if not canMove(begPos,endPos):
			#print 'debug:canMove=False'
			return False

	else:
		# for "drop", NOTE: all piece inputs are in lowercase here
		piece=move[1]
		endPos=move[2]
		'''
		1) one can only drop a piece in its capture
		2) drop position should be in range
		3) drop position should not have another piece
		'''
		if not inCapture(piece,player) or not inRange(endPos) or get(endPos)!='':
			return False
		'''
		4) pawn may not be dropped into promotion zone
		5) pawn may not be dropped into a square that results in immediate checkmate
		6) two unpromoted pawns may not lie in the same colunm when they belong to the same player
		'''
		if piece=='p' and inPromotionZone(endPos,player):
			return False
		if piece=='p':
			set(endPos,piece)
			if checkmate(opponent(player)):
				set(endPos,'')
				return False
			set(endPos,'')
		if piece=='p':
			j=getCol(endPos)
			for i in range(0,5):
				piece=State['Board'][i][j]
				if piece.lower()=='p' and piece.islower()==player.islower():
					return False
	return True

def executeMove(move,player):
	'''
	possible results for 'move':
	1) normal move
	2) capturing (capture unpromoted/ promoted piece)
	3) promotion (forced pawn promotion)
	'''
	'''
	possible results for 'drop':
	1) normal drop
	'''
	moveType=move[0]
	if moveType=='move':
		begPos=move[1]
		endPos=move[2]
		promote=len(move)==4
		piece=get(begPos)

		set(begPos,'')
		if get(endPos)!='':
			addToCapture(player,get(endPos))
		if promote:
			piece='+'+piece
		elif  piece.lower()=='p' and inPromotionZone(endPos,player):
			piece='+'+piece
		set(endPos,piece)
	else:
		piece=move[1]
		endPos=move[2]
		set(endPos,removeFromCapture(player,piece))

def display():
	print(utils.stringifyBoard(State['Board']))
	print("Captures UPPER: %s" % " ".join(State['Cap_U']))
	print("Captures lower: %s\n" % " ".join(State['Cap_l']))

def displayAction(player,move):
	print '%s player action: %s' % (player," ".join(move))

# helper methods

# add component's piece into player's capture list
def addToCapture(player,piece):
	# preprocess if piece was promoted
	if piece[0]=='+':
		piece=piece[1]
	# add
	if player=='lower':
		State['Cap_l'].append(piece.lower())
	else:
		State['Cap_U'].append(piece.upper())

# remove lowercase piece from player's capture list and return
def removeFromCapture(player,piece):
	piece=piece if player=='lower' else piece.upper()
	if player=='lower':
		State['Cap_l'].remove(piece)
	else:
		State['Cap_U'].remove(piece)
	return piece

# check if the player is checkmated by opponent
def checkmate(player):
	# find the king
	king='k' if player=='lower' else 'K'
	for i in range(0,5):
		for j in range(0,5):
			if State['Board'][i][j]==king:
				kingPos=chr(ord('a')+j)+str(i+1)
				break

	# check if opponent's any pieces can take over the king
	for i in range(0,5):
		for j in range(0,5):
			piece=State['Board'][i][j]
			if piece!='' and piece.islower()!=king.islower():
				pos=chr(ord('a')+j)+str(i+1)
				if canMove(pos,kingPos):
					return True
	return False

def opponent(player):
	return 'lower' if player=='UPPER' else 'UPPER'

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

def inCapture(piece,player):
	if player=='lower':
		return piece in State['Cap_l']
	else:
		return piece.upper() in State['Cap_U']

def inPromotionZone(pos,player):
	if player=="lower":
		return pos[1]=='5'
	else:
		return pos[1]=='1'

# check if the piece on begPos can be moved to endPos in one step
def canMove(begPos,endPos):
	piece=get(begPos)
	piece_type=piece.lower()
	diff=[]
	if piece.islower():
		diff=[ord(begPos[1])-ord(endPos[1]),ord(endPos[0])-ord(begPos[0])]
	else:
		diff=[ord(endPos[1])-ord(begPos[1]),ord(endPos[0])-ord(begPos[0])]
	
	if piece_type=='k':
		return canMove_k(begPos,endPos,diff)
	elif piece_type=='g':
		return canMove_g(begPos,endPos,diff)
	elif piece_type=='s':
		return canMove_s(begPos,endPos,diff)
	elif piece_type=='p':
		return canMove_p(begPos,endPos,diff)
	elif piece_type=='r':
		return canMove_r(begPos,endPos,diff)
	elif piece_type=='b':
		return canMove_b(begPos,endPos,diff)
	elif piece_type=='+s':
		return canMove_g(begPos,endPos,diff)
	elif piece_type=='+b':
		return canMove_b(begPos,endPos,diff) or canMove_k(begPos,endPos,diff)
	elif piece_type=='+r':
		return canMove_r(begPos,endPos,diff) or canMove_k(begPos,endPos,diff)
	elif piece_type=='+p':
		return canMove_g(begPos,endPos,diff)

# canMove based on type of piece
def canMove_k(begPos,endPos,diff):
	return diff in config.MoveRules['k']

def canMove_g(begPos,endPos,diff):
	return diff in config.MoveRules['g']

def canMove_s(begPos,endPos,diff):
	return diff in config.MoveRules['s']

def canMove_p(begPos,endPos,diff):
	return diff in config.MoveRules['p']

def canMove_r(begPos,endPos,diff):
	if diff[0]!=0 and diff[1]!=0:
		return False;
	return canMove_rb(begPos,endPos,diff)

def canMove_b(begPos,endPos,diff):
	if abs(diff[0])!=abs(diff[1]):
		return False
	return canMove_rb(begPos,endPos,diff)

def canMove_rb(begPos,endPos,diff):
	piece=get(begPos)
	di=0 if diff[0]==0 else diff[0]/abs(diff[0])
	dj=0 if diff[1]==0 else diff[1]/abs(diff[1])
	di=-di if piece.islower() else di
	i=ord(begPos[1])-ord('1')
	j=ord(begPos[0])-ord('a')
	while i!=getRow(endPos) and j!=getCol(endPos):
		i+=di
		j+=dj
		if State['Board'][i][j]!='':
			return False
	return True

def pieceOwner(pos):
	piece=get(pos)
	if len(piece)==2 and piece[0]=='+':
		piece=piece[1]
	if piece in ('p','g','k','s','b','r'):
		return "lower"
	elif piece in ('P','G','K','S','B','R'):
		return "UPPER"
	else:
		return ""

def set(pos,piece):
	State['Board'][getRow(pos)][getCol(pos)]=piece

def get(pos):
	return State['Board'][getRow(pos)][getCol(pos)]

def getRow(pos):
	return ord(pos[1])-ord('1')

def getCol(pos):
	return ord(pos[0])-ord('a')

def inRange(pos):
	return len(pos)==2 and pos[0] in ('a','b','c','d','e') and pos[1] in ('1','2','3','4','5')


if __name__=="__main__":
	# verify and process arguments
	if not processArgv(sys.argv):
		# invalid argv
		print "invalid arguments"
		sys.exit(1)

	#display()
	# print("State:")
	# print(State)
	play()