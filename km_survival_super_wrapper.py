#!/usr/bin/env python

import os
from job_manager import job_manager
from km_survival_wrapper import *

if len(sys.argv) < 5:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' {km survival r script location}'
                                               '{permutated sample list}{permutated cluster list}{SNF param table}\n')
    exit(1)
km_survival_wrapper = '/home/ubuntu/TOOLS/snf_robustinator/km_survival_wrapper.py'
r_script = sys.argv[1]
cwd = os.getcwd()
perm_slist = cwd + '/' + sys.argv[2]
perm_clist = cwd + '/' + sys.argv[3]
tbl = open(sys.argv[4])

head = next(tbl)
job_list = []
for line in tbl:
    params = line.rstrip('\n').split('\t')
    (K, alpha, T) = params[1:3]
    wd = '_'.join((K, alpha, T))
    source_clust = cwd + '/' + wd + '.txt'
    cmd = 'cd ' + cwd + '; mkdir ' + wd + ';cd ' + wd + ';'
    cmd += km_survival_wrapper + ' ' + ' '.join((source_clust, r_script, perm_slist, perm_clist, K, alpha, T)) + ';'
    job_list.append(cmd)
job_manager(job_list, '8')
