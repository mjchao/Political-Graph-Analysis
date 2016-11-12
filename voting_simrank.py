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
			# nodes.Load(os.path.join("Voting_Data", folder))
			reader = csv.DictReader('Voting_Data/'+folder+'/legislators.csv')
			dataframes.append(list(reader))

	nodes = copy.deepcopy(dataframes[0])
	for node in nodes:
		node.pop('yes_votes', None)
		node.pop('no_votes', None)

	g = graph.SimrankGraph
	indexes = [i for i in range(len(nodes))]
	for pair in itertools.combinations(indexes, 2):
		weight = 0
		for i in range(2):
			if 'yes_votes' in dataframes[i][pair[0]] and 'yes_votes' in dataframes[i][pair[1]]:
				weight += len(set.intersection(dataframes[i][pair[0]]['yes_votes'], dataframes[i][pair[1]]['yes_votes']))
			if 'no_votes' in dataframes[i][pair[0]] and 'no_votes' in dataframes[i][pair[1]]:
				weight += len(set.intersection(dataframes[i][pair[0]]['no_votes'], dataframes[i][pair[1]]['no_votes']))
		print(pair)
		g.SetEdgeById(pair[0], pair[1], weight, False)

	g.Run()
