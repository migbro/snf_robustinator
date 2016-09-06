#!/usr/bin/env python

import sys
import subprocess
import time


def date_time():
    cur_date = ">" + time.strftime("%c") + '\n'
    return cur_date


if len(sys.argv) < 5:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' {source cluster data}{km survival r script location}'
                                               '{permutated sample list}{permutated cluster list}\n')
    exit(1)
source_clust = open(sys.argv[1], 'r')
r_script = sys.argv[2]
perm_slist = open(sys.argv[3], 'r')
perm_clist = open(sys.argv[4], 'r')
head = next(source_clust)
head = head.rstrip('\n').split('\t')
info_dict = {}
sys.stderr.write(date_time() + 'Populating and initializing km survival')
for line in source_clust:
    data = line.rstrip('\n').split('\t')
    info_dict[data[0]] = {}
    for i in xrange(1, len(head), 1):
        info_dict[data[0]][head[i]] = data[i]
source_clust.close()

r_cmd = "Rscript " + r_script + ' ' + sys.argv[1] + ' 0'
check = subprocess.call(r_cmd, shell=True)
if check != 0:
    sys.stderr.write('Initializing failed\n' + r_cmd + '\n')
    exit(1)
sys.stderr.write(date_time() + ' Initial dataset complete, going through permutations\n')
m = 25
n = 1
for sample in perm_slist:
    if n % m == 0:
        sys.stderr.write(date_time() + 'On iteration ' + str(n) + '\n')
    s_data = sample.rstrip('\n').split('\t')
    clusters = next(perm_clist)
    c_data = clusters.rstrip('\n').split('\t')
    cur = open('temp_table.txt', 'w')
    cur.write('\t'.join(head) + '\n')
    for i in xrange(1, len(s_data), 1):
        pname = s_data[i]
        cur.write(pname + '\t' + c_data[i] + '\t' + info_dict[pname][head[2]] + '\t' + info_dict[pname][head[3]] + '\n')
    cur.close()
    r_cmd = "Rscript " + r_script + ' temp_table.txt ' + c_data[0]
    check = subprocess.call(r_cmd, shell=True)
    if check != 0:
        sys.stderr.write('Failed at iteration ' + str(n) + '\n' + r_cmd + '\n')
        exit(1)
    n += 1
perm_clist.close()
perm_slist.close()
sys.stderr.write(date_time() + 'P-value tabulation of permutation results completed\n')
