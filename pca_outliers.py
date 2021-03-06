import numpy as np
import matplotlib.pylab as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

X = np.empty([1])

print 'Reading in feature matrix file...'
# Read in node2vec into np.array
with open('contribution_node2vec_out_113.txt', 'r') as f:
  numNodes, numFeatures = map(int, (f.readline()[:-1]).split(' '))
  print 'Number of nodes: ' + str(numNodes)
  print 'Number of features: ' + str(numFeatures)
  X = np.empty([numNodes, numFeatures])
  for line in f:
    nodeValues = map(float, line[:-1].split(' '))
    X[int(nodeValues[0])] = nodeValues[1:numFeatures+1]

# TODO may want to run PCA before TSNE to reduce the feature dimension down to the suggested 50 features
print 'Modelling t-SNE...'
model = PCA(n_components=2)#, random_state=None)
Y = model.fit_transform(X)
x_coords = Y[:, 0]
y_coords = Y[:, 1]
is_democrat = []
is_republican = []
names = []
with open("contribution_id_map/contribution_id_map_113.txt") as f:
  for line in f.readlines():
    data = line.rstrip("\n").split(",")
    names.append(data[1])
    if len(data) > 3:
	  party = data[3]
	  if party == "democrat":
	    is_democrat.append(True)
	    is_republican.append(False)
	  elif party == "republican":
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

plt.scatter(company_x, company_y, color="g")
plt.scatter(republican_x, republican_y, color="r", marker='^')
plt.scatter(democrat_x, democrat_y, color="b", marker='.')
plt.title("PCA on Democrats, Republicans, and Companies")
plt.show()

f = open("pca_output.csv",'w')
for i in range(len(names)):
	if is_republican[i]:
		f.write(names[i] + "," + str(x_coords[i]) + "," + str(y_coords[i]) + ",Republican\n")
	if is_democrat[i]:
		f.write(names[i] + "," + str(x_coords[i]) + "," + str(y_coords[i]) + ",Democrat\n")

