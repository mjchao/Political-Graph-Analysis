from evaluate import ReadNodeVectors, EntropyEvaluator
import numpy as np
import os
from optparse import OptionParser

def ClusterByDemRep(vec_file, ground_truth_file):
    vecs = ReadNodeVectors(vec_file)
    ground_truth = []
    with open(ground_truth_file) as f:
        for line in f.readlines():
            data = line.rstrip("\n").split(",")
            entity_id = int(data[0])
            if np.any(np.isnan(vecs[entity_id, :])):
                ground_truth.append(-2)
            if len(data) > 3:
                politician_party = data[3].lower()
                if politician_party == "democrat":
                    ground_truth.append(0)
                elif politician_party == "republican":
                    ground_truth.append(1)
                else:
                    ground_truth.append(-1)
            else:
                ground_truth.append(-1)
    
    evaluator = EntropyEvaluator()
    evaluator.fit(vecs, 2)
    print "Distribution:"
    print evaluator.GetDistributionAmongClusters(ground_truth)

    entropy = evaluator.evaluate(ground_truth)
    print "Entropy:", entropy
    print "Average entropy:", np.mean(entropy)


def main():
    parser = OptionParser()
    parser.add_option("-t", "--tripartite", action="store_true",
                        dest="tripartite", default=False,
                        help="Use tripartite graph node2vec results.")
    parser.add_option("-w", "--weighted", action="store_true",
                        dest="weighted", default=False,
                        help="Use weighted node2vec results.")
    options, args = parser.parse_args()
    if options.tripartite:
        for i in range(105, 106):
            print "Processing Congress #%d (tripartite, unweighted)" %(i)
            vec_file = os.path.join("tripartite", "tripartite_node2vec_out_%d.txt" %(i))
            ground_truth_file = os.path.join("tripartite", "%d_key.txt" %(i))
            ClusterByDemRep(vec_file, ground_truth_file)
            print
    else:
        if not options.weighted:
            for i in range(105, 115):
                print "Processing Congress #%d (unweighted)" %(i)
                vec_file = os.path.join("data", "contribution_node2vec_out_%d.txt" %(i))
                ground_truth_file = os.path.join("data", "contribution_id_map_%d.txt" %(i))
                ClusterByDemRep(vec_file, ground_truth_file)
                print
        elif options.weighted:
            for i in range(105, 115):
                print "Processing Congress #%d (weighted)" %(i)
                vec_file = os.path.join("weighted_data", "contribution_node2vec_out_%d.txt" %(i))
                ground_truth_file = os.path.join("weighted_data", "contribution_id_map_%d.txt" %(i))
                ClusterByDemRep(vec_file, ground_truth_file)
                print

if __name__ == "__main__": main()
