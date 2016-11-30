from sets import Set
import graph

# Choose the congress session
# years = Set([1998])
years = Set([2014])
# years = Set([1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016])
nodes = Set()
edges = []
with open('contributions.csv','r') as f:
  for line in f:
    line = line.split(',')
    # TODO (cvwang): this needs to be fixed
    if int(line[2]) in years:
      nodes.add(line[0])
      nodes.add(line[4])
      edges.append([line[0],line[4]])

print len(nodes)
print len(edges)

contribution_graph = graph.SimrankGraph(list(nodes))
for edge in edges:
  contribution_graph.SetEdge(edge[0], edge[1], directed=False)

contribution_graph.Run(r=1)

# TODO (cvwang): change this to a file print
for edge in edges:
	print(contribution_graph.Similarity(edge[0],edge[1]))
