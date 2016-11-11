import numpy as np

class Graph(object):
    """Represents a graph (nodes and edges).
    """

    def __init__(self, nodes):
        """Creates a graph with the given nodes.

        Args:
            nodes: (list) A list of objects that represent the nodes in the
                graph.
        """
        self._nodes = nodes
        self._node_to_id = {nodes[i]: i for i in range(len(nodes))}
        self._id_to_node = {i: nodes[i] for i in range(len(nodes))}

    def GetId(self, node):
        """Gets the internal id in range [0, NUM_NODES) for a given node.

        Args:
            node: (object) The source node. This is a value in the nodes list
                supplied in the constructor.

        Returns:
            node_id: (int) The internal id that represents the given node.
        """
        return self._node_to_id[node]

    def GetNode(self, node_id):
        """Gets the node given an internal id in range [0, NUM_NODES).

        Args:
            node_id: (int) The internal id in range [0, NUM_NODES).

        Returns:
            node: (object) The node the given ID represents.
        """
        return self._id_to_node[node_id]


class DenseGraph(Graph):
    """Represents a dense graph. This uses an adjacency matrix to store the
    edges.
    """

    def __init__(self, nodes):
        """Creates a dense graph with the given nodes.

        Args:
            nodes: (list) A list of objects that represent the nodes in the
                graph.
        """
        super(DenseGraph, self).__init__(nodes)
        self._adj = np.zeros((len(nodes), len(nodes)), dtype=np.float32)

    def SetEdgeById(self, from_id, to_id, weight=1.0, directed=True):
        """Sets an edge between two nodes.

        Args:
            from_id: (int) The internal id for the source node.
            to_id: (int) The internal id for the destination node.
            weight: (float) The weight of the edge
            directed: (bool) Whether the edge is directed.
        """
        self._adj[from_id][to_id] = weight
        if not directed:
            self._adj[to_id][from_id] = weight

    def SetEdge(self, from_node, to_node, weight=1.0, directed=True):
        """Sets an edge between two nodes.

        Args:
            from_node: (object) The source node. This is a value in the nodes
                list supplied in the constructor.
            to_node: (object) The destination node. This is a value in the
                nodes list supplied in the constructor.
        """
        from_id = self._node_to_id[from_node]
        to_id = self._node_to_id[to_node]
        self.SetEdgeById(from_id, to_id, weight, directed)

    def GetEdgeWeight(self, from_node=None, to_node=None, from_id=None,
                        to_id=None):
        """Gets the edge weight between two nodes. Either the nodes or the ids
        should be specified but not both.

        Args:
            from_node: (object) The source node.
            to_node: (object) The destination node.
            from_id: (int) The internal node id for the source node.
            to_id: (int) The internal node id for the destination node.
        """
        if ((from_node is not None and to_node is not None) and
                                        (from_id is None and to_id is None)):
            from_id = self._node_to_id[from_node]
            to_id = self._node_to_id[to_node]
            return self._adj[from_id][to_id]

        if ((from_node is None and to_node is None) and
                                (from_id is not None and to_id is not None)):
            return self._adj[from_id][to_id]

        raise ValueError("Must specify (from_node, to_node)"
                            "or (from_id, to_id), but not both")


class SimrankGraph(DenseGraph):
    """A DenseGraph with functions for the SimRank algorithm.
    """

    def __init__(self, nodes):
        """Creates a graph on which to run SimRank.

        Args:
            nodes: (list of object) The nodes in the graph.
        """
        super(SimrankGraph, self).__init__(nodes)
        self._similarity = np.identity(len(nodes), dtype=np.float32)

        for i in range(len(self._nodes)):
            self._adj[i][i] = 1.0

    def GetNeighbors(self, node=None, node_id=None):
        """Gets the neighbors of the given node. Either the node or the node_id
        but not both should be specified. A neighbor of a given node has a
        directed edge coming into it from the given node. If a node links to
        itself, it is a neighbor of itself.

        Args:
            node: (object) The node for which to obtain neighbors.
            node_id: (int) The node id for which to obtain neighbors.

        Returns:
            neighbors: (list of object) A list of neighbors. The list contains
                objects in the nodes list passed in to the constructor. The
                list is sorted by internal node id (the order in the list passed
                to the constructor).
        """
        if node is None and node_id is None:
            raise ValueError("Must specify either node or node_id.")
        if node is not None and node_id is not None:
            raise ValueError("Can only specify one of node or node_id.")
        
        if node is not None:
            node_id = self._node_to_id[node]
        
        neighbors = []
        for i in range(len(self._nodes)):
            if self.GetEdgeWeight(from_id=node_id, to_id=i) != 0.0:
                neighbors.append(self._id_to_node[i])
        return neighbors

    def Run(self, iterations=5, C=0.8):
        """Runs the SimRank algorithm to determine the node similarity between
        all pairs of nodes. Note: similarity is not reset after each call to
        this function, so you can continue running for more iterations later on.

        Args:
            iterations: (int) Number of iterations for which to run.
        """
        for iteration in range(iterations):
            next_similarity = np.zeros((len(self._nodes), len(self._nodes)))
            for i in range(len(self._nodes)):
                for j in range(len(self._nodes)):
                    node1_neighbors = self.GetNeighbors(node_id=i)
                    node2_neighbors = self.GetNeighbors(node_id=j)
                    for node1_neighbor in node1_neighbors:
                        for node2_neighbor in node2_neighbors:
                            node1_id = self._node_to_id[node1_neighbor]
                            node2_id = self._node_to_id[node2_neighbor]
                            next_similarity[i][j] += self._similarity[node1_id][node2_id]
                    multiplier = C / float(len(node1_neighbors) *
                                            len(node2_neighbors))
                    next_similarity[i][j] *= multiplier
            self._similarity = next_similarity

    def Similarity(self, a, b):
        """Returns the similarity between two nodes.

        Args:
            a: (object) A node
            b: (object) Another node

        Returns:
            sim: (float) The similarity between a and b
        """
        a_id = self._node_to_id[a]
        b_id = self._node_to_id[b]
        return self._similarity[a_id][b_id]
                            
                    
         
