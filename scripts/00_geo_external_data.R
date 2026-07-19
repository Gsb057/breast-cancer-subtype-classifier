library(GEOquery)
library(data.table)

# --- Step 1: Get phenotype data from GEO ---
gse <- getGEO("GSE96058", GSEMatrix = TRUE)

pheno1 <- pData(gse[[1]])
pheno2 <- pData(gse[[2]])
pheno_all <- rbind(pheno1, pheno2)

cat("Total samples in pheno_all:", nrow(pheno_all), "\n")
print(table(pheno_all$`pam50 subtype:ch1`))

# --- Step 2: Filter to LumA + Basal ---
keep <- pheno_all$`pam50 subtype:ch1` %in% c("LumA", "Basal")
pheno_filtered <- pheno_all[keep, ]
sample_ids <- pheno_filtered$title

cat("Filtered samples:", length(sample_ids), "\n")
print(table(pheno_filtered$`pam50 subtype:ch1`))

# --- Step 3: Peek at expression file header ---
expr_path <- "C:/Users/sathy/Downloads/GSE96058_gene_expression_3273_samples_and_136_replicates_transformed.csv.gz"

header <- fread(expr_path, nrows = 0)
cat("First 5 columns of expression file:\n")
print(colnames(header)[1:5])

# --- Step 4: Save checkpoint so we don't have to redo GEO steps ---
save.image("checkpoint.RData")
cat("Checkpoint saved.\n")

# --- Step 5: Filter big expression file to only LumA/Basal samples ---
cols_to_keep <- c("V1", sample_ids)

cat("Reading filtered expression matrix... this may take a while.\n")
expr_filtered <- fread(expr_path, select = cols_to_keep)

cat("Filtered expression matrix dimensions:\n")
print(dim(expr_filtered))

# --- Step 6: Save filtered outputs ---
dir.create("data_clean", showWarnings = FALSE)

fwrite(expr_filtered, "data_clean/GSE96058_expr_LumA_Basal.csv")
write.csv(pheno_filtered, "data_clean/GSE96058_pheno_LumA_Basal.csv", row.names = FALSE)

cat("Saved filtered expression + phenotype files to data_clean/\n")

save.image("checkpoint.RData")
cat("Checkpoint updated.\n")