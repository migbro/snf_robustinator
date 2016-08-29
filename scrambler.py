#!/usr/bin/env python

import sys
import numpy as np
import subprocess
import pdb
if len(sys.argv) < 2:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' {table to permute} {iterations} {table to not permute}\n')
    exit(1)
runSNF = '/Users/Miguel/Documents/Scripts/white_lab/snf_robustinator/runSNF2.R'
eset2 = sys.argv[1]
tbl = open(eset2, 'r')
k = int(sys.argv[2])
eset1 = sys.argv[3]

Samples = next(tbl)
Samples = Samples.rstrip('\n').split('\t')
Genes = []
# populate numpy array with data
data = np.array(Samples[1:], dtype=str)

# create data matrix, initialize as size of head

for line in tbl:
    info = line.rstrip('\n').split('\t')
    Genes.append(info[0])
    cur = np.array(info[1:])
    data = np.vstack((data, cur))
headers = open('permuted_samples_' + str(k) + 'x.txt', 'w')
data = data.astype(np.str)
# Will permute with header column, but then replace with original to satisfy software while still tracking rearranged
#  indices
out = 'permutation_res.txt'
for i in xrange(1, (k+1), 1):
    new = np.transpose(np.random.permutation(np.transpose(data)))
    headers.write(str(i) + '\t' + '\t'.join(new[0]) + '\n')
    new = np.delete(new, (0), axis=0)
    cur = open('eset2_permutated.txt', 'w')
    cur.write('\t'.join(Samples) + '\n')
    j = 0
    for values in new:
        cur.write(Genes[j] + '\t' + '\t'.join(values) + '\n')
        j += 1
    cur.close()

    # run snf on scrambled data set
    rcmd = 'Rscript ' + runSNF + ' ' + eset1 + ' eset2_permutated.txt ' + out + ' ' + str(i)
    subprocess.call(rcmd, shell=True)