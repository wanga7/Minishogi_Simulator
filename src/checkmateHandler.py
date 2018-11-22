'''
Author: Anjie Wang
File: checkmateHandler.py
Descrition: implement checkmate-related methods
'''

from board import Board
from captures import Captures
import verification
import config


# check if the player in check, return a list of positions of opponent's pieces that threats the 'king'
def checkmate(player,board):
	kingPos=board.getKingPos(player)

	# check if opponent's pieces can threat the king
	threats=[]
	for i in range(0,config.BOARD_SIZE):
		for j in range(0,config.BOARD_SIZE):
			piece=board.get_ij(i,j)
			if piece!='' and not verification.ownPiece(player,piece):
				pos=board.ijToPos(i,j)
				if verification.canMove(pos,kingPos,board):
					threats.append(pos)
	return threats

# return a list of all possible moves for the player to solve the 'in check' situation
def solveCheck(player,threats,board,captures):
	'''
	Ways to solve check
	1) remove king from danger
	2) capture the piece that threatens the king (impossible if multiple threats)
	3) put another piece between the king and the threat (impossible if multiple threats)
	'''
	solutions=[]
	kingPos=board.getKingPos(player)
	dropPoses=[]
	if len(threats)==1:
		dropPoses=checkRoute(threats[0],kingPos,board)
	
	for i in range(0,config.BOARD_SIZE):
		for j in range(0,config.BOARD_SIZE):
			piece=board.get_ij(i,j)
			piece_type=piece.lower()
			pos=board.ijToPos(i,j)

			if piece!='' and verification.ownPiece(player,piece) and (piece_type=='k' or len(threats)==1):
				# try 'move's
				for m in config.MoveRules[piece_type]:
					nextPos=board.ijToPos(i+m[0],j+m[1])
					moveOption=['move',pos,nextPos]
					if verification.validMove(moveOption,player,board,captures) and not movingIntoCheck(pos,nextPos,player,board):
						solutions.append(' '.join(moveOption))
			elif piece=='' and len(threats)==1 and [i,j] in dropPoses:
				# try 'drop's
				for cap_p in captures.getCaptures(player):
					moveOption=['drop',cap_p.lower(),pos]
					if verification.validMove(moveOption,player,board,captures):
						solutions.append(' '.join(moveOption))
	
	# sort solutions based on alphabetical order
	solutions.sort()
	return solutions

# return a list of positions on the route between the king and the piece that checks the king
def checkRoute(threatPos,kingPos,board):
	ti=board.getRow(threatPos)
	tj=board.getCol(threatPos)
	ki=board.getRow(kingPos)
	kj=board.getCol(kingPos)
	routes=[]
	diff=[ki-ti,kj-tj]
	di=0 if diff[0]==0 else diff[0]/abs(diff[0])
	dj=0 if diff[1]==0 else diff[1]/abs(diff[1])
	i=ti+di
	j=tj+dj
	while i!=ki or j!=kj:
		routes.append([i,j])
		i+=di
		j+=dj
	return routes

# check if this move will result in a check for the player itself
def movingIntoCheck(begPos,endPos,player,board):
	endPiece=board.get(endPos)
	begPiece=board.get(begPos)
	
	# try the move
	board.set(begPos,'')
	board.set(endPos,begPiece)
	inCheck=len(checkmate(player,board))>0
	
	# reverse the move
	board.set(begPos,begPiece)
	board.set(endPos,endPiece)
	return inCheck