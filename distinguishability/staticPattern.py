import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# type of E: 'set' which is a subset of (4,6), e in E, e[0] is '4', e[1] is '6'
# type of D: duration in of the pattern (integer in ms)
# type of G_f: frequency of wave type (integer)
# type of W: string, denoting the wave type

def staticPattern(E, a, f, d, g_f, w):
	"""
	#TODO: add drawing
	We say 'extra' is a parameter either a or f.
	We say 'x' is from top view of the grid the x-coordinate
	We say 'y' is from top view of the grid the y-coordinate

	:param E: (array) subset of whole grid. E = E[e_1,e_2,...]. For each e in E: x=e[0], y=e[1]
	:param a: (int) one of all amplitudes. a = a in A
	:param f: (int) one of all frequencies. f = f in F
	:param d: (int) one of all durations. d = d in D ()
	:param g_f: (int) one of all group frequencies. g_f = g_f in G_f
	:param w: (str) one of all wave types. w = w in W
	:return: array: (array) an array representing the pattern in video form. array = array[time][x][y][extra].
			 note that array[][][][0] gives the frequency, and array[][][][1] gives the amplitude.
	"""

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
		# Note that we assume a sine wave y = A sin(B(x-phi))+D

		#can be calculated from input
		B = 2*np.pi*g_f
		A = (max_amp - 0.5*max_amp)/2   # assuming a sin wave with 0.5*max_amp amplitude
		D = max_amp - A  				# wave between max_amp and max_amp/2

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
		#TODO: add explanation of theoretic function from signal.sawtooth

		#can be calculated from input
		B = 2*np.pi*g_f

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
		# Note that we assume a hanning window y = 0.5(1 - cos(2pin/N)), 0 <= n <= N
		# This function is built in into numpy as hanning(discretization_rate).

		#create amplitude list
		amplitude_list = max_amp * np.hanning(discretization) #hanning window

		for timestep in range(discretization):
			for e in E:
				array[timestep][e[0]][e[1]][0] = f
				array[timestep][e[0]][e[1]][1] = amplitude_list[timestep]

	elif w == 'block':
		# Note that we assume a block function y = 1 if 0 <= x < period, -1 if period < x < 2*period

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

	return array


################# testing: #################
# max_amp = 250
# t = np.linspace(0, 1, 500)
# plt.plot(t, (max_amp*signal.sawtooth(2 * np.pi * t) + max_amp)/2)
# plt.show()

# print((max_amp*signal.sawtooth(2 * np.pi * 5 * t) + max_amp)/2)