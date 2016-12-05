import unittest
import numpy as np
import os
from evaluate import EntropyEvaluator
from sklearn.cluster import KMeans


class TestGraph(unittest.TestCase):
    _TEST_DATA = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])

    def setUp(self):
        pass

    def testFit(self):
        evaluator = EntropyEvaluator(KMeans)
        evaluator.fit(TestGraph._TEST_DATA, 2)

    def testDistributionAmongClusters(self):
        evaluator = EntropyEvaluator(KMeans)
        evaluator.fit(TestGraph._TEST_DATA, 2)
        evaluator._labels = [1, 1, 0, 0]
        distribution = evaluator.GetDistributionAmongClusters([1, 1, 0, 0])
        self.assertTrue(np.all(distribution == [[2, 0],
                                                [0, 2]]))
        distribution = evaluator.GetDistributionAmongClusters([0, 0, 1, 1])
        self.assertTrue(np.all(distribution == [[0, 2],
                                                [2, 0]]))
        distribution = evaluator.GetDistributionAmongClusters([-1, 0, 1, 1])
        self.assertTrue(np.all(distribution == [[0, 2],
                                                [1, 0]]))

    def testInvalidGroundTruth(self):
        evaluator = EntropyEvaluator(KMeans)
        evaluator.fit(TestGraph._TEST_DATA, 2)
        with self.assertRaises(ValueError):
            evaluator.GetDistributionAmongClusters([1, 2, 0, 0])

    def testEvaluate(self):
        evaluator = EntropyEvaluator(KMeans)
        evaluator.fit(TestGraph._TEST_DATA, 2)
        evaluator._labels = [1, 1, 0, 0]
        self.assertTrue(np.all(evaluator.evaluate([1, 1, 0, 0]) == [0, 0]))
        evaluator._labels = [0, 0, 1, 1]
        self.assertTrue(np.all(evaluator.evaluate([1, 1, 0, 0]) == [0, 0]))
        evaluator._labels = [1, 0, 1, 0]
        self.assertTrue(np.all(evaluator.evaluate([1, 1, 0, 0]) == [1, 1]))
        self.assertTrue(np.all(np.isnan(evaluator.evaluate([-1, -1, -1, -1]))))
        
    
if __name__ == "__main__":
    unittest.main()
