#!/usr/bin/env python

import sys
import numpy as np
import subprocess
import pdb
import time


def date_time():
    cur_date = ">" + time.strftime("%c") + '\n'
    return cur_date


if len(sys.argv) < 2:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' {table to permute} {iterations} {table to not permute} '
                                               '{ R script location}{ K } {alpha} {T}\n')
    exit(1)

eset2 = sys.argv[1]
tbl = open(eset2, 'r')
k = int(sys.argv[2])
eset1 = sys.argv[3]
runSNF = sys.argv[4]
K = sys.argv[5]
alpha = sys.argv[6]
T = sys.argv[7]

Samples = next(tbl)
Samples = Samples.rstrip('\n').split('\t')
Genes = []
# populate numpy array with data
data = np.array(Samples[1:], dtype=str)

# create data matrix, initialize as size of head
sys.stderr.write(date_time() + 'Reading table to permute into memory ' + eset2 + '\n')
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
temp_fn = 'temp_eset2_permutated.txt'
sys.stderr.write(date_time() + 'Permuting table. ' + str(k) + ' iterations indicated\n')
for i in xrange(1, (k+1), 1):
    sys.stderr.write(date_time() + 'At iteration ' + str(i) + '\n')
    new = np.transpose(np.random.permutation(np.transpose(data)))
    headers.write(str(i) + '\t' + '\t'.join(new[0]) + '\n')
    new = np.delete(new, 0, axis=0)
    cur = open(temp_fn, 'w')
    cur.write('\t'.join(Samples) + '\n')
    j = 0
    for values in new:
        cur.write(Genes[j] + '\t' + '\t'.join(values) + '\n')
        j += 1
    cur.close()

    # run snf on scrambled data set
    rcmd = 'Rscript ' + runSNF + ' ' + eset1 + ' ' + temp_fn + ' ' + out + ' ' + str(i) + ' '.join((K, alpha, T))
    subprocess.call(rcmd, shell=True)
sys.stderr.write(date_time() + 'Permutations complete!\n')