import nodes
import graph
import os
import sys
import itertools
import pandas as pd
import copy
import csv

if __name__ == "__main__":
	session = sys.argv[1]
	dataframes = []
	lengths = []
	i = 0
	print(os.path.isdir('Voting_Data'))
	for folder in os.listdir("Voting_Data"):
		nodes.Reset()
		if folder.startswith('legislators_' + session):
			print(folder)
			# nodes.Load(os.path.join("Voting_Data", folder))
			with open('Voting_Data/'+folder+'/legislators.csv', 'r') as infile:
				reader = csv.DictReader(infile)
				dataframes.append(list(reader))
				for data in dataframes[i]:
					data['yes_votes'] = list(map(int, data['yes_votes'][1:-1].split(',')))
					data['no_votes'] = list(map(int, data['no_votes'][1:-1].split(',')))
				i += 1

	nodes = [i for i in range(len(dataframes[0]))]
	print('Number of Nodes: ', len(nodes))
	g = graph.SimrankGraph(nodes)
	num_edges = 0;
	total_weight = 0;
	for pair in itertools.combinations(nodes, 2):
		weight = 0
		for i in range(2):
			# print(dataframes[i][pair[0]]['yes_votes'])
			# print(set.intersection(set(dataframes[i][pair[0]]['yes_votes']), set(dataframes[i][pair[1]]['yes_votes'])))
			weight += len(set.intersection(set(dataframes[i][pair[0]]['yes_votes']), set(dataframes[i][pair[1]]['yes_votes'])))
			# weight += len(set.intersection(dataframes[i][pair[0]]['no_votes'], dataframes[i][pair[1]]['no_votes']))
		g.SetEdgeById(pair[0], pair[1], weight, False)
		num_edges += 1
		total_weight += weight
		# print(weight)
	print('Number of Edges: ', num_edges)
	print('Average Edge Weight: ', total_weight/num_edges)
	g.Run()
