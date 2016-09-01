
snf_death_censor_RNAseq_results$SurvObj <- with(snf_death_censor_RNAseq_results, Surv(time=snf_death_censor_RNAseq_results$Follow.up.Time.or.Time.to.Death..y., snf_death_censor_RNAseq_results$Death..Yes.1. == 1, type="right"))
km.by.snf <- survfit(SurvObj ~ SNF.group, data = snf_death_censor_RNAseq_results, conf.type="log-log"
km_test$SurvObj <- with(km_test, Surv(time=km_test$censor, km_test$death == 1, type="right"))
test.by.snf <- survfit(SurvObj ~ snf_clust, data = km_test, conf.type="log-log")
survdiff(formula = snf_death_censor_RNAseq_results$SurvObj ~ snf_death_censor_RNAseq_results$SNF.group)
survdiff(formula = km_test$SurvObj ~ km_test$snf_clust)
result = survdiff(formula = km_test$SurvObj ~ km_test$snf_clust)
pchisq(result$chisq, length(result$n)-1, lower.tail = FALSE)