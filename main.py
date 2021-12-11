import datetime
import sys
import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.stats
import seaborn as sns
import math

from sklearn.linear_model import LogisticRegression
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, plot_confusion_matrix, accuracy_score
import seaborn as sns
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix

# #################################################################################
# analisis dataset original
# #################################################################################

org_dataset = pd.read_csv('data.csv', error_bad_lines=False)
org_dataset = org_dataset.dropna()

print(" ")
print("org_dataset.info()")
print(org_dataset.info())
print(" ")
print("org_dataset.describe()")
print(org_dataset.describe())
print(" ")
print("Contingut de les primeres mostres:")
print(org_dataset.head())
print(" ")
print("Dimensionalitat de la BBDD:", org_dataset.shape)
print(" ")

# #################################################################################
# borrat de les files amb un length major a 25
# #################################################################################

org_dataset['length'] = [len(i) for i in org_dataset['password']]

dataset = org_dataset.drop(org_dataset[org_dataset['length'] > 25].index)

# #################################################################################
# generacio de dades analisis del nou dataset
# #################################################################################

dataset['lower_freq'] = [len([j for j in i if j.islower()]) / len(i) for i in dataset['password']] #proporció de minusculas
dataset['upper_freq'] = [len([j for j in i if j.isupper()]) / len(i) for i in dataset['password']] #proporció de majusculas
dataset['alpha_freq'] = [len([j for j in i if j.isalpha()]) / len(i) for i in dataset['password']] #proporció de lletres
dataset['digit_freq'] = [len([j for j in i if j.isdigit()]) / len(i) for i in dataset['password']] #proporció de numeros
dataset['special_freq'] = [len([j for j in i if not j.isdigit() and not j.isalpha()]) / len(i) for i in dataset['password']] #proporció de caracters especials
dataset['lower'] = [len([j for j in i if j.islower()]) for i in dataset['password']] #minusculas
dataset['upper'] = [len([j for j in i if j.isupper()]) for i in dataset['password']] #majusculas
dataset['digit'] = [len([j for j in i if j.isdigit()]) for i in dataset['password']] #numeros
dataset['special'] = [len([j for j in i if not j.isdigit() and not j.isalpha()]) for i in dataset['password']] #caracters especials

print(" ")
print("dataset.info()")
print(dataset.info())
print(" ")
print("dataset.describe()")
print(dataset.describe())
print(" ")
print("Contingut de les primeres mostres:")
print(dataset.head())
print(" ")
print("Dimensionalitat de la BBDD:", dataset.shape)
print(" ")

df = dataset['strength'].value_counts().reset_index()
df.columns = ['value', 'count']
print("")
print("Balanç de les etiquetes: ")
print(df)
print("")

# #################################################################################
# correlació
# #################################################################################
"""
data = dataset.values

x = data[:, :7]
y = data[:, 7]

correlacio = dataset.corr()
plt.rcParams.update({'font.size': 3})
plt.rcParams.update({'figure.dpi': 200})
fig = plt.figure()
plt.title("Corelació")
plt.xticks(rotation=90)
plt.yticks(rotation=90)
ax = sns.heatmap(correlacio, annot=True, linewidths=.5)
plt.show()
"""
# #################################################################################
# normalització
# #################################################################################

dataset_copy = dataset.copy()
dataset_copy = dataset_copy.drop("password", axis="columns")

tmp = dataset_copy.drop("strength", axis="columns").values
col_names = dataset_copy.columns
scaler = MinMaxScaler()
tmp = scaler.fit_transform(tmp)

for i in range(1, 10):
    dataset_copy[col_names[i]] = tmp[:, i]

print("\ndataset.describe() un cop normalitzat:")
print(dataset_copy.describe())
print(dataset_copy.head())

# #################################################################################
# feature selection
# #################################################################################

dataset = dataset.drop("password", axis="columns")

dataset = dataset.drop("length", axis="columns")

dataset = dataset.drop("lower_freq", axis="columns")
dataset = dataset.drop("upper_freq", axis="columns")
dataset = dataset.drop("digit_freq", axis="columns")

dataset = dataset.drop("lower", axis="columns")
dataset = dataset.drop("upper", axis="columns")
dataset = dataset.drop("special", axis="columns")





print("Info de la base de dades després del preprocessing")
dataset.info()

X = dataset.drop("strength", axis="columns").values
y = dataset["strength"].to_numpy()
x_t, x_v, y_t, y_v = train_test_split(X, y, train_size=0.7)

# #################################################################################
# Logistic Regression
# #################################################################################

# multi_class="ovr"
C = 0.1
scores_array = []
plot_labels = []

print("\nLogistic regression multi_class=ovr accuracy score:")
for i in range(5):
    logireg = LogisticRegression(C=C, tol=0.001, multi_class="ovr", max_iter=10000)
    scores = cross_val_score(logireg, x_t, y_t, cv=5, scoring='accuracy')
    scores_array.append(scores.mean())
    plot_labels.append(str(C))
    print("[C=" + str(C) + "]: " + str(scores.mean()))
    C = C + 0.1

fig = plt.figure()
plt.rcParams.update({'font.size': 8})
plt.rcParams.update({'figure.dpi': 100})
plt.plot(plot_labels, scores_array)
plt.xticks(rotation=90)
plt.xlabel('C value')
plt.ylabel('Accuracy')
fig.suptitle('Cross-validation accuracy score per LOGISTIC REGRESSION\n amb multi_class=ovr')
plt.show()

# multi_class="multinomial"
C = 0.1
scores_array = []
plot_labels = []

print("\nLogistic regression multi_class=multinomial accuracy score:")
for i in range(5):
    logireg = LogisticRegression(C=C, tol=0.001, multi_class="multinomial", max_iter=10000)
    scores = cross_val_score(logireg, x_t, y_t, cv=5, scoring='accuracy')
    scores_array.append(scores.mean())
    plot_labels.append(str(C))
    print("[C=" + str(C) + "]: " + str(scores.mean()))
    C = C + 0.1

fig = plt.figure()
plt.plot(plot_labels, scores_array)
plt.xticks(rotation=90)
plt.xlabel('C value')
plt.ylabel('Accuracy')
fig.suptitle('Cross-validation accuracy score per LOGISTIC REGRESSION\n amb multi_class=multinomial')
plt.show()

"""

# #################################################################################
# SVM
# #################################################################################

# kernel='linear'
C = 0.1
scores_array = []
plot_labels = []

print("\nSVM kernel='linear' accuracy score:")
for i in range(5):
    svc = svm.SVC(C=C, kernel='linear', gamma='auto', probability=True)
    scores = cross_val_score(svc, x_t, y_t, cv=5, scoring='accuracy')
    scores_array.append(scores.mean())
    plot_labels.append(str(C))
    print("[C=" + str(C) + "]: " + str(scores.mean()))
    C = C + 0.1

fig = plt.figure()
plt.plot(plot_labels, scores_array)
plt.xticks(rotation=90)
plt.xlabel('C value')
plt.ylabel('Accuracy')
fig.subplots_adjust(bottom=0.3, right=None, top=None, wspace=None, hspace=None)
fig.suptitle('Cross-validation accuracy score per SVM amb kernel=linear')
plt.show()

# kernel='rbf'
C = 0.1
scores_array = []
plot_labels = []

print("\nSVM kernel='rbf' accuracy score:")
for i in range(5):
    svc = svm.SVC(C=C, kernel='rbf', gamma='auto', probability=True)
    scores = cross_val_score(svc, x_t, y_t, cv=5, scoring='accuracy')
    scores_array.append(scores.mean())
    plot_labels.append(str(C))
    print("[C=" + str(C) + "]: " + str(scores.mean()))
    C = C + 0.1

fig = plt.figure()
plt.plot(plot_labels, scores_array)
plt.xticks(rotation=90)
plt.xlabel('C value')
plt.ylabel('Accuracy')
fig.subplots_adjust(bottom=0.3, right=None, top=None, wspace=None, hspace=None)
fig.suptitle('Cross-validation accuracy score per SVM amb kernel=rbf')
plt.show()

C = 0.1
scores_array = []
plot_labels = []

# kernel='poly'
print("\nSVM kernel='poly' accuracy score:")
for i in range(5):
    svc = svm.SVC(C=C, kernel='poly', gamma='auto', probability=True)
    scores = cross_val_score(svc, x_t, y_t, cv=5, scoring='accuracy')
    scores_array.append(scores.mean())
    plot_labels.append(str(C))
    print("[C=" + str(C) + "]: " + str(scores.mean()))
    C = C + 0.1

fig = plt.figure()
plt.plot(plot_labels, scores_array)
plt.xticks(rotation=90)
plt.xlabel('C value')
plt.ylabel('Accuracy')
fig.subplots_adjust(bottom=0.3, right=None, top=None, wspace=None, hspace=None)
fig.suptitle('Cross-validation accuracy score per SVM amb kernel=poly')
plt.show()

# kernel='sigmoid'
C = 0.1
scores_array = []
plot_labels = []

print("\nSVM kernel='sigmoid' accuracy score:")
for i in range(5):
    svc = svm.SVC(C=C, kernel='sigmoid', gamma='auto', probability=True)
    scores = cross_val_score(svc, x_t, y_t, cv=5, scoring='accuracy')
    scores_array.append(scores.mean())
    plot_labels.append(str(C))
    print("[C=" + str(C) + "]: " + str(scores.mean()))
    C = C + 0.1

fig = plt.figure()
plt.plot(plot_labels, scores_array)
plt.xticks(rotation=90)
plt.xlabel('C value')
plt.ylabel('Accuracy')
fig.subplots_adjust(bottom=0.3, right=None, top=None, wspace=None, hspace=None)
fig.suptitle('Cross-validation accuracy score per SVM amb kernel=sigmoid')
plt.show()
"""
