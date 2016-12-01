import numpy as np
from numpy import random

class KMeans():
    def __init__(self, similarities):
        self._similarities = similarities

    def Run(self, num_clusters=2, iterations=100):
        self.centers = np.random.randint(0, len(self._similarities), num_clusters)
        for i in range(iterations):
            self.clusters = [[] for i in range(num_clusters)]
            indexes = [i for i in range(len(self._similarities))]
            for i in indexes:
                best_cluster = -1
                highest_sim_score = 0
                for cluster in range(num_clusters):
                    if self._similarities[i][self.centers[cluster]] > highest_sim_score:
                        best_cluster = cluster
                        highest_sim_score = self._similarities[i][self.centers[cluster]]
                self.clusters[best_cluster].append(i)


            for cluster_index, cluster in enumerate(self.clusters):
                best_average_similarity = 0
                best_center = -1
                for i in range(len(cluster)):
                    total_similarity = 0
                    for j in range(len(cluster)):
                        if i != j:
                            total_similarity += self._similarities[cluster[i]][cluster[j]]
                    average_similarity = total_similarity / len(cluster)
                    if average_similarity > best_average_similarity:
                        best_average_similarity = average_similarity
                        best_center = i
                self.centers[cluster_index] = best_center

    def Save(self, fn):
        """Saves the clusters to fn

        Args:
            fn: (string) The filename to save to. Should end with 
            '.csv' or '.txt'
        """

        np.savetxt(fn, np.array(self. clusters), delimiter=',')

    def Load(self, fn):
        """Loads the clusters from fn

        Args:
            fn: (string) The filename to load from. Should end with
            '.csv' or '.txt'
        """
        self.clusters = np.loadtxt(fn, delimiter=',')