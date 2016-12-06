from sets import Set
import graph

""" Get contribution graph edges and node attributes
"""

# nameToID = {}

# # Tie politician name and ID
# with open('contributions.csv', 'r') as f:
#   for line in f:
#     line = line[:-1]
#     line = line.split(',')
#     nameToID[line[0]] = line[1]

IDToParty = {}

# Tie politician IDs to party affiliation
with open('legislators.csv', 'r') as f:
  for line in f:
    line = line[:-1]
    # line = line.lower()
    line = line.split(',')
    politicianID = line[20]
    politicianParty = line[7].lower()
    IDToParty[politicianID] = politicianParty

# Choose the congress session
# years = Set([1998])
# years = Set([2014])
# years = Set([1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2016])
years = Set([1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016])

yearToSession = {
  1998 : 105,
  2000 : 106,
  2002 : 107,
  2004 : 108,
  2006 : 109,
  2008 : 110,
  2010 : 111,
  2012 : 112,
  2014 : 113,
  2016 : 114
}

for year in years:
  nodes = Set()
  politicians = Set()
  edges = []
  with open('contributions.csv','r') as f:
    for line in f:
      line = line.split(',')
      if int(line[2]) == year:
        line[1] = line[1].upper()
        nodeName = line[0] + ',' + line[1]
        if line[1] in IDToParty:
          nodeName = nodeName + ',' + IDToParty[line[1]]


        politicians.add(nodeName)
        nodes.add(nodeName)
        nodes.add(line[4])
        edges.append([nodeName,line[4]])

  print 'Number of nodes: ' + str(len(nodes))
  print 'Number of edges: ' + str(len(edges))

  contribution_graph = graph.SparseGraph(list(nodes))
  for edge in edges:
    contribution_graph.SetEdge(edge[0], edge[1], directed=True)

  # # Save graph adjacency list to file
  # contribution_graph.SaveAdjacencyList('node2vec/contribution_edges_%d.txt' % yearToSession[year], weight=False)
  # # Save node ID mapping
  # contribution_graph.SaveNodeMapping('node2vec/contribution_id_map_%d.txt' % yearToSession[year])

  # Print 
  # Save graph adjacency list to file
  contribution_graph.SaveAdjacencyList('node2vec/contribution_edges_weight_%d.txt' % yearToSession[year], weight=True)
  # Save node ID mapping
  contribution_graph.SaveNodeMapping('node2vec/contribution_id_map_%d.txt' % yearToSession[year])
