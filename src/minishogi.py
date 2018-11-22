'''
Author: Anjie Wang
File: minishogi.py
Descrition: implement a minishogi game
'''

from board import Board
from captures import Captures
import verification
import checkmateHandler
import config
import utils

class Minishogi:
	# intialize game state
	def __init__(self,initialState,mode):
		self._board=Board(initialState['initialPieces'])	# Board object that stores state of the game board
		self._captures=Captures(initialState)	# Captures object that stores state of players' capture lists
		self._moves=initialState['moves']	# a list of moves in file mode ('-f')
		self._mode=mode 	# game mode

		self.validGame=True 	# game is finished or not
		self.player=config.UPPER_PLAYER 	# current player in the game
		self.endReason='' 	# ending reason for the game
		self.stepCnt=0 		# number of moves in the game
		self.inCheck=False 	# if there is a check situaion at current round of the game
		self.solutions=[] 	# list of moves to solve the 'check' situation at current round

	# play the game
	def play(self):
		if self._mode=='i':
			self.display()

		while self.validGame:
			# switch side
			self.player=self.opponent(self.player)

			# check checkmate situation
			self.checkmateSituation()
			if not self.validGame:
				break
		
			# check move limit
			if self.validGame and self.stepCnt==config.MOVE_LIMIT:
				self.endReason=config.TIE_MSG
				self.validGame=False
				break

			# read in next move (-i,-f)
			if self._mode=='i':
				move=raw_input(player+'> ').split(' ')
				self.displayAction(self.player,move)
			else:
				if self.stepCnt>=len(self._moves):
					self.validGame=False
					break
				else:
					move=self._moves[self.stepCnt].split(' ')

			# verify the move and execute
			if verification.validMove(move,self.player,self._board,self._captures):
				self.executeMove(move,self.player)
				self.stepCnt+=1
				if self._mode=='i':
					self.display()
			else:
				self.endReason=config.ILLEGAL_MSG
				self.validGame=False
	
		# handling game result
		if self._mode=='f':
			self.displayAction(self.player if self.endReason==config.ILLEGAL_MSG else self.opponent(self.player),move)
			self.display()
		if self.endReason!='':
			self.displayEndResult(self.endReason,self.opponent(self.player))
		else:
			if self.inCheck:
				self.displaySolutions(self.player,self.solutions)
			print '%s> ' % self.player

	# check if there is a 'check' situation and find suggestions for the player
	def checkmateSituation(self):
		threats=checkmateHandler.checkmate(self.player,self._board)
		self.inCheck=len(threats)>0
		self.solutions=[]
		if self.inCheck:
			# find available moves for player
			self.solutions=checkmateHandler.solveCheck(self.player,threats,self._board,self._captures)

			if self._mode=='i' and len(self.solutions)>0:
				self.displaySolutions(self.player,self.solutions)
			if len(self.solutions)==0:
				# no solution is found, game ends
				self.endReason=config.CHECK_MSG
				self.validGame=False

	# execute a move (assume the move has already been verified)
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

	# display current state of the game (board and capture lists)
	def display(self):
		print(utils.stringifyBoard(self._board._board))
		print('Captures UPPER: %s' % ' '.join(self._captures.getCaptures(config.UPPER_PLAYER)))
		print('Captures lower: %s\n' % ' '.join(self._captures.getCaptures(config.LOWER_PLAYER)))

	# display current move 
	def displayAction(self,player,move):
		print '%s player action: %s' % (player,' '.join(move))

	# display solutions to the current 'check' situation
	def displaySolutions(self,player,solutions):
		print '%s player is in check!\nAvailable moves:' % player
		print '\n'.join(solutions)

	# display result of the game
	def displayEndResult(self,endReason,player):
		if endReason==config.TIE_MSG:
			print endReason
		elif endReason!='':
			print '%s player wins.  %s' % (player,endReason)

	# get the opponent of the player
	def opponent(self,player):
		return 'lower' if player=='UPPER' else 'UPPER'