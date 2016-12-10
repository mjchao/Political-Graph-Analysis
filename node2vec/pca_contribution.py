"""Usage

-f, --file: The file with the node vectors.
-g, --ground_truth: The file with the ground truth (democrat/republican)
-a, --comp1: The first principal component onto which to project. E.g. 1
-b, --comp2: The second principal component onto which to project. E.g. 5
-c, --comp3: The third principal component onto which to project. E.g. 7

Example:

python pca_contribution.py -f data/contribution_node2vec_out_105.txt -g data/contribution_id_map_105.txt -a 1 -b 2
"""
import numpy as np
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import sys
from evaluate import ReadNodeVectors
from optparse import OptionParser

def ReadGroundTruth(filename):
    """Reads  ground truth data from a file. If an entity is not democrat and
    not republican, it is treated as a company.

    Arg:
        filename: (string) name of file with ground truth.

    Returns:
        is_democrat: (numpy array) Array of shape (n,) which indicates whether
            each entity is democrat.
        is_republican: (numpy array) Array of shape (n,) which indicates whether
            each entity is republican.
        name_to_id: (dict) Maps names of entities to their IDs.
        id_to_name: (dict) Maps IDs of entities to their names.
    """
    name_to_id = {}
    id_to_name = {}
    is_democrat = []
    is_republican = []
    with open(filename) as f:
        for line in f.readlines():
            data = line.rstrip("\n").split(",")
            entity_id = int(data[0])
            name = data[1]
            name_to_id[name] = entity_id
            id_to_name[entity_id] = name
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
    return np.array(is_democrat), np.array(is_republican), name_to_id, id_to_name

def PlotProjectionsWithRepDemCompany(node_vecs, comps, is_republican, is_democrat):
    """Plots the projection of the node vectors onto the specified components.

    Args:
        node_vecs: (numpy array) 2D array of shape (n, m). The node vectors.
        comps: (list of int - max 3) The indices of the components onto which
            to project. For example, if comps is [1, 5, 10], this will project
            onto the 1st, 5th, and 10th principal components.
        is_republican: (numpy array) Array of shape (n,). Indicates for each i,
            if the i-th node vector represents a republican legislator.
        is_democrat: (numpy array) Array of shape (n,). Indicates for each i,
            if the i-th node vector represents a democrat legislator.
    """
    if len(comps) > 3:
        raise ValueError("Cannot visualize more than 3 dimensions!")

    pca = PCA(n_components=max(comps), random_state=None)
    proj_values = pca.fit_transform(node_vecs)

    is_company = np.logical_and(np.logical_not(is_republican),
                                np.logical_not(is_democrat))
    if len(comps) == 1:
        x_coords = proj_values[:, comps[0]-1]
        republican_x = x_coords[is_republican]
        democrat_x = x_coords[is_democrat]
        company_x = x_coords[is_company]
        plt.scatter(company_x, [0]*len(company_x), color="g")
        plt.scatter(republican_x, [0]*len(republican_x), color="r", marker='^') 
        plt.scatter(democrat_x, [0]*len(democrat_x), color="b", marker='.')
    elif len(comps) == 2:
        x_coords = proj_values[:, comps[0]-1]
        y_coords = proj_values[:, comps[1]-1]
        republican_x = x_coords[is_republican]
        republican_y = y_coords[is_republican]
        democrat_x = x_coords[is_democrat]
        democrat_y = y_coords[is_democrat]
        company_x = x_coords[is_company]
        company_y = y_coords[is_company]
        plt.scatter(company_x, company_y, color="g")
        plt.scatter(republican_x, republican_y, color="r", marker="^")
        plt.scatter(democrat_x, democrat_y, color="b", marker=".")
    elif len(comps) == 3:
        x_coords = proj_values[:, comps[0]-1]
        y_coords = proj_values[:, comps[1]-1]
        z_coords = proj_values[:, comps[2]-1]
        republican_x = x_coords[is_republican]
        republican_y = y_coords[is_republican]
        republican_z = z_coords[is_republican]
        democrat_x = x_coords[is_democrat]
        democrat_y = y_coords[is_democrat]
        democrat_z = z_coords[is_democrat]
        company_x = x_coords[is_company]
        company_y = y_coords[is_company]
        company_z = z_coords[is_company]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        sampled_companies = (np.random.rand(len(company_x)) < 0.1)
        ax.scatter(company_x[sampled_companies], company_y[sampled_companies], company_z[sampled_companies], color="g")
        ax.scatter(republican_x, republican_y, republican_z, color="r", marker="^")
        ax.scatter(democrat_x, democrat_y, democrat_z, color="b", marker=".")

    plt.show()

def main():
    parser = OptionParser()
    parser.add_option("-o", "--old_pca", action="store_true", dest="old_pca",
                        help="use original PCA code (before code became modular).")
    parser.add_option("-f", "--file", action="store", dest="file",
                        help="node vector file.")
    parser.add_option("-g", "--ground_truth", action="store",
                        dest="ground_truth",
                        help="file containing the ground truth.")
    parser.add_option("-a", "--comp1", action="store", dest="comp1",
                        default=None,
                        help="component index to display on x axis.")
    parser.add_option("-b", "--comp2", action="store", dest="comp2",
                        default=None,
                        help="component index to display on y axis.")
    parser.add_option("-c", "--comp3", action="store", dest="comp3",
                        default=None,
                        help="component index to display on z axis.")
    options, args = parser.parse_args()

    if options.old_pca:
        main2()
        return

    comps = []
    if options.comp1 is not None:
        comps.append(int(options.comp1))
    if options.comp2 is not None:
        comps.append(int(options.comp2))
    if options.comp3 is not None:
        comps.append(int(options.comp3))

    if len(comps) == 0:
        print "Please specify a component onto which to project!"
    else:
        node_vecs = ReadNodeVectors(options.file)
        is_democrat, is_republican, _, _ = ReadGroundTruth(options.ground_truth)
        PlotProjectionsWithRepDemCompany(node_vecs, comps, is_democrat,
                                            is_republican)
    

def main2():
    X = np.empty([1])
    print 'Reading in feature matrix file...'
    # Read in node2vec into np.array
    with open('data/contribution_node2vec_out_114.txt', 'r') as f:
        numNodes, numFeatures = map(int, (f.readline()[:-1]).split(' '))
        print 'Number of nodes: ' + str(numNodes)
        print 'Number of features: ' + str(numFeatures)
        X = np.empty([numNodes, numFeatures])
        for line in f:
            nodeValues = map(float, line[:-1].split(' '))
            X[int(nodeValues[0])] = nodeValues[1:numFeatures+1]

    # TODO may want to run PCA before TSNE to reduce the feature dimension down to the suggested 50 features
    print 'Modelling t-SNE...'
    model = PCA(n_components=2, random_state=None)
    Y = model.fit_transform(X)
    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    is_democrat = []
    is_republican = []
    name_to_id = {}
    id_to_name = {}
    with open("data/contribution_id_map_114.txt") as f:
        for line in f.readlines():
            data = line.rstrip("\n").split(",")
            entity_id = int(data[0])
            name = data[1]
            name_to_id[name] = entity_id
            id_to_name[entity_id] = name
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

    def annotate(name):
        entity_id = name_to_id[name]
        print "Annotate point at", x_coords[entity_id], y_coords[entity_id]
        plt.annotate(name, xy=(x_coords[entity_id], y_coords[entity_id]))

    lowest_x = (999, -1)
    highest_x = (-999, -1)
    for i in range(len(x_coords)):
        if is_republican[i] or is_democrat[i]:
            if x_coords[i] < lowest_x[0]:
                lowest_x = (x_coords[i], i)
            if x_coords[i] > highest_x[0]:
                highest_x = (x_coords[i], i)

    print "Low extreme:", id_to_name[lowest_x[1]]
    print "High extreme:", id_to_name[highest_x[1]]
            
    annotate("mitch mcconnell")
    annotate("nancy pelosi")
    annotate("jim jordan")
    annotate("bernie sanders")
    annotate("trump organization")
    plt.show()

if __name__ == "__main__":
    main()
    sys.exit(0)

    

