import unittest
import numpy as np
import graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        pass

    def testGraph(self):
        nodes = ["zero", "one", "two", "three", "four"]
        g = graph.Graph(nodes) 
        self.assertEqual(g.GetId("zero"), 0)
        self.assertEqual(g.GetId("two"), 2)
        self.assertEqual(g.GetId("four"), 4)
        self.assertEqual(g.GetNode(1), "one")
        self.assertEqual(g.GetNode(3), "three")

    def testDenseGraphNeighbors(self):
        nodes = ["Alice", "Bob", "Carl", "David", "Ethan"]
        g = graph.DenseGraph(nodes)
        g.SetEdge("Alice", "Bob")
        g.SetEdge("Carl", "David")
        g.SetEdge("Ethan", "Ethan", 10.0)
        g.SetEdgeById(4, 0, 5.0, False)
        self.assertEqual(g.GetId("Alice"), 0)
        self.assertEqual(g.GetId("David"), 3)
        self.assertEqual(g.GetEdgeWeight("Ethan", "Alice"), 5.0)
        self.assertEqual(g.GetEdgeWeight("Alice", "Ethan"), 5.0)
        self.assertEqual(g.GetEdgeWeight("Alice", "Bob"), 1.0)

    def testSimrankGraphNeighbors(self):
        nodes = ["Alice", "Bob", "Carl", "David", "Ethan"]
        g = graph.SimrankGraph(nodes)
        g.SetEdge("Alice", "Bob")
        g.SetEdge("Carl", "David", directed=False)
        g.SetEdge("Ethan", "Ethan", 10.0)
        g.SetEdge("Ethan", "Alice", weight=-10.0)

        alice_neighbors = g.GetNeighbors(node="Alice")
        self.assertEqual(alice_neighbors, ["Alice", "Bob"])
        
        bob_neighbors = g.GetNeighbors(node="Bob")
        self.assertEqual(bob_neighbors, ["Bob"])

        ethan_neighbors = g.GetNeighbors(node_id=4)
        self.assertEqual(ethan_neighbors, ["Alice", "Ethan"])

    def testSimrankSanity(self):
        nodes = ["Alice", "Bob", "Carl"]
        g = graph.SimrankGraph(nodes)
        g.SetEdge("Alice", "Bob", directed=False)
        g.SetEdge("Carl", "Bob", directed=False)
        g.Run(iterations=1, C=1.0)
        
        # Alice and Carl both have neighbors [Bob]. This gives a sum of 
        # 1. The multiplier is 1.0/4. Therefore, the similarity should be .25.
        self.assertEqual(g.Similarity("Alice", "Carl"), 0.25)

    def testSimrankAlgorithm(self):
        nodes = ["Baker", "Chef", "Programmer",
                "Eggs", "Flour", "Chocolate",
                "Meat", "Rice", "Onion",
                "Computer", "Keyboard", "Headphones"]
        g = graph.SimrankGraph(nodes)

        edges = [("Baker", "Eggs"), ("Baker", "Flour"), ("Baker", "Chocolate"),
                    ("Chef", "Eggs"), ("Chef", "Flour"), ("Chef", "Meat"),
                    ("Chef", "Rice"), ("Chef", "Onion"),
                    ("Programmer", "Computer"), ("Programmer", "Keyboard"),
                    ("Programmer", "Headphones"), ("Programmer", "Chocolate")]

        for edge in edges:
            g.SetEdge(edge[0], edge[1], directed=False)

        g.Run(iterations=5, C=0.6)

        self.assertTrue(g.Similarity("Baker", "Chef") >
                        g.Similarity("Baker", "Programmer"))
        self.assertTrue(g.Similarity("Baker", "Programmer") >
                        g.Similarity("Chef", "Programmer"))
        self.assertTrue(g.Similarity("Eggs", "Flour") >
                        g.Similarity("Eggs", "Headphones"))
        self.assertTrue(g.Similarity("Eggs", "Chocolate") >
                        g.Similarity("Eggs", "Headphones"))
        self.assertTrue(np.isclose(g.Similarity("Baker", "Chef"),
                        g.Similarity("Chef", "Baker")))

        print "Baker ~ Chef:", g.Similarity("Baker", "Chef")
        print "Baker ~ Programmer:", g.Similarity("Baker", "Programmer")
        print "Chef ~ Programmer:", g.Similarity("Chef", "Programmer")

if __name__ == "__main__":
    unittest.main()
