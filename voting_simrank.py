import nodes
import graph
import os
import sys
import itertools
import pandas as pd
import copy
import csv
import kmeans

if __name__ == "__main__":
	session = sys.argv[1]
	dataframe = []
	lengths = []
	i = 0
	for folder in os.listdir("Voting_Data"):
		nodes.Reset()
		if folder.startswith('legislators_' + session):
			# nodes.Load(os.path.join("Voting_Data", folder))
			with open('Voting_Data/'+folder+'/legislators.csv', 'r') as infile:
				reader = csv.DictReader(infile)
				dataframe= list(reader)
				for data in dataframe:
					data['yes_votes'] = list(map(int, data['yes_votes'][1:-1].split(',')))
					data['no_votes'] = list(map(int, data['no_votes'][1:-1].split(',')))
				i += 1

	nodes = [i for i in range(len(dataframe))]
	
	g = graph.SimrankGraph(nodes)
	num_edges = 0;
	total_weight = 0;
	for pair in itertools.combinations(nodes, 2):
		weight = len(set.intersection(set(dataframe[pair[0]]['yes_votes']), set(dataframe[pair[1]]['yes_votes'])))
		weight += len(set.intersection(set(dataframe[pair[0]]['no_votes']), set(dataframe[pair[1]]['no_votes'])))
		if(weight != 0):
			g._SetEdgeById(pair[0], pair[1], 1.0/weight, False)
			total_weight += 1.0/weight
		else:
			g._SetEdgeById(pair[0], pair[1], 1, False)
		num_edges += 1

	g.Run(r=1.0/300, C=.99, iterations=1)
	g.Save(argv[1] + '_similarity.csv')

	#Initialie K-Means
	km2 = KMeans(g._similarity, num_clusters=2)
	km3 = KMeans(g._similarity, num_clusters=3)
	km4 = KMeans(g._similarity, num_clusters=4)

	#Run K-Means
	km2.Run()
	km3.Run()
	km4.Run()

	print(km2.clusters)
	print(km3.clusters)
	print(km4.clusters)
	#TEST
	print('Number of Nodes: ', len(nodes))
	print('Number of Edges: ', num_edges)
	print('Average Edge Weight: ', total_weight/num_edges)

	dem_indexes = []
	rep_indexes = []
	for i in range(len(nodes)):
		if(dataframe[i]['party'] == 'Democrat'):
			dem_indexes.append(i)
		elif(dataframe[i]['party'] == 'Republican'):
			rep_indexes.append(i)

	print('Number of Democrats: ', len(dem_indexes))
	print('Number of Republicans: ', len(rep_indexes))
	dem_total = 0
	rep_total = 0
	between_total = 0
	all_score = 0

	for dem_index in dem_indexes:
		for rep_index in rep_indexes:
			between_total += g.Similarity(dem_index, rep_index)

	total_nonzero = 0.0
	for pair in itertools.combinations(nodes, 2):
		sim_score = g.Similarity(pair[0], pair[1])
		all_score += sim_score
		if(sim_score):
			total_nonzero += 1.0

	dem_range = [i for i in range(len(dem_indexes))]
	dem_total_pairs = 0.0
	for pair in itertools.combinations(dem_range, 2):
		dem_total += g.Similarity(dem_indexes[pair[0]], dem_indexes[pair[1]])
		dem_total_pairs += 1.0

	rep_total_pairs = 0.0
	rep_range = [i for i in range(len(rep_indexes))]
	for pair in itertools.combinations(rep_range, 2):
		rep_total += g.Similarity(rep_indexes[pair[0]], rep_indexes[pair[1]])
		rep_total_pairs += 1.0

	print(g._adj)
	print('Total similarity score sum: ', all_score)
	print('Total nonzero similarity scores: ', total_nonzero)
	print('Democrat average score: ', dem_total/dem_total_pairs)
	print('Republican average score: ', rep_total/rep_total_pairs)
	print('Between average score: ', between_total/(len(rep_indexes) * len(dem_indexes)))





