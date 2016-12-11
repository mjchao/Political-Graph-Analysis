# NOTE: You first need to run gen_contrib_edges.py in the parent folder to get the 
# edge file and ID map file.

contrib:
	# python node2vec-master/src/main.py --weighted --input contribution_edges.txt --output contribution_node2vec_out.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_105.txt --output contribution_node2vec_out_105.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_106.txt --output contribution_node2vec_out_106.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_107.txt --output contribution_node2vec_out_107.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_108.txt --output contribution_node2vec_out_108.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_109.txt --output contribution_node2vec_out_109.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_110.txt --output contribution_node2vec_out_110.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_111.txt --output contribution_node2vec_out_111.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_112.txt --output contribution_node2vec_out_112.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_113.txt --output contribution_node2vec_out_113.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_114.txt --output contribution_node2vec_out_114.txt

contrib_weight:
	# python node2vec-master/src/main.py --weighted --input contribution_edges.txt --output contribution_node2vec_out.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_105.txt --output contribution_node2vec_out_105.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_106.txt --output contribution_node2vec_out_106.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_107.txt --output contribution_node2vec_out_107.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_108.txt --output contribution_node2vec_out_108.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_109.txt --output contribution_node2vec_out_109.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_110.txt --output contribution_node2vec_out_110.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_111.txt --output contribution_node2vec_out_111.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_112.txt --output contribution_node2vec_out_112.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_113.txt --output contribution_node2vec_out_113.txt
	python node2vec-master/src/main.py --weighted --input contribution_edges_weight_114.txt --output contribution_node2vec_out_114.txt

tripartite:
	python node2vec-master/src/main.py --input tripartite_edgelists/105_tripartite_edgelist.txt --output tripartite_node2vec_out_105.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/106_tripartite_edgelist.txt --output tripartite_node2vec_out_106.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/107_tripartite_edgelist.txt --output tripartite_node2vec_out_107.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/108_tripartite_edgelist.txt --output tripartite_node2vec_out_108.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/109_tripartite_edgelist.txt --output tripartite_node2vec_out_109.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/110_tripartite_edgelist.txt --output tripartite_node2vec_out_110.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/111_tripartite_edgelist.txt --output tripartite_node2vec_out_111.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/112_tripartite_edgelist.txt --output tripartite_node2vec_out_112.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/113_tripartite_edgelist.txt --output tripartite_node2vec_out_113.txt
	python node2vec-master/src/main.py --input tripartite_edgelists/114_tripartite_edgelist.txt --output tripartite_node2vec_out_114.txt

voting:
	python node2vec-master/src/main.py --input voting_edgelists/101_bipartite_edgelist.txt --output voting_node2vec_out_101.txt
	python node2vec-master/src/main.py --input voting_edgelists/102_bipartite_edgelist.txt --output voting_node2vec_out_102.txt
	python node2vec-master/src/main.py --input voting_edgelists/103_bipartite_edgelist.txt --output voting_node2vec_out_103.txt
	python node2vec-master/src/main.py --input voting_edgelists/104_bipartite_edgelist.txt --output voting_node2vec_out_104.txt
	python node2vec-master/src/main.py --input voting_edgelists/105_bipartite_edgelist.txt --output voting_node2vec_out_105.txt
	python node2vec-master/src/main.py --input voting_edgelists/106_bipartite_edgelist.txt --output voting_node2vec_out_106.txt
	python node2vec-master/src/main.py --input voting_edgelists/107_bipartite_edgelist.txt --output voting_node2vec_out_107.txt
	python node2vec-master/src/main.py --input voting_edgelists/108_bipartite_edgelist.txt --output voting_node2vec_out_108.txt
	python node2vec-master/src/main.py --input voting_edgelists/109_bipartite_edgelist.txt --output voting_node2vec_out_109.txt
	python node2vec-master/src/main.py --input voting_edgelists/110_bipartite_edgelist.txt --output voting_node2vec_out_110.txt
	python node2vec-master/src/main.py --input voting_edgelists/111_bipartite_edgelist.txt --output voting_node2vec_out_111.txt
	python node2vec-master/src/main.py --input voting_edgelists/112_bipartite_edgelist.txt --output voting_node2vec_out_112.txt
	python node2vec-master/src/main.py --input voting_edgelists/113_bipartite_edgelist.txt --output voting_node2vec_out_113.txt

nn:
	# python near_neighbor.py
	python near_neighbor.py -f unweighted_graph/contribution_node2vec_out_105.txt -g unweighted_graph/contribution_id_map_105.txt -i contribution_node2vec_nn_105.txt -n contribution_node2vec_nn_names_105.txt

tsne:
	python tsne_contribution.py -f unwighted_graph/contribution_node2vec_out_105.txt -g unwighted_graph/contribution_id_map_105.txt
