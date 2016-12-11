import nodes
import graph
import os
import sys
import itertools
import csv

if __name__ == "__main__":
	print(sys.argv[1])
	session = sys.argv[1]
	use_saved = False
	if len(sys.argv) == 3:
		use_saved = sys.argv[2]

	dataframe = []
	lengths = []
	i = 0
	for folder in os.listdir("Voting_Data"):
		nodes.Reset()
		if folder.startswith('legislators_' + str(session)):
			# nodes.Load(os.path.join("Voting_Data", folder))
			print(folder)
			with open('Voting_Data/'+folder+'/legislators.csv', 'r') as infile:
				print 'here'
				reader = csv.DictReader(infile)
				dataframe= list(reader)
				for data in dataframe:
					if(data['yes_votes'] != '[]'):
						data['yes_votes'] = list(map(int, data['yes_votes'][1:-1].split(',')))
					if(data['no_votes'] != '[]'):
						data['no_votes'] = list(map(int, data['no_votes'][1:-1].split(',')))
				i += 1

	nodes = [i for i in range(len(dataframe))]

	print dataframe

	vote_ids = {}
	next_id = len(dataframe)
	with open('voting_edgelists/' + str(session) + '_bipartite_edgelist.txt', 'w') as outfile:
		for node in nodes:
			for vote in dataframe[node]['yes_votes']:
				if vote in vote_ids:
					outfile.write(str(node) + ',' + str(vote_ids[vote]) + '\n')
				else:
					outfile.write(str(node) + ',' + str(next_id) + '\n')
					vote_ids[vote] = next_id
					next_id += 1

	with open('voting_edgelists/' + str(session) + 'congressmen_edgelist_key.txt', 'w') as outfile:
		for i, data in enumerate(dataframe):
			outfile.write(str(i) + ',' + 
							data['first_name'] + ',' + 
							data['last_name'] + ',' + 
							data['party'] + ',' + 
							data['state'] + ',' +
							data['gender'] + ',' +
							data['opensecrets_id'] + '\n')
	
	with open('voting_edgelists/' + str(session) + 'bills_edgelist_key.txt', 'w') as outfile:
		for key, val in vote_ids.iteritems():
			outfile.write(str(val) + ',' + str(key) + '\n')