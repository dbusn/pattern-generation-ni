import sys
import string
from staticPattern import generateRandomPattern, generateGIF

if __name__ == '__main__':
	if(len(sys.argv) < 2):
		print('Number of patterns missing')
		print('Pass number of patterns as an argument')
		sys.exit(1)

	if(sys.argv[1].isnumeric() is False):
		print('Illegal arguments provided')
		sys.exit(2)

	min_actuators = 4
	max_actuators = 8
	n_patterns = int(sys.argv[1])
	for i in range(n_patterns):
		p_name = 'p_' + str(i)
		generateGIF(p_name, generateRandomPattern(p_name, min_actuators, max_actuators)[1])