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
    parser.add_option("-s", "--start", action="store", dest="start", default=105,
                        help="Start session (inclusive).")
    parser.add_option("-e", "--end", action="store", dest="end", default=115,
                        help="End session (exclusive).")
    parser.add_option("-f", "--vec_file", action="store", dest="vec_file",
                        help="Filename pattern for node vectors.")
    parser.add_option("-g", "--gt_file", action="store", dest="gt_file",
                        help="Filename pattern for ground truth.")

    options, args = parser.parse_args()
    for i in range(int(options.start), int(options.end)):
        print "Processing Congress #%d" %(i)
        vec_file = options.vec_file %(i)
        ground_truth_file = options.gt_file %(i)
        ClusterByDemRep(vec_file, ground_truth_file)
        print

if __name__ == "__main__": main()
