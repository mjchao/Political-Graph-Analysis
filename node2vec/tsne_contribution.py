import numpy as np
import matplotlib.pylab as plt
from sklearn.manifold import TSNE

X = np.empty([1])

print 'Reading in feature matrix file...'
# Read in node2vec into np.array
with open('unweighted_graph/contribution_node2vec_out_113.txt', 'r') as f:
  numNodes, numFeatures = map(int, (f.readline()[:-1]).split(' '))
  print 'Number of nodes: ' + str(numNodes)
  print 'Number of features: ' + str(numFeatures)
  X = np.empty([numNodes, numFeatures])
  for line in f:
    nodeValues = map(float, line[:-1].split(' '))
    X[int(nodeValues[0])] = nodeValues[1:numFeatures+1]

# TODO may want to run PCA before TSNE to reduce the feature dimension down to the suggested 50 features
print 'Modelling t-SNE...'
model = TSNE(n_components=2, random_state=0)
Y = model.fit_transform(X)
plt.scatter(Y[:,0], Y[:,1])
plt.show()