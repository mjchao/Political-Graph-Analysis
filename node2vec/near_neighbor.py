""" Usage

Example:

python near_neighbor.py -f unweighted_graph/contribution_node2vec_out_105.txt -g unweighted_graph/contribution_id_map_105.txt -i contribution_node2vec_nn_105.txt -n contribution_node2vec_nn_names_105.txt
"""

from sklearn.neighbors import NearestNeighbors
import numpy as np
from optparse import OptionParser
import sys

def genNN(inFeatureFile, inIDMapFile, outNNIDFile, outNNNameFile):
  distances = indices = []
  # Read in node2vec into np.array
  with open(inFeatureFile, 'r') as f:
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
  with open(outNNIDFile, 'w') as f:
    for nn in indices:
      f.write(' '.join(map(str, nn)) + '\n')

  # Read in ID mapping
  id_to_name = []
  with open(inIDMapFile, 'r') as f:
    for line in f:
      id_to_name.append(line[:-1].split(',')[1])

  # Print out NN names
  print 'Outputting nearest neighbors name to file'
  with open(outNNNameFile, 'w') as f:
    for nn in indices:
      f.write(','.join([id_to_name[i] for i in nn]) + '\n')

# TODO (cvwang): Do a NN just on politician vectors gotten from node2vec (but calculated with company connections as well, obviously).

def main():
  parser = OptionParser()
  parser.add_option('-f', '--features', action='store', dest='feature_file',
                        help='input node feature vector file.')
  parser.add_option('-g', '--id_map', action='store',
                      dest='id_map_file',
                      help='input file containing the node id to name mapping.')
  parser.add_option('-i', '--nn_id', action='store',
                      dest='nn_id_file',
                      help='output file nearest neighbor IDs.')
  parser.add_option('-n', '--nn_name', action='store',
                      dest='nn_name_file',
                      help='output file nearest neighbor names.')

  options, args = parser.parse_args()
  genNN(options.feature_file, options.id_map_file, options.nn_id_file, options.nn_name_file)

if __name__ == '__main__':
  main()
  sys.exit(0)
