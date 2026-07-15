library(limma)

exp_df <- read.csv("output/train_X.csv")
meta_data <- read.csv("output/train_y.csv")

#change the first column to rownames and remove the duplicate first column
rownames(exp_df) <- exp_df[, 1]
exp_df <- exp_df[, -1]

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