import pandas

#filtering phenotype files to LumA and Basal subtypes only:
raw_phenotype_file = pandas.read_csv(r"raw_data\TCGA.BRCA.sampleMap_BRCA_clinicalMatrix", sep='\t')
subtype_column = raw_phenotype_file['PAM50Call_RNAseq']
filtered = raw_phenotype_file[subtype_column.isin(['LumA','Basal'])]

#match patients id across both files:
raw_expression_file = pandas.read_csv(r"raw_data\HiSeqV2", sep='\t')
patient_id_raw = raw_expression_file.columns
patient_id_phenotype = filtered['sampleID']
intersecting_patient_ids = list(set(patient_id_raw).intersection(set(patient_id_phenotype)))
intersecting_patient_ids.insert(0,"sample")
filtered_exp_file = raw_expression_file[intersecting_patient_ids]

#removing genes where >20% of values are zeros:
gene_zero_count = (filtered_exp_file==0).sum(axis = 1)
filtered_exp_file = filtered_exp_file[gene_zero_count <= 115]

#finding duplicate genes, and among dupes keeping the genes with high expression only:
'''
duplicate_genes = filtered_exp_file.duplicated(subset='sample', keep= False).sum()
print(duplicate_genes)
'''

#transposing the expression file cause machine learning needs it that way.
transposed_exp_file = filtered_exp_file.set_index('sample').T

#reordering the phenotype file to match the gene expression file.
filtered = filtered.set_index('sampleID')
filtered = filtered.reindex(transposed_exp_file.index)

transposed_exp_file.to_csv('output/cleaned_expression_data.csv')
filtered.to_csv('output/cleaned_phenotype_data.csv')

#splittning train/test data 80/20:
from sklearn.model_selection import train_test_split

X = transposed_exp_file
y = filtered['PAM50Call_RNAseq']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42, stratify= y)

X_train.to_csv('output/train_X.csv')
X_test.to_csv('output/test_X.csv')
y_train.to_csv('output/train_y.csv')
y_test.to_csv('output/test_y.csv')

