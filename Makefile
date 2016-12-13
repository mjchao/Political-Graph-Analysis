# This is root Makefile


# Simrank Commands #############################################################

# Run kmeans on contribution simrank data
kmeans_simrank_contrib:
	python kmeans_contrib.py

# Run kmeans on voting simrank data
kmeans_simrank_voting:
	python kmeans_voting.py

################################################################################


# Node2Vec Commands ############################################################

# Scraping contribution data
scrape_contrib: 
	python scrape.py

# Generate contribution edgelists
# TODO (cvwang): Change make format to require files like below?
# gen_contrib_edges: gen_contrib_edges.py
gen_contrib_edges:
	python gen_contrib_edges.py

gen_contrib_edges_weight:
	python gen_contrib_edges.py --weight

# Generate node2vec feature vectors for contribution edge and ID mapping files
n2v_contrib:
	make -C node2vec contrib

# Generate node2vec feature vectors for contribution weighted edge and ID mapping files
n2v_contrib_weight:
	make -C node2vec contrib_weight

# Generate node2vec feature vectors for voting edge and ID mapping files
n2v_voting:
	make -C node2vec voting

# Run nearest neighbors on node2vec contribution data
# TODO (cvwang): This file will need to be generalized later
nn_n2v_contrib:
	make -C node2vec nn

tsne:
	make -C node2vec tsne	

find_outliers_pca:
	python pca_outliers.py	

simrank_opensecrets:
	python sim_rank_on_donations.py

#Collect and process govtrack data
govTrackData:
	python govTrackData.py

#Run simrank and knn on voting data
#Requires govTrackData
voting_simrank: govTrackData
	bash run_simrank.sh
	
#Create voting edgelists and keys
generate_voting_graphs: govTrackData
	bash generate_all_voting_graphs.sh

################################################################################
