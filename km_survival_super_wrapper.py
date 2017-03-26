#!/usr/bin/env python

import sys
import os
from job_manager import job_manager


if len(sys.argv) < 3:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' {km survival r script location} {SNF param table}\n')
    exit(1)
km_survival_wrapper = '/home/ubuntu/TOOLS/snf_robustinator/km_survival_wrapper.py'
r_script = sys.argv[1]
cwd = os.getcwd()

tbl = open(sys.argv[2])

head = next(tbl)
job_list = []
for line in tbl:
    params = line.rstrip('\n').split('\t')
    (K, alpha, T) = params[0:3]
    wd = '_'.join((K, alpha, T))
    source_clust = cwd + '/' + wd + '.txt'
    perm_slist = cwd + '/permuted_samples_1000x.txt'
    perm_clist = cwd + '/permutation_res.txt'
    cmd = 'cd ' + cwd + '/' + wd + ';'
    cmd += km_survival_wrapper + ' ' + ' '.join((source_clust, r_script, perm_slist, perm_clist)) + ';'
    job_list.append(cmd)
job_manager(job_list, '8')
