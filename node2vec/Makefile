# NOTE: You first need to run gen_contrib_edges.py in the parent folder to get the 
# edge file and ID map file.

node2vec:
	# python node2vec-master/src/main.py --input contribution_edges.txt --output contribution_node2vec_out.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_105.txt --output contribution_node2vec_out_105.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_106.txt --output contribution_node2vec_out_106.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_107.txt --output contribution_node2vec_out_107.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_108.txt --output contribution_node2vec_out_108.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_109.txt --output contribution_node2vec_out_109.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_110.txt --output contribution_node2vec_out_110.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_111.txt --output contribution_node2vec_out_111.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_112.txt --output contribution_node2vec_out_112.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_113.txt --output contribution_node2vec_out_113.txt
	python node2vec-master/src/main.py --input contribution_edges_weight_114.txt --output contribution_node2vec_out_114.txt

nn:
	python near_neighbor.py