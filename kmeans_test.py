import unittest
import numpy as np
import graph
import kmeans


class TestGraph(unittest.TestCase):

    def setUp(self):
        pass

    def testSimrankSanity(self):
        nodes = ["Alice", "Bob", "Carl"]
        g = graph.SimrankGraph(nodes)
        g.SetEdge("Alice", "Bob", directed=False)
        g.SetEdge("Carl", "Bob", directed=False)
        g.Run(iterations=1, C=1.0)

        km = kmeans.KMeans(g._similarity)
        km.Run()
        self.assertTrue(len(km.clusters) == 2)
        
        

    # def testSimrankAlgorithm(self):
    #     nodes = ["Baker", "Chef", "Programmer",
    #             "Eggs", "Flour", "Chocolate",
    #             "Meat", "Rice", "Onion",
    #             "Computer", "Keyboard", "Headphones"]
    #     g = graph.SimrankGraph(nodes)

    #     edges = [("Baker", "Eggs"), ("Baker", "Flour"), ("Baker", "Chocolate"),
    #                 ("Chef", "Eggs"), ("Chef", "Flour"), ("Chef", "Meat"),
    #                 ("Chef", "Rice"), ("Chef", "Onion"),
    #                 ("Programmer", "Computer"), ("Programmer", "Keyboard"),
    #                 ("Programmer", "Headphones"), ("Programmer", "Chocolate")]

    #     for edge in edges:
    #         g.SetEdge(edge[0], edge[1], directed=False)

    #     g.Run(iterations=5, C=0.6)

    #     self.assertTrue(g.Similarity("Baker", "Chef") >
    #                     g.Similarity("Baker", "Programmer"))
    #     self.assertTrue(g.Similarity("Baker", "Programmer") >
    #                     g.Similarity("Chef", "Programmer"))
    #     self.assertTrue(g.Similarity("Eggs", "Flour") >
    #                     g.Similarity("Eggs", "Headphones"))
    #     self.assertTrue(g.Similarity("Eggs", "Chocolate") >
    #                     g.Similarity("Eggs", "Headphones"))
    #     self.assertTrue(np.isclose(g.Similarity("Baker", "Chef"),
    #                     g.Similarity("Chef", "Baker")))

    #     print "Baker ~ Chef:", g.Similarity("Baker", "Chef")
    #     print "Baker ~ Programmer:", g.Similarity("Baker", "Programmer")
    #     print "Chef ~ Programmer:", g.Similarity("Chef", "Programmer")



if __name__ == "__main__":
    unittest.main()