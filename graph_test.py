import unittest
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

    def testSimrankGraph(self):
        nodes = ["Alice", "Bob", "Carl", "David", "Ethan"]
        g = graph.SimrankGraph(nodes)
        g.SetEdge("Alice", "Bob")
        g.SetEdge("Carl", "David", directed=False)
        g.SetEdge("Ethan", "Ethan", 10.0)
        g.SetEdge("Ethan", "Alice", weight=-10.0)

        alice_neighbors = g.GetNeighbors(node="Alice")
        self.assertEqual(alice_neighbors, ["Bob"])
        
        bob_neighbors = g.GetNeighbors(node="Bob")
        self.assertEqual(bob_neighbors, [])

        ethan_neighbors = g.GetNeighbors(node_id=4)
        self.assertEqual(ethan_neighbors, ["Alice", "Ethan"])
        
        
if __name__ == "__main__":
    unittest.main()
