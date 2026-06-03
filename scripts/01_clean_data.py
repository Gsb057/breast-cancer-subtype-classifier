import pandas

raw_phenotype_file = pandas.read_csv(r"raw_data\TCGA.BRCA.sampleMap_BRCA_clinicalMatrix", sep='\t')
subtype_column = raw_phenotype_file['PAM50Call_RNAseq']
filtered = raw_phenotype_file[subtype_column.isin(['LumA','Basal'])]
filtered.to_csv('output/cleaned_phenotype_data.csv', index = False)

raw_expression_file = pandas.read_csv(r"raw_data\HiSeqV2", sep='\t')
patient_id_raw = raw_expression_file.columns
patient_id_phenotype = filtered['sampleID']
intersecting_patient_ids = list(set(patient_id_raw).intersection(set(patient_id_phenotype)))
intersecting_patient_ids.insert(0,"sample")
filtered_exp_file = raw_expression_file[intersecting_patient_ids]
filtered_exp_file.to_csv('output/cleaned_expression_data.csv', index=False)

print(filtered_exp_file.shape)