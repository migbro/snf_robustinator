suppressPackageStartupMessages({
    library(survival)
})
args <- commandArgs(TRUE)

km_test <- read.delim(args[1], quote="")
km_i = args[2]
km_test$SurvObj <- with(km_test, Surv(time=km_test$censor, km_test$death == 1, type="right"))
survdiff(formula = km_test$SurvObj ~ km_test$snf_clust)
result = survdiff(formula = km_test$SurvObj ~ km_test$snf_clust)
pval = pchisq(result$chisq, length(result$n)-1, lower.tail = FALSE)
work = paste("km_iter_", km_i, "_workspace.Rdata", sep="")
out_fn = "KM_pvals.txt"
out_res = paste(km_i, toString(pval), sep="\t")
write(out_res, file=out_fn,  append=TRUE)
save.image(file=work)
