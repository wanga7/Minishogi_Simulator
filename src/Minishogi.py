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
	if State['Mode']=='i':
		display()

	endReason=''
	stepCnt=0
	inCheck=False
	solutions=[]
	while validGame:
		# switch side
		player=opponent(player)

		# check checkmate situation
		# print 'debug: checkmate(%s)' % player
		inCheck=False
		threats=checkmate(player)
		# print 'debug: threats: %s' % threats
		solutions=[]
		if len(threats)>0:
			inCheck=True
			# find available moves for player
			solutions=solveCheck(player,threats)

			if State['Mode']=='i' and len(solutions)>0:
				displaySolutions(player,solutions)
			if len(solutions)==0:
				player=opponent(player)
				endReason=config.CHECK_MSG
				validGame=False
				break
		
		# check move limit
		if validGame and stepCnt==config.MOVE_LIMIT:
			player=opponent(player)
			endReason=config.TIE_MSG
			validGame=False
			break

		# read in next move (-i,-f)
		if State['Mode']=="i":
			move=raw_input(player+'> ').split(' ')
			displayAction(player,move)
		else:
			if stepCnt>=len(State['Moves']):
				player=opponent(player)
				validGame=False
				break
			else:
				move=State['Moves'][stepCnt].split(' ')

		# verify the move
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
	
	# handling game result
	if State['Mode']=='f':
		displayAction(player,move)
		display()
		if endReason==config.TIE_MSG:
			print endReason
		elif endReason==config.ILLEGAL_MSG:
			print '%s player wins.  %s' % (opponent(player),endReason)
		elif endReason==config.CHECK_MSG:
			print '%s player wins.  %s' % (player,endReason)
		else:
			if inCheck:
				displaySolutions(opponent(player),solutions)
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

		# cannot move into check
		tmp=get(endPos)
		piece=get(begPos)
		set(begPos,'')
		set(endPos,piece)
		inCheck=len(checkmate(player))>0
		set(begPos,piece)
		set(endPos,tmp)
		if inCheck:
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
			if len(checkmate(opponent(player)))>0:
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

# display functions

def display():
	print(utils.stringifyBoard(State['Board']))
	print("Captures UPPER: %s" % " ".join(State['Cap_U']))
	print("Captures lower: %s\n" % " ".join(State['Cap_l']))

def displayAction(player,move):
	print '%s player action: %s' % (player," ".join(move))

def displaySolutions(player,solutions):
	print '%s player is in check!\nAvailable moves:' % player
	print '\n'.join(solutions)

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

# check if the player in check, return threats
def checkmate(player):
	kingPos=getKingPos(player)

	# check if opponent's any pieces can take over the king
	threats=[]
	for i in range(0,5):
		for j in range(0,5):
			piece=get_ij(i,j)
			if piece!='' and piece.islower()!=player.islower():
				pos=ijToPos(i,j)
				if canMove(pos,kingPos):
					threats.append(pos)
	return threats

def solveCheck(player,threats):
	'''
	Ways to solve check
	1) remove king from danger
	2) capture the piece that threatens the king (infeasible if there're multiple threats)
	3) put another piece between the king and the threat (infeasible if multiple threats)
	?) do solutions contain promotions?
	'''
	#print 'debug: threats=%s' % threats
	solutions=[]
	dropPoses=[]
	kingPos=getKingPos(player)
	if len(threats)==1:
		dropPoses=checkRoute(getRow(threats[0]),getCol(threats[0]),getRow(kingPos),getCol(kingPos))
		#print 'debug: dropPoses=%s' % dropPoses
	for i in range(0,5):
		for j in range(0,5):
			piece=get_ij(i,j)
			piece_type=piece.lower()
			pos=ijToPos(i,j)
			if piece!='' and piece.islower()==player.islower():
				# try 'move's
				if piece_type=='k' or len(threats)==1:
					for m in config.MoveRules[piece_type]:
						nextPos=ijToPos(i+m[0],j+m[1])
						moveOption=['move',pos,nextPos]
						if validMove(moveOption,player):
							tmp=get(nextPos)
							set(nextPos,piece)
							set(pos,'')
							if len(checkmate(player))==0:
								solutions.append(' '.join(moveOption))
							set(nextPos,tmp)
							set(pos,piece)
			elif piece=='' and len(threats)==1 and [i,j] in dropPoses:
				# try 'drop's
				#print 'debug: try drop at %d,%d' % (i,j)
				CapList=State['Cap_l'] if player=='lower' else State['Cap_U']
				for cap_p in CapList:
					moveOption=['drop',cap_p.lower(),pos]
					if validMove(moveOption,player):
						solutions.append(' '.join(moveOption))
	solutions.sort()
	return solutions

# return a list of positions between threat and king
def checkRoute(threat_i,threat_j,king_i,king_j):
	#print 'debug: checkRoute %d,%d -> %d,%d' % (threat_i,threat_j,king_i,king_j)
	routes=[]
	diff=[king_i-threat_i,king_j-threat_j]
	di=0 if diff[0]==0 else diff[0]/abs(diff[0])
	dj=0 if diff[1]==0 else diff[1]/abs(diff[1])
	i=threat_i+di
	j=threat_j+dj
	while i!=king_i or j!=king_j:
		routes.append([i,j])
		i+=di
		j+=dj
	return routes

def getKingPos(player):
	king='k' if player=='lower' else 'K'
	for i in range(0,5):
		for j in range(0,5):
			if State['Board'][i][j]==king:
				return ijToPos(i,j)
	return ''

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
	# print 'debug: piece=%s' % piece
	piece_type=piece.lower()
	# print 'debug: piece_type=%s' % piece_type
	diff=[]
	if piece.islower():
		diff=[ord(begPos[1])-ord(endPos[1]),ord(endPos[0])-ord(begPos[0])]
	else:
		diff=[ord(endPos[1])-ord(begPos[1]),ord(endPos[0])-ord(begPos[0])]
	# print 'debug: diff=%s' % diff
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
		# print 'debug: canMove_r, begPos=%s,endPos=%s' % (begPos,endPos)
		# print 'debug: canMove_r=%r' % canMove_r(begPos,endPos,diff)
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
	#print 'debug: canMove_r beg:%s, end:%s' % (begPos,endPos)
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
	
	i=getRow(begPos)+di
	j=getCol(begPos)+dj
	# print 'debug: canmove_rb,%d,%d' % (i,j)
	# print 'debug: canmove_rb,end,%d,%d' % (getRow(endPos),getCol(endPos))
	while i!=getRow(endPos) or j!=getCol(endPos):
		# print 'debug: canmove_rb,while,%d,%d' % (i,j)
		if State['Board'][i][j]!='':
			return False
		i+=di
		j+=dj
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

def set_ij(i,j,piece):
	State['Board'][i][j]=piece

def get(pos):
	return State['Board'][getRow(pos)][getCol(pos)]

def get_ij(i,j):
	return State['Board'][i][j]

def getRow(pos):
	return ord(pos[1])-ord('1')

def getCol(pos):
	return ord(pos[0])-ord('a')

def inRange(pos):
	return len(pos)==2 and pos[0] in ('a','b','c','d','e') and pos[1] in ('1','2','3','4','5')

def inRange_ij(i,j):
	return 0<=i<5 and 0<=j<5

def ijToPos(i,j):
	return chr(ord('a')+j)+str(i+1)


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