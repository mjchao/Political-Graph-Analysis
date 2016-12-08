# Generates the full tripartite graphs for sessions 105-114
#
# Assumes the voting bipartite edgelists are in the directory 'voting_edgelists'
# and that the contribution bipartite edgelists are in the directory 'unweighted_contribution_edgelists',
# both in the same diretory as this file

import csv
import itertools

for session in range(105,114):
	congressmen = {} #open secrets id to both voting and donation data ids
	congressmen_old_voting_to_opensecrets = {}
	congressmen_old_contribution_to_opensecrets = {}
	congressmen_new_to_opensecrets = {}

	bill_id_map = {} # old voting data id to new tripartite graph id
	bill_to_number = {}

	company_id_map = {} #old id to new id
	company_to_name = {}

	new_edges = []


	next_id = 0 #new id
	with open('voting_edgelists/' + str(session) + 'congressmen_edgelist_key.txt', 'r') as infile:
		fieldnames = ['id', 'first_name', 'last_name', 'party', 'state', 'gender', 'opensecrets_id']
		reader = csv.DictReader(infile, fieldnames=fieldnames)
		for con in list(reader):
			congressmen[con['opensecrets_id']] = {'voting_id':con['id'], 
													'new_id':next_id,
													'first_name':con['id'],
													'last_name':con['last_name'],
													'party': con['party'],
													'state':con['state'],
													'gender':con['gender']}
			congressmen_old_voting_to_opensecrets[con['id']] = con['opensecrets_id']
			next_id += 1

	with open('voting_edgelists/' + str(session) + 'bills_edgelist_key.txt', 'r') as infile:
		fieldnames = ['id', 'bill_id']
		for bill in infile:
			old_id, number = bill.split(' ')
			bill_id_map[old_id] = str(next_id)
			bill_to_number[str(next_id)] = number
			next_id += 1

	with open('unweighted_contribution_edgelists/contribution_id_map/contribution_id_map_' + str(session) + '.txt', 'r') as infile:
		fieldnames = ['id', 'name', 'opensecrets_id', 'party']
		reader = csv.DictReader(infile, fieldnames=fieldnames)
		for entity in list(reader):
			if entity['opensecrets_id'] != None:
				if not entity['opensecrets_id'] in congressmen:
					party = con['party']
					if not party:
						party = ''
					congressmen[entity['opensecrets_id']] = {'contribution_id': entity['id'], 
															'new_id':next_id,
															'first_name': entity['name'].split()[0],
															'last_name': entity['name'].split()[1],
															'party': party,
															'state': '',
															'gender': ''}
					next_id += 1
				else:
					congressmen[entity['opensecrets_id']]['contribution_id'] = entity['id']
				congressmen_old_contribution_to_opensecrets[entity['id']] = entity['opensecrets_id']
			else:
				company_id_map[entity['id']] = str(next_id)
				company_to_name[str(next_id)] = entity['name']
				next_id += 1

	with open('voting_edgelists/' + str(session) + '_bipartite_edgelist.txt', 'r') as voting_edgelist, \
	 open('unweighted_contribution_edgelists/contribution_edges/contribution_edges_' + str(session) + '.txt', 'r') as contribution_edgelist, \
	 open('tripartite_edgelists/' + str(session) + '_tripartite_edgelist.txt', 'w') as outfile:
		for line in voting_edgelist:
			edge = line.split(' ')

			opensecrets_id = congressmen_old_voting_to_opensecrets[edge[0]]
			new_c_id = congressmen[opensecrets_id]['new_id']
			new_v_id = bill_id_map[edge[1][:-1]]

			outfile.write(str(new_c_id) + ' ' + str(new_v_id) + '\n')

		for line in contribution_edgelist:
			edge = line.split(' ')

			opensecrets_id = congressmen_old_contribution_to_opensecrets[edge[0]]
			new_c_id = congressmen[opensecrets_id]['new_id']
			new_v_id = company_id_map[edge[1][:-1]]

			outfile.write(str(new_c_id) + ' ' + str(new_v_id) + '\n')

	with open('tripartite_edgelists/' + str(session) + '_key.txt', 'w') as outfile:
		for opensecrets_id, con in congressmen.iteritems():
			outfile.write(str(con['new_id']) + ',' +
							con['first_name'] + ',' +
							con['last_name'] + ',' +
							con['party'] + ',' +
							con['state'] + ',' +
							con['gender'] + '\n')

		for old_id, new_id in company_id_map.iteritems():
			outfile.write(str(new_id) + ',' + company_to_name[new_id] + '\n')

		for old_id, new_id in bill_id_map.iteritems():
			outfile.write(str(new_id) + ',' + bill_to_number[new_id])
