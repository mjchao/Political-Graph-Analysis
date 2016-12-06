from sklearn.neighbors import NearestNeighbors
import numpy as np

distances = indices = []


# Read in node2vec into np.array
with open('contribution_node2vec_out.txt', 'r') as f:
  numNodes, numFeatures = map(int, (f.readline()[:-1]).split(' '))
  print 'Number of nodes: ' + str(numNodes)
  print 'Number of features: ' + str(numFeatures)
  X = np.empty([numNodes, numFeatures])
  for line in f:
    nodeValues = map(float, line[:-1].split(' '))
    X[int(nodeValues[0])] = nodeValues[1:numFeatures+1]
  print X
  print 'Modelling nearest neighbors...'
  nbrs = NearestNeighbors().fit(X)
  print 'Finding nearest neighbors...'
  distances, indices = nbrs.kneighbors(X)
  print 'Nearest neighbors calculated'

print indices

# Print out NN IDs
print 'Outputting nearest neighbors ID to file'
with open('contribution_node2vec_nn.txt', 'w') as f:
  for nn in indices:
    f.write(' '.join(map(str, nn)) + '\n')

# Read in ID mapping
id_to_name = []
with open('contribution_id_map.txt', 'r') as f:
  for line in f:
    id_to_name.append(line[:-1].split(',')[1])

# Print out NN names
print 'Outputting nearest neighbors name to file'
with open('contribution_node2vec_nn_names.txt', 'w') as f:
  for nn in indices:
    f.write(','.join([id_to_name[i] for i in nn]) + '\n')

# TODO (cvwang): Do a NN just on politician vectors gotten from node2vec (but calculated with company connections as well, obviously).