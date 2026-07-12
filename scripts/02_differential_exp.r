library(limma)

exp_df <- read.csv("output/train_X.csv")
meta_data <- read.csv("output/train_y.csv")

rownames(exp_df) <- exp_df[, 1]
exp_df <- exp_df[, -1]

