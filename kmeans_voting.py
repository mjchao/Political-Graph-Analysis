"""Usage
-s --start: starting session, inclusive (105 by default)
-e --end: ending session, exclusive (115 by default)
-f --vec_file: file pattern for node vectors. E.g. data/contribution_node2vec_out_%d.txt
-g --gt_file: file pattern for ground truth. E.g. data/contribution_id_map_%d.txt

Example to run clustering + entropy evaluation:

python node2vec_cluster.py -f data/contribution_node2vec_out_%d.txt -g data/contribution_id_map_%d.txt
"""

import graph
import kmeans
import sys

""" Run the kmeans algorithm on the donations graph network.
"""
def kmeansVoting():
  sessions = [ 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113 ]

  for session in sessions:
    print 'Processing session %d' % session
    # Get similarity edges
    IDToData = {}
    with open('voting_edgelists/%dcongressmen_edgelist_key.txt' % session, 'r') as f:
      for line in f:
        line = line.strip('\n').split(',')
        # (first name, last name, party)
        IDToData[int(line[0])] = (line[1], line[2], line[3])

    nodes = set()
    edges = []
    with open('voting_edgelists/%d_edgelist.txt' % session, 'r') as f:
      for line in f:
        line = line[:-1].split(' ')
        nodes.add(int(line[1]))
        nodes.add(int(line[2]))
        edges.append(line[0:3])

    contribution_graph = graph.SimrankGraph(list(nodes))
    for edge in edges:
      contribution_graph.SetEdge(int(edge[1]),int(edge[2]),weight=float(edge[0]),
        directed=False)

    kmeansObj = kmeans.KMeans(contribution_graph.getAdjacencyMatrix())
    print 'Running KMeans...'
    # Set number of clusters
    kmeansObj.Run(num_clusters=2,iterations=2000)

    print 'Printing results...'
    results = []
    with open('voting_edgelists/kmeans_votings_%d_out.txt' % session, 'w') as f:
      for clusterID, cluster in enumerate(kmeansObj.clusters):
        results.append({})
        for nodeID in cluster:
          partyStr = IDToData[nodeID][2]
          if partyStr not in results[clusterID]:
            results[clusterID][partyStr] = 1
          else:
            results[clusterID][partyStr] = results[clusterID][partyStr] + 1
          f.write(str(clusterID) + ',' + IDToData[nodeID][0] + ','
                  + IDToData[nodeID][1] + ',' + partyStr + '\n')

    # print results
    for result in results:
      print result


def main():
  kmeansVoting()

if __name__ == "__main__":
  main()
  sys.exit(0)
