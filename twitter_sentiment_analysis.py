# -*- coding: utf-8 -*-
"""Twitter Sentiment Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/142100nUecXQrMEbCmrHPgt6vDZwee2OV

# **Import Modules**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
import nltk
import warnings
# %matplotlib inline

warnings.filterwarnings('ignore')

"""# **Loading the Dataset**"""

!wget -O HindenBerg_Report.csv "https://www.dropbox.com/scl/fi/g445ntavlys2pwvclt39s/HindenBerg_Report.csv?rlkey=uxalbnmr6izvt8sh45ixtdeq8&dl=0"
data = pd.read_csv('HindenBerg_Report.csv')
data.head()

# datatype info
data.info()

"""# **Preprocessing the Dataset**

**Removing pattern in input text**
"""

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for word in r:
        input_txt = re.sub(word, "", input_txt)
    return input_txt
data.head()

"""**Removing twitter handles**"""

def remove_twitter_handles(text):
    pattern = r'@[A-Za-z0-9_]+'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text
df = pd.DataFrame(data)
df['Clean_Tweets'] = df['Tweets'].apply(remove_twitter_handles)
df.head()

"""**Removing special characters, numbers and punctuations**"""

data['Clean_Tweets'] = data['Clean_Tweets'].str.replace("[^a-zA-Z#]", " ")
data.head()

"""**Removing the stopwords**"""

!pip install nltk

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text)
data['Clean_Tweets'] = data['Clean_Tweets'].apply(remove_stopwords)
data.head()

"""**Removing short words**"""

data['Clean_Tweets'] = data['Clean_Tweets'].apply(lambda x: " ".join([w for w in x.split() if len(w)>3]))
data.head()

"""**Taking individual words as tokens**"""

Tokenized_Tweets = data['Clean_Tweets'].apply(lambda x: x.split())
Tokenized_Tweets.head()

"""**Lemmatizing the words**"""

from nltk.stem import WordNetLemmatizer

import nltk
nltk.download('wordnet')

lm = nltk.WordNetLemmatizer()
def lemmatizer_on_text(data):
    text = [lm.lemmatize(word) for word in data]
    return data
Tokenized_Tweets= Tokenized_Tweets.apply(lambda x: lemmatizer_on_text(x))
Tokenized_Tweets.head()

"""**Combining words into single sentence**"""

for i in range(len(Tokenized_Tweets)):
    Tokenized_Tweets[i] = " ".join(Tokenized_Tweets[i])
data['Clean_Tweets'] = Tokenized_Tweets

from PIL import Image
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

import nltk
nltk.download('vader_lexicon')

for index, row in data['Clean_Tweets'].iteritems():
	score = SentimentIntensityAnalyzer().polarity_scores(row)
	neg = score['neg']
	neu = score['neu']
	pos = score['pos']
	comp = score['compound']

	if neg > pos:
		data.loc[index, 'sentiment'] = "negative"
	elif pos > neg:
		data.loc[index, 'sentiment'] = "positive"
	else:
		data.loc[index, 'sentiment'] = "neutral"

	data.loc[index, 'neg'] = neg
	data.loc[index, 'neu'] = neu
	data.loc[index, 'pos'] = pos
	data.loc[index, 'compound'] = comp

total_pos = len(data.loc[data['sentiment'] == "positive"])
total_neg = len(data.loc[data['sentiment'] == "negative"])
total_neu = len(data.loc[data['sentiment'] == "neutral"])
total_tweets = len(data)
print("Total Positive Tweets % : {:.2f}"
	.format((total_pos/total_tweets)*100))
print("Total Negative Tweets % : {:.2f}"
	.format((total_neg/total_tweets)*100))
print("Total Neutral Tweets % : {:.2f}"
	.format((total_neu/total_tweets)*100))

mylabels = ["Positive", "Negative", "Neutral"]
mycolors = ["Green", "Red", "Blue"]

plt.figure(figsize=(5,3),
		dpi=100) # Push new figure on stack
myexplode = [0, 0.2, 0]
plt.pie([total_pos, total_neg, total_neu], colors=mycolors,
		labels=mylabels, explode=myexplode)
plt.show()

from wordcloud import WordCloud

data_plt = data['Clean_Tweets'][:1002]
plt.figure(figsize = (10,10))
wc = WordCloud(max_words = 500, width = 1200 , height = 600,
               collocations=False).generate(" ".join(data_plt))
plt.imshow(wc)

from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report

from sklearn import preprocessing
le=preprocessing.LabelEncoder()
data['sentiment']=le.fit_transform(data['sentiment'])

text, sentiment = list(data['Clean_Tweets']), list(data['sentiment'])
df=data[['Clean_Tweets','sentiment']]

data['Clean_Tweets']

df.head()

X=df['Clean_Tweets']
y=df['sentiment']

import nltk
nltk.download('averaged_perceptron_tagger')

# Separating the 95% data for training data and 5% for testing data
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.05, random_state =26)

!pip install textaugment

from textaugment import Wordnet
import random

aug = Wordnet()

def augment_text(text):
    return aug.augment(text)

augmented_data = [augment_text(text) for text in X_train]

from sklearn.feature_extraction.text import CountVectorizer

# Applying Countvectorizer
countVectorizer = CountVectorizer()
countVector = countVectorizer.fit_transform(data["Clean_Tweets"])
count_vect_df = pd.DataFrame(
	countVector.toarray(),
columns=countVectorizer.get_feature_names_out())
count_vect_df.head()

# Most Used Words
count = pd.DataFrame(count_vect_df.sum())
countdf = count.sort_values(0,
							ascending=False).head(20)
countdf[1:11]

count = pd.DataFrame(count_vect_df.sum())
countdf = count.sort_values(0,
							ascending=False).head(175)
countdf

countVectorizer = CountVectorizer(ngram_range=(1,1),max_features=170)
countVectorizer.fit(X_train)
X_train1= countVectorizer.transform(X_train)
X_test1= countVectorizer.transform(X_test)

def model_Evaluate(model):
  # Predict values for Test dataset
  y_pred = model.predict(X_test1)
  # Print the evaluation metrics for the dataset.
  print(classification_report(y_test, y_pred))
  # Compute and plot the Confusion matrix
  cf_matrix = confusion_matrix(y_test, y_pred)
  categories = ['Negative','Positive']
  group_names = ['True Neg','False Pos', 'False Neg','True Pos']
  group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)]
  labels = [f'{v1}n{v2}' for v1, v2 in zip(group_names,group_percentages)]
  labels = np.asarray(labels).reshape(2,2)
  sns.heatmap(cf_matrix,annot = True, cmap = 'Blues',fmt = '',
  xticklabels = categories, yticklabels = categories)
  plt.xlabel("Predicted values", fontdict = {'size':14}, labelpad = 10)
  plt.ylabel("Actual values" , fontdict = {'size':14}, labelpad = 10)
  plt.title ("Confusion Matrix", fontdict = {'size':18}, pad = 20)

model = BernoulliNB()
model.fit(X_train1, y_train)
y_pred =model.predict(X_test1)
model_Evaluate(model)

model.score(X_test1,y_test)

model.score(X_train1,y_train)

from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
accuracy=accuracy_score(y_test,y_pred)
precision =precision_score(y_test,y_pred,average='weighted')
recall= recall_score(y_test,y_pred,average='weighted')
f1=f1_score(y_test,y_pred,average='weighted')
accuracy,precision,f1,recall

SVCmodel = LinearSVC()
SVCmodel.fit(X_train1, y_train)
model_Evaluate(SVCmodel)
y_pred2 = SVCmodel.predict(X_test1)

from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
accuracy=accuracy_score(y_test,y_pred2)
precision =precision_score(y_test,y_pred2,average='weighted')
recall= recall_score(y_test,y_pred2,average='weighted')
f1=f1_score(y_test,y_pred2,average='weighted')
accuracy,precision,recall,f1

SVCmodel.score(X_test1,y_test)

SVCmodel.score(X_train1,y_train)

LRmodel = LogisticRegression(C = 2, max_iter = 1000, n_jobs=-1)
LRmodel.fit(X_train1, y_train)
model_Evaluate(LRmodel)
y_pred3 = LRmodel.predict(X_test1)

from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
accuracy=accuracy_score(y_test,y_pred3)
precision =precision_score(y_test,y_pred3,average='weighted')
recall= recall_score(y_test,y_pred3,average='weighted')
f1=f1_score(y_test,y_pred3,average='weighted')
accuracy,precision,recall,f1

LRmodel.score(X_test1,y_test)

LRmodel.score(X_train1,y_train)

#Transforming the Dataset Using TF-IDF Vectorizer
vectoriser = TfidfVectorizer(ngram_range=(1,2), max_features=170)
vectoriser.fit(X_train)

X_train2=vectoriser.transform(X_train)
X_test2=vectoriser.transform(X_test)

def model_Evaluate(model):
  # Predict values for Test dataset
  y_pred = model.predict(X_test2)
  # Print the evaluation metrics for the dataset.
  print(classification_report(y_test, y_pred))
  # Compute and plot the Confusion matrix
  cf_matrix = confusion_matrix(y_test, y_pred)
  categories = ['Negative','Positive']
  group_names = ['True Neg','False Pos', 'False Neg','True Pos']
  group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)]
  labels = [f'{v1}n{v2}' for v1, v2 in zip(group_names,group_percentages)]
  labels = np.asarray(labels).reshape(2,2)
  sns.heatmap(cf_matrix,annot = True, cmap = 'Blues',fmt = '',
  xticklabels = categories, yticklabels = categories)
  plt.xlabel("Predicted values", fontdict = {'size':14}, labelpad = 10)
  plt.ylabel("Actual values" , fontdict = {'size':14}, labelpad = 10)
  plt.title ("Confusion Matrix", fontdict = {'size':18}, pad = 20)

model = BernoulliNB()
model.fit(X_train2, y_train)
y_pred4 =model.predict(X_test2)
model_Evaluate(model)

from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
accuracy=accuracy_score(y_test,y_pred4)
precision =precision_score(y_test,y_pred4,average='weighted')
recall= recall_score(y_test,y_pred4,average='weighted')
f1=f1_score(y_test,y_pred4,average='weighted')
accuracy,precision,recall,f1

model.score(X_test2,y_test)

model.score(X_train2,y_train)

SVCmodel = LinearSVC()
SVCmodel.fit(X_train2, y_train)
model_Evaluate(SVCmodel)
y_pred5 = SVCmodel.predict(X_test2)

from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
accuracy=accuracy_score(y_test,y_pred5)
precision =precision_score(y_test,y_pred5,average='weighted')
recall= recall_score(y_test,y_pred5,average='weighted')
f1=f1_score(y_test,y_pred5,average='weighted')
accuracy,precision,recall,f1

SVCmodel.score(X_test2,y_test)

SVCmodel.score(X_train2,y_train)

LRmodel = LogisticRegression(C = 2, max_iter = 1000, n_jobs=-1)
LRmodel.fit(X_train2, y_train)
model_Evaluate(LRmodel)
y_pred6 = LRmodel.predict(X_test2)

from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
accuracy=accuracy_score(y_test,y_pred6)
precision =precision_score(y_test,y_pred6,average='weighted')
recall= recall_score(y_test,y_pred6,average='weighted')
f1=f1_score(y_test,y_pred6,average='weighted')
accuracy,precision,recall,f1

LRmodel.score(X_test2,y_test)

LRmodel.score(X_train2,y_train)

labels=train.pop("survived")

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train, labels, test_size=0.05)



