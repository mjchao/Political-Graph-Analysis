""" Usage

Example:

python tsne_contribution.py -f unwighted_graph/contribution_node2vec_out_105.txt -g unwighted_graph/contribution_id_map_105.txt
"""

import numpy as np
import matplotlib.pylab as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from optparse import OptionParser
import sys

def runTSNE(vec_file, ground_truth_file):
  X = np.empty([1])

  print 'Reading in feature matrix file...'
  # Read in node2vec into np.array
  with open(vec_file, 'r') as f:
    numNodes, numFeatures = map(int, (f.readline()[:-1]).split(' '))
    print 'Number of nodes: ' + str(numNodes)
    print 'Number of features: ' + str(numFeatures)
    X = np.empty([numNodes, numFeatures])
    for line in f:
      nodeValues = map(float, line[:-1].split(' '))
      X[int(nodeValues[0])] = nodeValues[1:numFeatures+1]

  # TODO may want to run PCA before TSNE to reduce the feature dimension down to the suggested 50 features
  print 'Reducing node2vec down to 50 feature PCA vector'
  model = PCA(n_components=50, random_state=None)
  pca = model.fit_transform(X)
  # Y = model.fit_transform(X)
  print 'Modelling t-SNE...'
  model = TSNE(n_components=2, random_state=None)
  Y = model.fit_transform(pca)

  x_coords = Y[:, 0]
  y_coords = Y[:, 1]
  is_democrat = []
  is_republican = []
  with open(ground_truth_file, 'r') as f:
    for line in f.readlines():
      data = line.rstrip('\n').split(',')
      if len(data) > 3:
        party = data[3]
        if party == 'democrat':
          is_democrat.append(True)
          is_republican.append(False)
        elif party == 'republican':
          is_republican.append(True)
          is_democrat.append(False)
        else:
          is_republican.append(False)
          is_democrat.append(False)
      else:
        is_republican.append(False)
        is_democrat.append(False)
      
  is_republican = np.array(is_republican)
  is_democrat = np.array(is_democrat)

  republican_x = x_coords[is_republican]
  republican_y = y_coords[is_republican]
  democrat_x = x_coords[is_democrat]
  democrat_y = y_coords[is_democrat]

  is_company = np.logical_and(np.logical_not(is_republican), np.logical_not(is_democrat))
  company_x = x_coords[is_company]
  company_y = y_coords[is_company]

  plt.scatter(company_x, company_y, color='g')
  plt.scatter(republican_x, republican_y, color='r', marker='^')
  plt.scatter(democrat_x, democrat_y, color='b', marker='.')
  plt.title('TSNE on Democrats, Republicans, and Companies')
  plt.savefig('pca_tsne_weighted_contrib_%d.png')
  plt.show()

def main():
  parser = OptionParser()
  parser.add_option('-f', '--file', action='store', dest='vec_file',
                        help='node vector file.')
  parser.add_option('-g', '--ground_truth', action='store',
                      dest='gt_file',
                      help='file containing the ground truth.')

  options, args = parser.parse_args()
  print 'Processing Congress'
  runTSNE(options.vec_file, options.gt_file)
  print

if __name__ == '__main__':
  main()
  sys.exit(0)
