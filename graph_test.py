import unittest
import numpy as np
import graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        pass

    def testGraph(self):
        nodes = ["zero", "one", "two", "three", "four"]
        g = graph.Graph(nodes) 
        self.assertEqual(g._GetId("zero"), 0)
        self.assertEqual(g._GetId("two"), 2)
        self.assertEqual(g._GetId("four"), 4)
        self.assertEqual(g._GetNode(1), "one")
        self.assertEqual(g._GetNode(3), "three")

    def testDenseGraphNeighbors(self):
        nodes = ["Alice", "Bob", "Carl", "David", "Ethan"]
        g = graph.DenseGraph(nodes)
        g.SetEdge("Alice", "Bob")
        g.SetEdge("Carl", "David")
        g.SetEdge("Ethan", "Ethan", 10.0)
        g._SetEdgeById(4, 0, 5.0, False)
        self.assertEqual(g._GetId("Alice"), 0)
        self.assertEqual(g._GetId("David"), 3)
        self.assertEqual(g.GetEdgeWeight("Ethan", "Alice"), 5.0)
        self.assertEqual(g.GetEdgeWeight("Alice", "Ethan"), 5.0)
        self.assertEqual(g.GetEdgeWeight("Alice", "Bob"), 1.0)

    def testDenseSparseNeighbors(self):
        nodes = ["Alice", "Bob", "Carl", "David", "Ethan"]
        g = graph.SparseGraph(nodes)
        g.SetEdge("Alice", "Bob")
        g.SetEdge("Carl", "David")
        g.SetEdge("Ethan", "Ethan", 10.0)
        g._SetEdgeById(4, 0, 5.0, False)
        self.assertEqual(g._GetId("Alice"), 0)
        self.assertEqual(g._GetId("David"), 3)
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

        g._ComputeNodesWithinRadius(r=None)
        alice_neighbors = g._GetNeighbors(node="Alice")
        self.assertEqual(alice_neighbors, ["Alice", "Bob"])
        
        bob_neighbors = g._GetNeighbors(node="Bob")
        self.assertEqual(bob_neighbors, ["Bob"])

        ethan_neighbors = g._GetNeighbors(node_id=4)
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

    def testSimrankNodesWithinRadius(self):
        #
        #    B - E
        #   /      \
        # A         F - G - H
        #   \       /
        #    C  -  D
        nodes = ["A", "B", "C", "D", "E", "F", "G", "H"] 
        edges = [("A", "B"), ("A", "C"), ("B", "E"), ("C", "D"), ("D", "F"),
                    ("E", "F"), ("F", "G"), ("G", "H")]
        g = graph.SimrankGraph(nodes)

        for edge in edges:
            g.SetEdge(edge[0], edge[1], directed=False)
        g._ComputeNodesWithinRadius(r=3) 
        neighbors_A = g._nodes_within_radius[0]
        expected_neighbors_A = [0, 1, 2, 3, 4, 5]
        self.assertEqual(set(expected_neighbors_A), set(neighbors_A))
        neighbors_H = g._nodes_within_radius[7]
        expected_neighbors_H = [7, 6, 5, 4, 3]
        self.assertEqual(set(expected_neighbors_H), set(neighbors_H))
       
        g._ComputeNodesWithinRadius(r=1) 
        neighbors_B = g._nodes_within_radius[1]
        expected_neighbors_B = [0, 1, 4]
        self.assertEqual(set(expected_neighbors_B), set(neighbors_B))

        g._ComputeNodesWithinRadius(r=-1)
        neighbors_D = g._nodes_within_radius[3]
        expected_neighbors_D = []
        self.assertEqual(set(expected_neighbors_D), set(neighbors_D))

        g._ComputeNodesWithinRadius(r=0)
        neighbors_C = g._nodes_within_radius[2]
        expected_neighbors_C = [2]
        self.assertEqual(set(expected_neighbors_C), set(neighbors_C))


        # test r = None
        g._ComputeNodesWithinRadius(r=None)
        neighbors_E = g._nodes_within_radius[4]
        expected_neighbors_E = range(8)
        self.assertEqual(set(expected_neighbors_E), set(neighbors_E))


        # (directed edges)
        #                                      G
        #                                    /
        # A - B - C - D                 E -  F
        #                                    \
        #                                     H
        #
        nodes = ["A", "B", "C", "D", "E", "F", "G", "H"] 
        edges = [("A", "B"), ("B", "C"), ("C", "D"),
                    ("E", "F"), ("F", "G"), ("F", "H")]
        g = graph.SimrankGraph(nodes)
        for edge in edges:
            g.SetEdge(edge[0], edge[1])
        g._ComputeNodesWithinRadius(r=2)
        neighbors_A = g._nodes_within_radius[0]
        expected_neighbors_A = [0, 1, 2] 
        self.assertEqual(set(expected_neighbors_A), set(neighbors_A))
        neighbors_D = g._nodes_within_radius[3]
        expected_neighbors_D = [3]
        self.assertEqual(set(expected_neighbors_D), set(neighbors_D))
        neighbors_F = g._nodes_within_radius[5]
        expected_neighbors_F = [5, 6, 7]
        self.assertEqual(set(expected_neighbors_F), set(neighbors_F))

    def testSimrankScale(self):
        NUM_NODES = 100
        nodes = range(NUM_NODES)
        g = graph.SimrankGraph(nodes)
        for i in range(NUM_NODES/2):
            for j in range(NUM_NODES/2 + 1, NUM_NODES):
                g.SetEdge(i, j, directed=True)

        g.Run(iterations=1, r=3)


if __name__ == "__main__":
    unittest.main()
