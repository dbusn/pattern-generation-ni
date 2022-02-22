from distinguishability.staticPattern import staticPattern
import numpy as np

# # type of E_j: 'set' which is a subset of (4,6), e in E, e[0] is '4', e[1] is '6'
# P_j is for j=3: [P_1, P_2, P_3]
# P_j is a list of 2 rows, where
# 	P_j[0] contains number dt
# 	P_j[1] consists of a list of [E_0, E_1, ..., E_k] such that
# 	each exciter e in E_i starts at time i * dt

# D_j is a list of durations, where D_j[i] is the amount of
# 	time the exciters in P_j[1][i] is active
# A_j is a list of amplitudes where A_j[i] is the amplitude
# 	of the group wave for the exciters in P_j[1][i]
# F_j
# G_F_j
# W_j

# P[j][E[j]][0] is a set of e's, a subset of (4,6), with dT on last index

def dynamicPattern(P, D, A, F, G_F, W):
	"""
	#TODO: add drawing somewhere

	We say 'extra' is a parameter either a or f.
	We say 'x' is from top view of the grid the x-coordinate
	We say 'y' is from top view of the grid the y-coordinate

	We say 'dt[i]' is t_start[i] - t_start[i-1] (see drawing)

	:param P: (array) P = P[P_1,P_2,...]. P_j=[P_j[0],P_j[1]], where P_j[0] = dt,
		      P_j[1] = [E_0,E_1,...], where e in E_i starts at time i*dt.
	:param D: (array) list of durations. D_j = [D_j[0],D_j[1],...],
			  where D_j[i] is the amount of time the exciters in P_j[1][i] is active.
	:param A: (array) list of amplitudes. A_j = [A_j[0],A_j[1],...],
			  where A_j[i] is the amplitude of the exciters in P_j[1][i].
	:param F: (array) list of frequencies. F_j = [F_j[0],F_j[1],...],
			  where F_j[i] is the frequency of the exciters in P_j[1][i].
	:param G_F: (array) list of group frequencies. G_F_j = [G_F_j[0],G_F_j[1],...],
			  where G_F_j[i] is the group frequency of the exciters in P_j[1][i].
	:param W: (array) list of wave types. W_j = [W_j[0],W_j[1],...],
			  where W_j[i] is the wave type of the exciters in P_j[1][i].
	:return: array: (array) an array representing the pattern in video form. array = array[time][x][y][extra].
			 note that array[][][][0] gives the frequency, and array[][][][1] gives the amplitude.
	"""

	discretization = sum([sum(D[i]) for i in range(len(D))]) // 10
	array = np.zeros(size=(discretization,4,6,2)) #maybe useful to make this a custom class


	# for j in range(len(P)):
	# 	for i in range(len(P)):
	# 		if W[j][i] == 'constant':
	# 			for timestep in range(D[][]):
	# 				for e in [P[j][1][i]]:
	# 					array[timestep][P[j][1][i]][0] =
	# 					array[timestep][P[j][1][i]][0] =

# Example input, |j|=2
dt_example = [0 for _ in range(2)]

e_111 = [2, 4]
e_112 = [2, 3]
E_11 = [e_111, e_112]

e_121 = [1, 2]
e_122 = [2, 2]
E_12 = [e_121, e_122]

E_example = [E_11, E_12]
P_1 = [dt_example, E_example] #E['dt',[E_11,E_12]]
P_2 = P_1
P = [P_1,P_2]  # [[[dt_example],[[E_11],[E_12]]], [[dt_example],[[E_21],[E_22]]]]
print(P)

D_1 = [400, 400]
D_2 = [200, 200]
D = [D_1, D_2]
# print(sum([sum(D[i]) for i in range(len(D))]))

A_1 = [250, 250]
A_2 = [250, 250]
A = [A_1, A_2]

F_1 = [300, 300]
F_2 = [60, 60]
F = [F_1, F_2]

G_F_1 = [30, 30]
G_F_2 = [30, 30]
G_F = [G_F_1, G_F_2]

W_1 = ['constant', 'constant']
W_2 = ['sawtooth', 'sawtooth']
W = [W_1, W_2]
