#!/usr/bin/env python

import sys
import numpy as np
if len(sys.argv) < 2:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' {table} {iterations}')
    exit(1)
eset2 = sys.argv[1]
tbl = open(eset2, 'r')
k = int(sys.argv[2])
eset1 = sys.argv[3]

Samples = next(tbl)
Samples = Samples.rstrip('\n').split('\t')
Genes = []
# populate numpy array with data
data = np.array(Samples[1:])

# create data matrix, initialize as size of head

for line in tbl:
    info = line.rstrip('\n').split('\t')
    Genes.append(info[0])
    data = np.vstack([data, info[1:]])

headers = open('permuted_samples_' + str(k) + 'x.txt', 'w')

# Will permute with header column, but then replace with original to satisfy software while still tracking rearranged
#  indices
for i in xrange(1, k, 1):
    new = np.transpose(np.random.permutation(np.transpose(data)))
    headers.write(str(i) + '\t' + '\t'.join(new[0]) + '\n')
    new = np.delete(new, 0)
    cur = open('eset2_perumutated.txt', 'w')
    cur.write(Samples + '\n')
    for j in xrange(0, len(Genes), 1):
        cur.write(Genes[j] + '\t' + '\t'.join(new[j]) + '\n')
    cur.close()
    # run snf on scrambled data set