'''
Author: Anjie Wang
File: board.py
Descrition: implement a Minishogi board and related methods
'''

import config

class Board:
	# initialize board state
	def __init__(self,pieces):
		self._board=[]	# stores state of the board
		self._lowerKingPos=''	# stores location of 'lower' player's 'king'
		self._upperKingPos=''	# stores location of 'UPPER' player's 'king'

		for i in range(0,config.BOARD_SIZE):
			row=[]
			for j in range(0,config.BOARD_SIZE):
				row.append('')
			self._board.append(row)
		
		for p in pieces:
			self.set(p['position'],p['piece'])
			if p['piece'].lower()=='k':
				self.updateKingPos(p['piece'],p['position'])

	# put piece on specific position of the board
	def set(self,pos,piece):
		self._board[self.getRow(pos)][self.getCol(pos)]=piece
		if piece.lower()=='k':
			self.updateKingPos(piece,pos)

	# put piece on specific position of the board
	def set_ij(self,i,j,piece):
		self.set(ijToPos(i,j),piece)

	# get the piece at specific position of the board
	def get(self,pos):
		return self._board[self.getRow(pos)][self.getCol(pos)]

	# get the piece at specific position of the board
	def get_ij(self,i,j):
		return self._board[i][j]

	# get the row number of a position string
	def getRow(self,pos):
		return ord(pos[1])-ord('1')

	# get the column number of a position string
	def getCol(self,pos):
		return ord(pos[0])-ord('a')

	# check if a position is in board range
	def inRange(self,pos):
		return len(pos)==2 and 'a'<=pos[0]<chr(ord('a')+config.BOARD_SIZE) and '1'<=pos[1]<chr(ord('1')+config.BOARD_SIZE)

	# check if a position is in board range
	def inRange_ij(self,i,j):
		return 0<=i<config.BOARD_SIZE and 0<=j<config.BOARD_SIZE

	# transform numerical position index to position string
	def ijToPos(self,i,j):
		return chr(ord('a')+j)+str(i+1)

	# get the position of the player's 'king' piece
	def getKingPos(self,player):
		return self._lowerKingPos if player==config.LOWER_PLAYER else self._upperKingPos

	# update the position of the player's 'king' piece
	def updateKingPos(self,piece,pos):
		if piece=='k':
			self._lowerKingPos=pos
		else:
			self._upperKingPos=pos

	# check if the position is in the player's promotion zone
	def inPromotionZone(self,pos,player):
		return pos[1]==str(config.BOARD_SIZE) if player==config.LOWER_PLAYER else pos[1]=='1'