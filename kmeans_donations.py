import graph
import kmeans

nameToID = {}

# Tie politician name and ID
with open('contributions.csv', 'r') as f:
  for line in f:
    line = line[:-1]
    line = line.split(',')
    nameToID[line[0]] = line[1]

IDToParty = {}

# Tie politician IDs to party affiliation
with open('legislators-historic.csv', 'r') as f:
  for line in f:
    line = line[:-1]
    line = line.lower()
    line = line.split(',')
    politicianID = line[20]
    politicianParty = line[7]
    # print politicianID, politicianParty
    IDToParty[politicianID] = politicianParty

nodes = set()
edges = []

# Get similarity edges
with open('simrank_contributions_results_1998.csv','r') as f:
  for line in f:
    line = line[:-1]
    line = line.split(',')
    # Check it's a politician
    if line[3] == 'Companies':
      continue
    nodes.add(line[0])
    nodes.add(line[1])
    edges.append(line[0:3])

nodes_list = []
for node in nodes:
  nodes_list.append(node)

contribution_graph = graph.SimrankGraph(nodes_list)

for edge in edges:
  contribution_graph.SetEdge(edge[0],edge[1],weight=float(edge[2]),directed=False)

# print contribution_graph.getAdjacencyMatrix()
# print contribution_graph.getAdjacencyMatrix().sum().sum()

kmeansObj = kmeans.KMeans(contribution_graph.getAdjacencyMatrix())
# Set number of clusters
kmeansObj.Run(num_clusters=2)

results = []

with open('kmeans_donations_out.txt', 'w') as f:
  for clusterID, cluster in enumerate(kmeansObj.clusters):
    results.append({})
    for nodeID in cluster:
      if nameToID[nodes_list[nodeID]] in IDToParty:
        partyStr = IDToParty[nameToID[nodes_list[nodeID]]]
        if partyStr not in results[clusterID]:
          results[clusterID][partyStr] = 1
        else:
          results[clusterID][partyStr] = results[clusterID][partyStr] + 1
        f.write(str(clusterID) + ', ' + nodes_list[nodeID] + ', ' + partyStr + '\n')
      # f.write(str(clusterID) + ', ' + nodes_list[nodeID] + '\n')

# print results
for result in results:
  print result

