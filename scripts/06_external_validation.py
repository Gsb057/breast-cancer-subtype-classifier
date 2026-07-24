import joblib
import pandas
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report, 
    roc_curve, auc, ConfusionMatrixDisplay, roc_auc_score
)

model = joblib.load('models/logistic_regression_model.pkl')

ext_test_x = pandas.read_csv("data_clean/matching_ext_test_x.csv", index_col= 0)
ext_test_x = ext_test_x[model.feature_names_in_]
ext_test_y = pandas.read_csv("data_clean/ext_test_Y.csv", index_col= 0)

prediction = model.predict(ext_test_x)

true_y = ext_test_y.iloc[:, 0]



print("--VALIDATION METRICS--")
print(f"Accuracy: {accuracy_score(true_y, prediction):.4f}\n")
print("Classification Report: ")
print(classification_report(true_y, prediction))
print("Confusion Matrix: ")
print(confusion_matrix(true_y, prediction))

y_probs = model.predict_proba(ext_test_x)[:, 1]

# Calculate and print AUC score
auc_score = roc_auc_score(true_y, y_probs)
print(f"ROC AUC Score: {auc_score:.4f}")

# 2. Calculate coordinates for the curve and the overall area
fpr, tpr, thresholds = roc_curve(
    true_y,
    y_probs,
    pos_label="LumA"
)
roc_auc = auc(fpr, tpr)

# 3. Plot the final graph
import matplotlib.pyplot as plt
plt.figure()
plt.plot(fpr, tpr, color='blue', label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='red', linestyle='--')  # Random guess line
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend()
plt.show()
