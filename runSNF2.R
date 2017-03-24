##------------------------------------------------
## Similarity Network Fusion Clustering Analysis
## Date: 08/05/2016
##------------------------------------------------


##------------------------------------------------
## readEset(fn) - read expression matrix
## Input: expression matrix file name
## Output: expression matrix w/ rows are genes/mirs
##         and cols are matched samples
##------------------------------------------------
readEset <- function(fn){
    eset <- read_tsv(fn) %>% as.data.frame()
    rownames(eset) <- eset$ID
    return(eset[,-1])
}

##------------------------------------------------
## runSNF(M1, M2, ...) - SNF clustering
## Input: matrice with matched samples
## Output: a numeric vector of cluster memberships,
##         where names of the vector are the sample IDs
##------------------------------------------------
runSNF <- function(M1, M2, K, alpha, T) {
    # Check if the sample IDs are matched in both matrices!")
    stopifnot(identical(colnames(M1), colnames(M2)))
    ## transpose data matrix to allow the rows are samples 
    ## and columns are genes/mirnas
    eset1 <- t(M1)
    eset2 <- t(M2)
    ## SNF parameters given as args
    # K = 20;  	# number of neighbors, usually (10~30)
    # alpha = 0.5;  	# hyperparameter, usually (0.3~0.8)
    # T = 20; 	# Number of Iterations, usually (10~20)
    ## normalize the input matrix
    dat1 <- standardNormalization(eset1)
    dat2 <- standardNormalization(eset2)

    D1 <- SNFtool::dist2(dat1, dat1)
    D2 <- SNFtool::dist2(dat2, dat2)
    
    W1 <- affinityMatrix(D1, K, alpha)
    W2 <- affinityMatrix(D2, K, alpha)
    
    W <- SNF(list(W1, W2), K, T)
    colnames(W) <- rownames(eset1)
    rownames(W) <- rownames(eset1)
    ## spectral clustering and cluster memberships
    ## fix the optimal number of clusters
    C <- 3
    group <- spectralClustering(W, C)
    names(group) <- rownames(eset1)
    return(group)
}

##----------------------
## main
##----------------------

packages <- c("readr", "dplyr", "SNFtool")
if (length(setdiff(packages, rownames(installed.packages()))) > 0) {
    install.packages(setdiff(packages, rownames(installed.packages())))
}

suppressPackageStartupMessages({
    library(readr)
    library(dplyr)
    library(SNFtool)
})

## the above functions can be saved in another R script
## and source to the current R session, e.g.
## source("foo.R")
args <- commandArgs(TRUE)
eset1 = args[1]
eset2 = args[2]
out = args[3]
i = args[4]
K = as.numeric(args[5])
alpha = as.numeric(args[6])
T = as.numeric(args[7])
eset.mrna <- readEset(eset1)
eset.mir <- readEset(eset2)

group <- runSNF(eset.mrna, eset.mir, K, alpha, T)
g_as_string = toString(group)
g_as_string = gsub(", ", "\t", g_as_string)
g_as_string = paste(i, g_as_string, sep="\t")
write(g_as_string, file=out,  append=TRUE)

