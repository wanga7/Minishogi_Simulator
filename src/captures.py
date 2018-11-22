'''
Author: Anjie Wang
File: captures.py
Descrition: implement players' capture lists and related methods
'''

import config

class Captures:
	# initialize capture lists' state
	def __init__(self,initialState):
		self._caps={}	# stores all players' capture lists
		self._caps[config.UPPER_PLAYER]=initialState['upperCaptures']
		self._caps[config.LOWER_PLAYER]=initialState['lowerCaptures']

	# add oppponent's piece into player's capture list
	def addToCapture(self,player,piece):
		# preprocess if piece was promoted
		if piece[0]=='+':
			piece=piece[1]
		# add
		self._caps[player].append(piece.lower() if player==config.LOWER_PLAYER else piece.upper())

	# remove lowercase piece from player's capture list and return the piece
	def removeFromCapture(self,player,piece):
		piece=piece if player==config.LOWER_PLAYER else piece.upper()
		self._caps[player].remove(piece)
		return piece

	# check if the piece is in the player's capture list
	def inCapture(self,piece,player):
		return (piece if player==config.LOWER_PLAYER else piece.upper()) in self._caps[player]
	
	# get the player's capture list
	def getCaptures(self,player):
		return self._caps[player]