#Collects data from govTrack.us and saves to panda files
#Saves a Legislator as {first_name(string), last_name(string), id(string), state(string), yes_votes(int[]), no_votes(int[])}
#Directories are labeled as session_year_vote e.g. 114_2014_3

import urllib2
import requests
import json
import sys
import csv
import nodes
import os

congressmen_template = {}

def get_congressmen():
	with open('legislators-current.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			congressmen_template[row['bioguide_id']] = {'first_name': row['first_name'], 
												'last_name': row['last_name'],
												'id': row['bioguide_id'],
												'state': row['state'],
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

def get_votes(year):
	year = 1986
	for session in range(100, 114):
		for j in range(2):
			congressmen = congressmen_template
			year += 1
			vote = 2
			url = "https://www.govtrack.us/data/congress/" + str(session) + "/votes/" + str(year) + "/h" + str(vote) +  "/data.json"
			response = requests.get(url)
			while response.status_code != 404:
				data = json.loads(response.text)
				# print(data['votes'])
				if 'No' in data['votes']:
					for c in data['votes']['No']:
						congressmen[c['id'].encode('utf8')]['no_votes'].append(vote)
				if 'Nay' in data['votes']:
					for c in data['votes']['Nay']:
						congressmen[c['id'].encode('utf8')]['no_votes'].append(vote)

				if 'Aye' in data['votes']:
					for c in data['votes']['Aye']:
						congressmen[c['id'].encode('utf8')]['yes_votes'].append(vote)
				if 'Yea' in data['votes']:
					for c in data['votes']['Yea']:
						congressmen[c['id'].encode('utf8')]['yes_votes'].append(vote)
				
				vote += 1
				url = "https://www.govtrack.us/data/congress/" + str(session) + "/votes/" + str(year) + "/h" + str(vote) +  "/data.json"
				response = requests.get(url)

			for key, c in congressmen.iteritems():
				if len(c['yes_votes']) != 0 or len(c['no_votes']) != 0:
					nodes.AddLegislator(c)

			directory = 'legislators_' + str(session) + '_' + str(year) + '_' + str(vote)
			if not os.path.exists(directory):
				os.makedirs(directory)
			print("Saving to directory " + directory + '...')
			nodes.Save(directory)

if __name__ == "__main__":
	get_congressmen()
	get_votes(sys.argv[1])