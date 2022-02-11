import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# type of E: 'set' which is a subset of (4,6), e in E, e[0] is '4', e[1] is '6'
# type of D: duration in of the pattern (integer in ms)
# type of G_f: frequency of wave type (integer)
# type of W: string, denoting the wave type

def staticPattern(E, a, f, d, g_f, w):
	#TODO: add clear docstring

	#initial values
	max_amp = 250
	discretization = d // 10
	array = np.zeros(size=(discretization,4,6,2)) #maybe useful to make this a custom class

	if w == 'constant':
		for timestep in range(discretization):
			for e in E:
				array[timestep][e[0]][e[1]][0] = f
				array[timestep][e[0]][e[1]][1] = a

	elif w == 'sin':
		#can be calculated from input
		period = 1 / g_f
		B = 2*np.pi*g_f
		A = (max_amp - 0.5*max_amp)/2
		D = max_amp - A

		#for creating wave
		start = 0
		stop = d
		x = np.linspace(start, stop, discretization)

		#create amplitude list
		phi = 0
		amplitude_list = []
		for i in range(len(x)):
			amplitude_list.append((int) (A*np.sin(B*(x[i] - phi)) + D))
		for timestep in range(discretization):
			for e in E:
				array[timestep][e[0]][e[1]][0] = f
				array[timestep][e[0]][e[1]][1] = amplitude_list[timestep]

	elif w == 'sawtooth':
		#can be calculated from input
		period = 1 / g_f
		B = 2*np.pi*g_f
		# A = (max_amp - 0.5*max_amp)/2
		# D = max_amp - A

		#for creating wave
		start = 0
		stop = d
		x = np.linspace(start, stop, discretization)

		#create amplitude list
		phi = 0
		amplitude_list = []
		for i in range(len(x)):
			amplitude_list.append((int) (max_amp*signal.sawtooth(B * (x[i] - phi)) + max_amp)/2)
		for timestep in range(discretization):
			for e in E:
				array[timestep][e[0]][e[1]][0] = f
				array[timestep][e[0]][e[1]][1] = amplitude_list[timestep]

	elif w == 'hanning':
		#create amplitude list
		amplitude_list = max_amp * np.hanning(discretization) #hanning window

		for timestep in range(discretization):
			for e in E:
				array[timestep][e[0]][e[1]][0] = f
				array[timestep][e[0]][e[1]][1] = amplitude_list[timestep]

	elif w == 'block':
		#can be calculated from input
		period = 1 / g_f

		#for creating wave
		start = 0
		stop = d
		x = np.linspace(start, stop, discretization)

		#create amplitude list
		phi = 0
		amplitude_list = []
		for i in range(len(x)):
			if x[i] % 2*period < period: # if 0 <= x < period
				sign = 1
			else:						  # period <= x < 2*period
				sign = -1
			amplitude_list.append((int) (a * sign))
		for timestep in range(discretization):
			for e in E:
				array[timestep][e[0]][e[1]][0] = f
				array[timestep][e[0]][e[1]][1] = amplitude_list[timestep]


	else:
		print("error: wave type unknown")


################# testing: #################
# max_amp = 250
# t = np.linspace(0, 1, 500)
# plt.plot(t, (max_amp*signal.sawtooth(2 * np.pi * t) + max_amp)/2)
# plt.show()

# print((max_amp*signal.sawtooth(2 * np.pi * 5 * t) + max_amp)/2)