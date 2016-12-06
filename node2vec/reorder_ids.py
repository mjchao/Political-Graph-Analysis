
oldNameToID = {}

with open('contribution_id_map_old.txt', 'r') as f1:
  for line in f1:
    line = line[:-1]
    line = line.split(',')
    oldNameToID[line[1]] = line[0]

string = [0] * len(oldNameToID)

with open('contribution_id_map.txt', 'r') as f1:
  for line in f1:
    line = line[:-1]
    line = line.split(',')
    line[0] = oldNameToID[line[1]]
    string[int(line[0])] = ','.join(line)

with open('contribution_id_map_new.txt', 'w') as f1:
  for i in xrange(len(string)):
    f1.write(string[i] + '\n')