import pandas

df = pandas.read_csv(r"raw_data\TCGA.BRCA.sampleMap_BRCA_clinicalMatrix", sep='\t')

subtype_column = df['PAM50Call_RNAseq']

filtered = df[subtype_column.isin(['LumA','Basal'])]

filtered.to_csv('output/cleaned_phenotype_data.csv', index = False)

