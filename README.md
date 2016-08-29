# snf_robustinator
## Purpose:
Iterate over a standard SNF clustering algorithm permutating coulmn data per iteration to prove algorithm and result robustness
## Usage:
```
./scrambler.py {table to scramble} {number of iterations} {table to keep fixed} 2> log.txt
```
##Outputs:
####temp_eset2_permutated.txt: A temp file with permutated data that is overwritten each iteration
####permutation_res.txt: Table with cluster results of permutation.  First column indicates permutation number, the rest are the the cluster membership values.  With is to be used in conjunction with permutated_samples_{n}x.txt
####permuted_samples_{n}x.txt: Table with sample ordering for each iteration.
