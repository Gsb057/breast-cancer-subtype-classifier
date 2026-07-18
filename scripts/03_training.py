import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np

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

#Train base logistic regression model first.

l_r_model = LogisticRegression()
l_r_model.fit(exp_train, meta_train.values.ravel()) #values.ravel() strips the first column and changes 2d array to 1d

#let the model predict using test_x

prediction = l_r_model.predict(exp_test)

#prediction accuracy for normal logisticregression is 116/116. checked everything and no data leakage or any other problem, the training dataset is powerful.
'''list1 = np.array(prediction)
list2 = np.array(meta_test.values.ravel())

match = np.sum(list1 == list2)
mismatch = np.sum(list1 != list2)

print("correct predictions: ", match)
print("incorrect prediction: ", mismatch)

print("length: ",len(prediction))
print("length: ",len(meta_test))

comparison = meta_test.copy()
comparison["prediction"] = prediction

print(comparison)

print(meta_test.value_counts())

print(exp_test.index[:5])
print(meta_test.index[:5])

print(exp_train.shape)
print(exp_test.shape)'''

#Train balanced logistic regression model

bal_l_r_model = LogisticRegression(class_weight="balanced")
bal_l_r_model.fit(exp_train, meta_train.values.ravel())

bal_prediction = bal_l_r_model.predict(exp_test)

#prediction accuracy for balanced logisticregression is also 116/116. 
'''list1 = np.array(bal_prediction)
list2 = np.array(meta_test.values.ravel())

match = np.sum(list1 == list2)
mismatch = np.sum(list1 != list2)

print("Correct: ", match)
print("Incorrect: ", mismatch)'''

# Check the class encoding and number of learned gene weights.
# classes_ shows which subtype is treated as the positive class.
# coef_ contains one learned weight for each input gene.
'''print(l_r_model.classes_)
print(l_r_model.coef_.shape)
print(bal_l_r_model.coef_.shape)'''

# Extract and interpret the features learned by the Logistic Regression model.
# Logistic Regression assigns a coefficient (weight) to each gene.
# Since sklearn encoded LumA as the positive class, positive coefficients
# indicate genes that push predictions toward LumA, while negative coefficients
# push predictions toward Basal.
# The coefficients are matched with their corresponding gene names and sorted
# to identify the genes with the strongest influence on classification.

#Create a table connecting gene names with their learned coefficients.
coef_table = pandas.DataFrame({
    "Gene" : exp_train.columns,
    "Coef" : l_r_model.coef_[0]
})

#Rank genes based on their influence on classification.
ascending_coef = coef_table.sort_values("Coef", ascending= True)
descending_coef = coef_table.sort_values("Coef", ascending= False)

print("Top Basal-associated genes(normal_logistic_reg):")
print(ascending_coef.head())
print("Top LumA-associated genes(normal_logistic_reg):")
print(descending_coef.head())

# Repeat the coefficient extraction for the balanced Logistic Regression model
# to determine whether class weighting changes the learned gene importance.
bal_coef_table = pandas.DataFrame({
    "Gene": exp_train.columns,
    "Coef" : bal_l_r_model.coef_[0]
})

ascending_bal_coef = bal_coef_table.sort_values("Coef", ascending=True)
descending_bal_coef = bal_coef_table.sort_values("Coef", ascending=False)

print("Top Basal-associated genes(balanced_logistic_reg):")
print(ascending_bal_coef.head())
print("Top LumA-associated genes(balanced_logistic_reg):")
print(descending_bal_coef.head())

#creating confusion matrix for both normal and balanced logistic regression models.
normal_confusion_matrix = confusion_matrix(meta_test.values.ravel(), prediction)
balanced_confusion_matrix = confusion_matrix(meta_test.values.ravel(), bal_prediction)

print("Normal Logistic regression confusion matrix: ")
print(normal_confusion_matrix)
print("Balanced Logistic regression confusion matrix: ")
print(balanced_confusion_matrix)
print("l_r_model classes: ")
print(l_r_model.classes_)

#getting precision recall f1 score for both logistic model
normal_classification = classification_report(meta_test.values.ravel(), prediction)
balanced_classification = classification_report(meta_test.values.ravel(), bal_prediction)

print("Normal Logistic regression classification report: ")
print(normal_classification)
print("Balanced Logistic regression classification report: ")
print(balanced_classification)