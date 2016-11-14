import unittest
import numpy as np
import graph
import kmeans


class TestGraph(unittest.TestCase):

    def setUp(self):
        pass

    def testKmeansSanity(self):
        similarity_matrix = [[100, 100, 0 , 0], 
                             [100, 100, 0 , 0], 
                             [ 0 ,  0 ,100,100], 
                             [ 0 ,  0 ,100,100]]
        km = kmeans.KMeans(similarity_matrix)
        km.Run()

        cluster1 = [0,1]
        cluster2 = [2,3]
        self.assertTrue((km.clusters[0] == cluster1 and km.clusters[1] == cluster2) or 
                        (km.clusters[1] == cluster1 and km.clusters[0] == cluster2))




if __name__ == "__main__":
    unittest.main()