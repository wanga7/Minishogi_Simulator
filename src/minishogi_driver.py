'''
Author: Anjie Wang
File: minishogi_driver.py
Descrition: 
'''

from minishogi import Minishogi
import sys
import utils
import config

# verify and process arguments
def processArgv(argv):
	if len(argv)==2 and argv[1]=="-i":
		#interactive mode
		return Minishogi(utils.parseTestCase(config.DEFAULT_STATE_FILEPATH),'i')
	elif len(argv)==3 and argv[1]=="-f":
		# file mode
		return Minishogi(utils.parseTestCase(argv[2]),'f')
	else:
		# invalid argvs
		return None

if __name__=="__main__":
	game=processArgv(sys.argv)
	if game!=None:
		game.play()
	else:
		print 'invalid arguments'