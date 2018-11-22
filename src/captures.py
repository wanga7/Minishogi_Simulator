'''
Author: Anjie Wang
File: captures.py
Descrition: 
'''

import config

class Captures:
	def __init__(self,initialState):
		self._caps={}
		self._caps[config.UPPER_PLAYER]=initialState['upperCaptures']
		self._caps[config.LOWER_PLAYER]=initialState['lowerCaptures']

	# add oppponent's piece into player's capture list
	def addToCapture(self,player,piece):
		# preprocess if piece was promoted
		if piece[0]=='+':
			piece=piece[1]
		# add
		self._caps[player].append(piece.lower() if player==config.LOWER_PLAYER else piece.upper())
		# if player=='lower':
		# 	self._cap_l.append(piece.lower())
		# else:
		# 	self._cap_U.append(piece.upper())

	# remove lowercase piece from player's capture list and return
	def removeFromCapture(self,player,piece):
		piece=piece if player==config.LOWER_PLAYER else piece.upper()
		self._caps[player].remove(piece)
		# if player=='lower':
		# 	self._cap_l.remove(piece)
		# else:
		# 	self._cap_U.remove(piece)
		return piece

	def inCapture(self,piece,player):
		return (piece if player==config.LOWER_PLAYER else piece.upper()) in self._caps[player]
	
	def getCaptures(self,player):
		return self._caps[player]