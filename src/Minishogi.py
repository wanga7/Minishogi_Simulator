'''
Author: Anjie Wang
File: Minishogi.py
Descrition: 
'''

from board import Board
from captures import Captures
import verification
import checkmateHandler
import config
import string
import utils

class Minishogi:
	def __init__(self,initialState,mode):
		self._board=Board(initialState['initialPieces'])
		self._captures=Captures(initialState)
		self._moves=initialState['moves']
		self._mode=mode

	def play(self):
		validGame=True
		player='UPPER'
		if self._mode=='i':
			self.display()

		endReason=''
		stepCnt=0
		inCheck=False
		solutions=[]

		while validGame:
			# switch side
			player=self.opponent(player)

			# check checkmate situation
			threats=checkmateHandler.checkmate(player,self._board)
			inCheck=len(threats)>0
			solutions=[]
			if inCheck:
				# find available moves for player
				solutions=checkmateHandler.solveCheck(player,threats,self._board,self._captures)

				if self._mode=='i' and len(solutions)>0:
					self.displaySolutions(player,solutions)
				if len(solutions)==0:
					# no solution is found, game ends
					endReason=config.CHECK_MSG
					validGame=False
					break
		
			# check move limit
			if validGame and stepCnt==config.MOVE_LIMIT:
				endReason=config.TIE_MSG
				validGame=False
				break

			# read in next move (-i,-f)
			if self._mode=='i':
				move=raw_input(player+'> ').split(' ')
				self.displayAction(player,move)
			else:
				if stepCnt>=len(self._moves):
					validGame=False
					break
				else:
					move=self._moves[stepCnt].split(' ')

			# verify the move and execute
			if verification.validMove(move,player,self._board,self._captures):
				self.executeMove(move,player)
				stepCnt+=1
				if self._mode=='i':
					self.display()
			else:
				endReason=config.ILLEGAL_MSG
				validGame=False
	
		# handling game result
		if self._mode=='f':
			self.displayAction(player if endReason==config.ILLEGAL_MSG else self.opponent(player),move)
			self.display()
		if endReason!='':
			self.displayEndResult(endReason,self.opponent(player))
		else:
			if inCheck:
				self.displaySolutions(player,solutions)
			print '%s> ' % player

	def displayEndResult(self,endReason,player):
		if endReason==config.TIE_MSG:
			print endReason
		elif endReason!='':
			print '%s player wins.  %s' % (player,endReason)

	def executeMove(self,move,player):
		if move[0]=='move':
			'''
			for 'move':
			1) normal move
			2) capturing (capture unpromoted/ promoted piece)
			3) promotion (forced pawn promotion)
			'''
			begPos=move[1]
			endPos=move[2]
			promote=len(move)==4
			piece=self._board.get(begPos)

			self._board.set(begPos,'')
			if self._board.get(endPos)!='':
				self._captures.addToCapture(player,self._board.get(endPos))
			if promote:
				piece='+'+piece
			elif  piece.lower()=='p' and self._board.inPromotionZone(endPos,player):
				piece='+'+piece
			self._board.set(endPos,piece)
		else:
			# for 'drop'
			piece=move[1]
			endPos=move[2]
			self._board.set(endPos,self._captures.removeFromCapture(player,piece))

	# display functions

	def display(self):
		print(utils.stringifyBoard(self._board._board))
		print('Captures UPPER: %s' % ' '.join(self._captures.getCaptures(config.UPPER_PLAYER)))
		print('Captures lower: %s\n' % ' '.join(self._captures.getCaptures(config.LOWER_PLAYER)))

	def displayAction(self,player,move):
		print '%s player action: %s' % (player,' '.join(move))

	def displaySolutions(self,player,solutions):
		print '%s player is in check!\nAvailable moves:' % player
		print '\n'.join(solutions)

	def opponent(self,player):
		return 'lower' if player=='UPPER' else 'UPPER'




