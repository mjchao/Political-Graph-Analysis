import numpy as np
import scipy as sp
from sklearn.cluster import KMeans

def ReadNodeVectors(vec_filename):
    """Reads node vectors from a file.

    Args:
        vec_filename: (string) the file from which to read node vectors.

    Returns:
        vecs: (numpy array) Numpy array of shape (# vecs, vec size) that are
            the node vectors.
    """
    with open(vec_filename) as f:
        dims = f.readline().split()
        num_vecs = int(dims[0])
        vec_size = int(dims[1])
        vecs = np.zeros((num_vecs, vec_size))
        for i in range(num_vecs):
            vec_entries = f.readline().split()
            vec_idx = int(vec_entries[0])
            for j in range(vec_size):
                vecs[vec_idx][j] = float(vec_entries[1 + j])
    return vecs


class Evaluator(object):
    """Evaluates the entropy among the clusters that a clustering algorithm
    will achieve on node2vec's node vectors.
    """

    def __init__(self, clustering_alg=KMeans):
        """Clustering on node2vec node vectors.

        Args:
            clustering_alg: (sklearn clusterer) Class of any sklearn clustering
                algorithm (e.g. KMeans).
        """
        self._alg = clustering_alg

    def fit(self, vecs, n_clusters):
        """Fits a clustering model to some node vectors.

        Args:
            vecs: (numpy array) node vectors to use.
            n_clusters: (int) number of clusters to use.
        """
        self._vecs = vecs
        self._n_clusters = n_clusters
        self._clustering = self._alg(n_clusters=n_clusters)
        self._labels = self._clustering.fit_predict(self._vecs)

    def predict(self, vecs):
        """Predicts the labels of the given node vectors.

        Args:
            vecs: (numpy array) Some node vectors.

        Returns:
            labels: (numpy array) Array of labels for each of the node vectors.
        """
        return self._clustering.predict(vecs)

    def GetDistributionAmongClusters(self, ground_truth):
        """Gets the distribution of the true classes within each cluster.

        Args:
            ground_truth: (2D array) Array of length num_vectors that is the
                actual label of each node vector.

        Returns:
            cluster_true_labels: (numpy array) Array of shape
                (n_clusters, n_clusters). The value at index (i, j) is the
                number of vectors categorized into cluster i with ground truth
                label j.
        """
        cluster_true_labels = np.zeros((self._n_clusters, self._n_clusters))
        for i in range(len(self._labels)):
            true_label = ground_truth[i]
            if true_label >= self._n_clusters:
                raise ValueError("Ground truth label out of range."
                                    "Must be in range [0, %d]"
                                    %(self._n_clusters - 1))
            if true_label != -1:
                cluster_id = self._labels[i]
                cluster_true_labels[cluster_id][true_label] += 1
        return cluster_true_labels 

class EntropyEvaluator(Evaluator):
    
    def __init__(self, clustering_alg=KMeans):
        super(EntropyEvaluator, self).__init__(clustering_alg)

    def evaluate(self, ground_truth):
        """Evaluates the model against some ground truth labels of the node
        vectors.

        Args:
            ground_truth: (array of int) The true labels of each node vector.
                Labels should be nonnegative, consecutive (i.e. 0, 1, 2, ...).
                If the label is -1, the example will be ignored.
        """
        cluster_true_labels = self.GetDistributionAmongClusters(ground_truth) 

        entropies = []
        for i in range(self._n_clusters):
            num_elements = np.sum(cluster_true_labels[i, :])
            if num_elements == 0:
                entropies.append(np.nan)
            else:
                cluster_probabilities = (cluster_true_labels[i, :] /
                                        float(num_elements))
                entropies.append(sp.stats.entropy(cluster_probabilities,
                                 base=self._n_clusters))
        return np.array(entropies)
