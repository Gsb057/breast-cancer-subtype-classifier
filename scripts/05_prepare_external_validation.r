library(HGNChelper)
library(styler)


exp_data <- readRDS("data_clean/GSE96058_expr_LumA_Basal.rds")
meta_data <- read.csv("data_clean/GSE96058_pheno_LumA_Basal.csv")

cleaned_meta_data <- meta_data[, c(1, 90)]

write.csv(cleaned_meta_data,
  "data_clean/ext_test_Y.csv",
  row.names = FALSE
)

exp_data <- as.data.frame(exp_data)
rownames(exp_data) <- exp_data[[1]]
r_exp_data <- exp_data[, -1]
transposed_exp <- as.data.frame(t(r_exp_data))

sig_genes <- read.csv("output/significant_genes.csv")
sig_gene <- sig_genes[, 1]

matching_genes <- sig_gene[sig_gene %in% colnames(transposed_exp)]

missing_genes <- sig_gene[!sig_gene %in% colnames(transposed_exp)]

outdated <- checkGeneSymbols(missing_genes)

validgenes <- outdated[!is.na(outdated$Suggested.Symbol), ]
matches <- validgenes$Suggested.Symbol %in% colnames(transposed_exp)

for (i in seq_len(nrow(validgenes))) {
  old_name <- validgenes$x[i]
  new_name <- validgenes$Suggested.Symbol[i]

  if (new_name %in% colnames(transposed_exp)) {
    colnames(transposed_exp)[
      colnames(transposed_exp) == new_name
    ] <- old_name
  }
}

matching_genes <- sig_gene[sig_gene %in% colnames(transposed_exp)]

missing_genes <- sig_gene[!sig_gene %in% colnames(transposed_exp)]

print(missing_genes)