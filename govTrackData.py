#Collects data from govTrack.us and saves to panda files
#Saves a Legislator as {first_name(string), last_name(string), id(string), state(string), yes_votes(int[]), no_votes(int[])}
#Directories are labeled as session_#vote e.g. 113_565

import urllib2
import requests
import json
import sys
import csv
import nodes
import os
import copy

congressmen_template = {}

def get_congressmen():
	with open('legislators-current.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			congressmen_template[row['bioguide_id']] = {'first_name': row['first_name'], 
												'last_name': row['last_name'],
												'id': row['bioguide_id'],
												'state': row['state'],
												'party': row['party'],
												'yes_votes': [],
												'no_votes': []}
	with open('legislators-historic.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			congressmen_template[row['bioguide_id']] = {'first_name': row['first_name'], 
												'last_name': row['last_name'],
												'state': row['state'],
												'yes_votes': [],
												'no_votes': []}
	return

def get_votes():
	year = 1988
	for session in range(101, 114):
		congressmen = copy.deepcopy(congressmen_template)
		for j in range(2):
			year += 1
			vote = 2
			path = "data/" + str(session) + "/votes/" + str(year)
			for folder in os.listdir(path):
				if folder.startswith('h'):
					with open(path+'/'+folder+'/data.json') as infile:
						data = json.load(infile)
						# print(data['votes'])
						if 'No' in data['votes']:
							for c in data['votes']['No']:
								congressmen[c['id'].encode('utf8')]['no_votes'].append(int(str(year) + str(vote)))
						if 'Nay' in data['votes']:
							for c in data['votes']['Nay']:
								congressmen[c['id'].encode('utf8')]['no_votes'].append(int(str(year) + str(vote)))

						if 'Aye' in data['votes']:
							for c in data['votes']['Aye']:
								congressmen[c['id'].encode('utf8')]['yes_votes'].append(int(str(year) + str(vote)))
						if 'Yea' in data['votes']:
							for c in data['votes']['Yea']:
								congressmen[c['id'].encode('utf8')]['yes_votes'].append(int(str(year) + str(vote)))
						
						vote += 1

		num_congressmen = 0
		for key, c in congressmen.iteritems():
			if len(c['yes_votes']) != 0 or len(c['no_votes']) != 0:
				nodes.AddLegislator(c)
				num_congressmen += 1

		print(num_congressmen)


		directory = 'Voting_Data/legislators_' + str(session) + '_' + str(vote)
		if not os.path.exists(directory):
			os.makedirs(directory)
		print("Saving to directory " + directory + '...')
		nodes.Save(directory)
		print('Reseting nodes')
		nodes.Reset()

if __name__ == "__main__":
	get_congressmen()
	get_votes()