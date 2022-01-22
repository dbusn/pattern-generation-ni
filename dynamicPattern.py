import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from staticPattern import staticPattern

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

#P[j][E[j]][0] is a set of e's, a subset of (4,6), with dT on last index

def dynamicPattern(P, D, A, F, G_F, W):
	dT = P[0] #ms

	for j in range(2):
		staticPattern(E = P[1][j], a = A[j], f = F[j], d = D[j], g_f = G_F[j], w = W[j]) # E and d are not correct yet

