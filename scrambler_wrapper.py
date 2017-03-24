#!/usr/bin/env python

import sys
import os
from job_manager import job_manager


if len(sys.argv) < 5:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' {r script }{table to permute} {iterations} {table to not permute} '
                                               '{SNF param table}\n')
    exit(1)
scramble = '/home/ubuntu/TOOLS/snf_robustinator/scrambler.py'
r_script = sys.argv[1]
cwd = os.getcwd()
eset2 = cwd + '/' + sys.argv[2]
num_iterations = sys.argv[3]
eset1 = cwd + '/' + sys.argv[4]
tbl = open(sys.argv[5])

head = next(tbl)
job_list = []
for line in tbl:
    params = line.rstrip('\n').split('\t')
    (K, alpha, T) = params[0:3]
    wd = '_'.join((K, alpha, T))

    cmd = 'cd ' + cwd + '; mkdir ' + wd + ';cd ' + wd + ';'
    cmd += scramble + ' ' + ' '.join((eset2, num_iterations, eset1, r_script, K, alpha, T)) + ';'
    job_list.append(cmd)
job_manager(job_list, '8')
