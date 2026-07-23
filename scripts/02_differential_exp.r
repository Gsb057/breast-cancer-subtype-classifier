library(limma)

exp_df <- read.csv("output/train_X.csv")
meta_data <- read.csv("output/train_y.csv")

#change the first column to rownames and remove the duplicate first column
rownames(exp_df) <- exp_df[, 1]
exp_df <- exp_df[, -1]

gene_map <- read.csv("output/gene_symbol_map.csv")

for (i in seq_len(nrow(gene_map))){
  old_name <- gene_map$x[i]
  new_name <- gene_map$Suggested.Symbol[i]

  if (old_name %in% colnames(exp_df)) {
    colnames(exp_df)[
      colnames(exp_df) == old_name
    ] <- new_name
  }
}

print("CCDC170" %in% colnames(exp_df))
print("C6orf97" %in% colnames(exp_df))
#transpose the expression data.
transposed_exp <- as.data.frame(t(exp_df))

#change the first column to rownames
rownames(meta_data) <- meta_data[, 1]
meta_data <- meta_data[, -1, drop = FALSE]

#set the reference to LumA, and set the column as factor.
meta_data$PAM50Call_RNAseq <- relevel(factor(meta_data$PAM50Call_RNAseq)
                                      , ref = "LumA")

#build the design matrix for meta_data.
design_matrix_meta <- model.matrix(~ ., data = meta_data)

#checked weather the column names from transposed exp match row names in design matrix # nolint
#print(colnames(transposed_exp) == rownames(design_matrix_meta)) #nolint

fit <- lmFit(transposed_exp, design_matrix_meta)
fit <- eBayes(fit)
result <- topTable(
  fit,
  coef = 2,
  number = Inf,
  p.value = 1,
  lfc = 0
)

#filter genes based on creteria using base r.

sig_genes <- result[which(result$adj.P.Val < 0.05 & abs(result$logFC) > 1), ]

write.csv(sig_genes,
          file = "output/significant_genes.csv",
          row.names = TRUE)

#get the gene names and filter trainx and testx

test_exp <- read.csv("output/test_X.csv")

rownames(test_exp) <- test_exp[, 1]
test_exp <- test_exp[, -1]

for (i in seq_len(nrow(gene_map))){
  old_name <- gene_map$x[i]
  new_name <- gene_map$Suggested.Symbol[i]

  if (old_name %in% colnames(test_exp)) {
    colnames(test_exp)[
      colnames(test_exp) == old_name
    ] <- new_name
  }
}

print("CCDC170" %in% colnames(test_exp))
print("C6orf97" %in% colnames(test_exp))

filtered_trainx <- exp_df[, colnames(exp_df) %in% rownames(sig_genes),
                          drop = FALSE]
filtered_testx <- test_exp[, colnames(test_exp) %in% rownames(sig_genes),
                           drop = FALSE]

#save the trainx and testx filtered csv.

write.csv(filtered_trainx,
          file = "output/filtered_train_x.csv",
          row.names = TRUE)
write.csv(filtered_testx,
          file = "output/filtered_test_x.csv",
          row.names = TRUE)

print(ncol(filtered_trainx))
print(ncol(filtered_testx))

print(identical(
    colnames(filtered_trainx),
    colnames(filtered_testx)
))