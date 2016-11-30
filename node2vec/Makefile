# You first need to run gen_contrib_edges.py in the parent folder to get the 
# edge file and ID map file.

node2vec:
	python node2vec-master/src/main.py --input contribution_edges.txt --output contribution_node2vec_out.txt

nn:
	python near_neighbor.py