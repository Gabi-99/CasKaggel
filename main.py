import datetime
import sys
import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.stats
import seaborn as sns
import math

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA

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

data = dataset.values

x = data[:, :7]
y = data[:, 7]

correlacio = dataset.corr()
fig = plt.figure()
plt.title("Corelació")
fig.subplots_adjust(left=0.15, bottom=0.2, right=None, top=None, wspace=None, hspace=None)
ax = sns.heatmap(correlacio, annot=True, linewidths=.5)
plt.show()

# #################################################################################
# normalització
# #################################################################################

dataset_copy = dataset.copy()
dataset_copy = dataset_copy.drop("password", axis="columns")

tmp = dataset_copy.drop("strength", axis="columns").values
col_names = dataset_copy.columns
scaler = MinMaxScaler()
tmp = scaler.fit_transform(tmp)

for i in range(1, 6):
    dataset_copy[col_names[i]] = tmp[:, i]

print("\ndataset.describe() un cop normalitzat:")
print(dataset_copy.describe())
print(dataset_copy.head())

# #################################################################################
# feature selection
# #################################################################################

dataset = dataset.drop("password", axis="columns")
dataset = dataset.drop("lower_freq", axis="columns")
dataset = dataset.drop("digit_freq", axis="columns")

print("Info de la base de dades després del preprocessing")
dataset.info()
