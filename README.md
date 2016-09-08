# snf_robustinator
## Purpose:
Iterate over a standard SNF clustering algorithm permutating column data per iteration to prove algorithm and result robustness
## Usage for permutations:
```
./scrambler.py {table to scramble} {number of iterations} {table to keep fixed} { R script location} 2> log.txt
```
##Outputs:
####temp_eset2_permutated.txt: A temp file with permutated data that is overwritten each iteration
####permutation_res.txt: Table with cluster results of permutation.  First column indicates permutation number, the rest are the the cluster membership values.  With is to be used in conjunction with permutated_samples_{n}x.txt
####permuted_samples_{n}x.txt: Table with sample ordering for each iteration.

#####Note: R script written by Lei Huang from CRI, modified y M Brown

## Usage for K-M Survival fitness p values:
```
./km_survival_wrapper.py {source cluster data}{km survival r script location} {permutated sample list}{permutated cluster list} 2> log.txt
```

##Outputs:
####KM_pvals.txt tab seprated text file, with first column being the iteration number, second the p value.  Iteration 0 is the empircal data.
