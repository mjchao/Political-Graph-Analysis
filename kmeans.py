import numpy as np
from numpy import random

class KMeans():
    def __init__(self, similarities):
        self._similarities = similarities

    def Run(self, num_clusters=2, maxIterations=100):
        self.centers = np.random.randint(0, len(self._similarities), num_clusters)
        count = 0
        while True:
            print count
            count = count + 1
            prevCenters = list(self.centers)
            self.clusters = [[] for i in range(num_clusters)]

            for i in range(num_clusters):
                self.clusters[i].append(self.centers[i])

            for i in range(len(self._similarities)):
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
                    if len(cluster) <= 1:
                        continue
                    total_similarity = 0
                    for j in range(len(cluster)):
                        if i != j:
                            total_similarity += self._similarities[cluster[i]][cluster[j]]
                    average_similarity = total_similarity / (len(cluster)-1)
                    if average_similarity > best_average_similarity:
                        best_average_similarity = average_similarity
                        best_center = i
                self.centers[cluster_index] = i

            # If converged
            converged = True
            for i in range(len(prevCenters)):
                if prevCenters[i] != self.centers[i]:
                    converged = False
                    break
            if converged or count >= maxIterations:
                break

    def Save(fn):
        """Saves the clusters to fn

        Args:
            fn: (string) The filename to save to. Should end with 
            '.csv' or '.txt'
        """

        np.savetxt(fn, np.array(clusters), delimiter=',')

    def Load(fn):
        """Loads the clusters from fn

        Args:
            fn: (string) The filename to load from. Should end with
            '.csv' or '.txt'
        """
        self.clusters = np.loadtxt(fn, delimiter=',')