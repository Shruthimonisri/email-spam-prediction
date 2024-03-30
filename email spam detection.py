# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NnqhkERFmpbwtkkB-XXP7a324-iW93sm
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

import warnings
warnings.filterwarnings('ignore')

# importing Stopwords
import nltk
from nltk.corpus import stopwords
import string

# models
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# train test split
from sklearn.model_selection import train_test_split, GridSearchCV
# Pipeline
from sklearn.pipeline import Pipeline

# score
from sklearn.metrics import confusion_matrix,classification_report,ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

from google.colab import files
uploaded = files.upload()

pip install chardet

import io
import chardet

# Assuming uploaded is a dictionary containing the uploaded file
rawdata = uploaded['spam.csv']
result = chardet.detect(rawdata)
encoding = result['encoding']

df = pd.read_csv(io.BytesIO(rawdata), encoding=encoding)
print(df)

df.head()

df.describe()

df['v1'].value_counts()

df.info()

df['length'] = df['v2'].apply(len)
df.head()

# plot for count of spam and ham in data
plt.figure(figsize=(14,6))
sns.set_style('darkgrid')
sns.countplot(x='v1',data=df)
plt.title('Number of Spam and Ham')

# Plot for distribution lenth of text
plt.figure(figsize=(12,8))
sns.histplot(x='length',data=df,bins=100)
plt.title('Length of Text')

df[df['length']==df['length'].max()]['v2']

df.hist(column='length',by='v1',figsize=(12,8))

import nltk
nltk.download('stopwords')

# function to remove punctuation and stopwords
def text_process(v2):
    non_punc = [char for char in v2 if char not in string.punctuation]
    non_punc=''.join(non_punc)
    return [word for word in non_punc.split() if word not in stopwords.words('english')]

# define X(features),y(target)
X= df['v2']
y=df['v1']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# creating a pipline to model the data
# pipeline for MultinomialNB
pipe_mnb = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tf',TfidfTransformer()),
    ('classifier',MultinomialNB())
])
# pipeline for Random Forest Classifier
pipe_rf =Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tf',TfidfTransformer()),
    ('classifier',RandomForestClassifier())
])

# pipeline for Random Forest Classifier
pipe_svc =Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tf',TfidfTransformer()),
    ('classifier',SVC())
])

# fit the data
pipe_mnb.fit(X_train,y_train)
pipe_rf.fit(X_train,y_train)
pipe_svc.fit(X_train,y_train)

# predict the target feature
pred_mnb = pipe_mnb.predict(X_test)
pred_rf = pipe_rf.predict(X_test)
pred_svc = pipe_svc.predict(X_test)

print('The accuracy for Multinomial Classifer:',accuracy_score(y_test,pred_mnb)*100)
print('The accuracy for Random_forest Classifer:',accuracy_score(y_test,pred_rf)*100)
print('The accuracy for SVC:',accuracy_score(y_test,pred_svc)*100)

# print confusion matrix and classification report
print ('Classification report on SVC:')
print('\n')
print(classification_report(y_test,pred_svc))

# Display confusioni matrix for SVC

sns.set_style('ticks')
ConfusionMatrixDisplay(confusion_matrix(y_test,pred_svc)).plot()
plt.title("Confusion Matrix for SVC")

from sklearn.model_selection import cross_val_score

# Number of folds
k = 5

# Initialize the SVC model in the pipeline
pipe_svc.set_params(classifier=SVC())

# Perform k-fold cross-validation
cv_scores = cross_val_score(pipe_svc, X, y, cv=k)

# Output the results
print(f'CV Scores for each fold: {cv_scores}')
print(f'Average CV Score: {np.mean(cv_scores)}')