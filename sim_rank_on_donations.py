import graph

nodes = {}
edges = []
with open('contributions.csv','r') as f:
  for line in f:
  	line = line.split(',')
  	nodes[line[0]] = True
  	nodes[line[3]] = True
  	edges.append([line[0],line[3]])

nodes_list = []
for key, value in nodes.iteritems():
	nodes_list.append(key)

contribution_graph = graph.SimrankGraph(nodes_list)
for edge in edges:
	contribution_graph.SetEdge(edge[0],edge[1],directed=False)

# Save adjacency matrix to file
# contribution_graph.SaveAdjacencyList('contribution_edges.txt')

contribution_graph.Run(r=1)

# for edge in edges:
# 	print(contribution_graph.Similarity(edge[0],edge[1]))
