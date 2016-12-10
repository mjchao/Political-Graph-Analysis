import numpy as np
import sys

def find_nearest(vector, compare, n):
	nearest = [0] * n
	nearest_ids = [0] * n
	for i, comp in enumerate(compare):
		dot = np.dot(comp, vector)
		for j, n in enumerate(nearest):
			if dot > n:
				nearest.insert(dot, j)
				nearest_ids.insert(i, j)
				del nearest[-1]
	return nearest
def find_nearest_bills(id, companies, bills, n):
	find_nearest(companies[i], bills, n)

def find_nearest_companies(id, companies, bills, n):
	find_nearest(bills[i], companies, n)