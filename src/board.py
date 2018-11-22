'''
Author: Anjie Wang
File: Board.py
Descrition: implement a Minishogi board
'''

import config

class Board:
	def __init__(self,pieces):
		self._board=[]
		self._lowerKingPos=''
		self._upperKingPos=''

		for i in range(0,5):
			row=[]
			for j in range(0,5):
				row.append('')
			self._board.append(row)
		
		for p in pieces:
			self.set(p['position'],p['piece'])
			if p['piece'].lower()=='k':
				self.updateKingPos(p['piece'],p['position'])

	def set(self,pos,piece):
		self._board[self.getRow(pos)][self.getCol(pos)]=piece
		if piece.lower()=='k':
			self.updateKingPos(piece,pos)

	def set_ij(self,i,j,piece):
		self.set(ijToPos(i,j),piece)

	def get(self,pos):
		return self._board[self.getRow(pos)][self.getCol(pos)]

	def get_ij(self,i,j):
		return self._board[i][j]

	def getRow(self,pos):
		return ord(pos[1])-ord('1')

	def getCol(self,pos):
		return ord(pos[0])-ord('a')

	def inRange(self,pos):
		return len(pos)==2 and pos[0] in ('a','b','c','d','e') and pos[1] in ('1','2','3','4','5')

	def inRange_ij(self,i,j):
		return 0<=i<5 and 0<=j<5

	def ijToPos(self,i,j):
		return chr(ord('a')+j)+str(i+1)

	def getKingPos(self,player):
		return self._lowerKingPos if player=='lower' else self._upperKingPos

	def updateKingPos(self,piece,pos):
		if piece=='k':
			self._lowerKingPos=pos
		else:
			self._upperKingPos=pos

	def inPromotionZone(self,pos,player):
		if player=="lower":
			return pos[1]=='5'
		else:
			return pos[1]=='1'

	def pieceOwner(self,piece):
		if len(piece)==2 and piece[0]=='+':
			piece=piece[1]
		
		if piece.lower() not in config.PIECE_TYPE:
			return ''
		else:
			return config.LOWER_PLAYER if piece.islower() else config.UPPER_PLAYER





