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

print 'Number of nodes: ' + str(len(nodes))
print 'Number of edges: ' + str(len(edges))

contribution_graph = graph.SparseGraph(list(nodes))
for edge in edges:
  contribution_graph.SetEdge(edge[0], edge[1], directed=True)

# Save graph adjacency list to file
contribution_graph.SaveAdjacencyList('node2vec/contribution_edges.txt', weight=False)
# Save node ID mapping
contribution_graph.SaveNodeMapping('node2vec/contribution_id_map.txt')
