from evaluate import ReadNodeVectors, EntropyEvaluator
import numpy as np
import os

def ClusterByDemRep(vec_file, ground_truth_file):
    vecs = ReadNodeVectors(vec_file)
    ground_truth = []
    with open(ground_truth_file) as f:
        for line in f.readlines():
            data = line.rstrip("\n").split(",")
            if len(data) > 3:
                politician_party = data[3]
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
    for i in range(110, 115):
        print "Processing Congress #%d" %(i)
        vec_file = os.path.join("weighted_data", "contribution_node2vec_out_%d.txt" %(i))
        ground_truth_file = os.path.join("weighted_data", "contribution_id_map_%d.txt" %(i))
        ClusterByDemRep(vec_file, ground_truth_file)
        print

if __name__ == "__main__": main()
