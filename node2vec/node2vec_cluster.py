from evaluate import ReadNodeVectors, EntropyEvaluator
import numpy as np

def ClusterByParty():
    vecs = ReadNodeVectors("contribution_node2vec_out.txt")
    ground_truth = []
    with open("contribution_id_map.txt") as f:
        for line in f.readlines():
            data = line.rstrip("\n").split(",")
            if len(data) > 2:
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
    print "Entropy:", evaluator.evaluate(ground_truth) 

def main():
    ClusterByParty()

if __name__ == "__main__": main()
