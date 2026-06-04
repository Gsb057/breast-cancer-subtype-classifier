import pandas

#filtering phenotype files to LumA and Basal subtypes only:
raw_phenotype_file = pandas.read_csv(r"raw_data\TCGA.BRCA.sampleMap_BRCA_clinicalMatrix", sep='\t')
subtype_column = raw_phenotype_file['PAM50Call_RNAseq']
filtered = raw_phenotype_file[subtype_column.isin(['LumA','Basal'])]
filtered.to_csv('output/cleaned_phenotype_data.csv', index = False)

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

filtered_exp_file.to_csv('output/cleaned_expression_data.csv', index=False)
