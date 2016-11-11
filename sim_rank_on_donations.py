import graph

nodes = {}
edges = []
f = open("contributions.csv",'r')
for line in f:
	line = line.split(",")
	nodes[line[0]] = True
	nodes[line[3]] = True
	edges.append([line[0],line[3]])

nodes_list = []
for key, value in nodes.iteritems():
	nodes_list.append(key)

contribution_graph = graph.SimrankGraph(nodes_list)
for edge in edges:
	contribution_graph.SetEdge(edge[0],edge[1],directed=False)

contribution_graph.Run()

for edge in edges:
	print(contribution_graph.Similarity(edge[0],edge[1]))
