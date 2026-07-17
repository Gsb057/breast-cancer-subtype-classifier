import pandas

#read the files needed and store them in variables.
exp_train = pandas.read_csv("output/filtered_train_x.csv", index_col= 0)
exp_test = pandas.read_csv("output/filtered_test_x.csv", index_col= 0)

meta_train = pandas.read_csv("output/train_y.csv", index_col= 0)
meta_test = pandas.read_csv("output/test_y.csv", index_col= 0)

#verify the loaded dataframes.
'''
print(exp_test.head())
print(exp_train.head())
print(meta_test.head())
print(meta_train.head())
'''
#alignment check
'''
alignment_check_train = exp_train.index.equals(meta_train.index)
alignment_check_test = exp_test.index.equals(meta_test.index)
print(alignment_check_test)
print(alignment_check_train)
'''
