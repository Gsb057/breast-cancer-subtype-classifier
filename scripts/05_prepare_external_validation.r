
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

train_x <- read.csv("output/filtered_train_x.csv")
test_x <- read.csv("output/filtered_test_x.csv")

rownames(train_x) <- train_x[, 1]
train_x <- train_x[, -1]

rownames(test_x) <- test_x[, 1]
test_x <- test_x[, -1]

matching_train_x <- train_x[, colnames(train_x) %in% matching_genes]
matching_test_x <- test_x[, colnames(test_x) %in% matching_genes]

write.csv(
  matching_train_x,
  "output/matching_train_x.csv",
  row.names = FALSE
)
write.csv(
  matching_test_x,
  "output/matching_test_x.csv",
  row.names = FALSE
)

matching_ext_test_x <- transposed_exp[, matching_genes, drop = FALSE]

matching_ext_test_x <- matching_ext_test_x[
    ,
    colnames(matching_train_x),
    drop = FALSE
]

write.csv(
  matching_ext_test_x,
  "data_clean/matching_ext_test_x.csv",
  row.names = TRUE
)

print(ncol(matching_train_x))
print(ncol(matching_test_x))
print(ncol(matching_ext_test_x))

print(identical(
    colnames(matching_train_x),
    colnames(matching_test_x)
))

print(identical(
    colnames(matching_train_x),
    colnames(matching_ext_test_x)
))