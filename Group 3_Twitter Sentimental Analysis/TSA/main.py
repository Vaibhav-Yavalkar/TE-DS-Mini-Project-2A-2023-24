import re
import nltk
import string
import numpy as np
import pandas as pd
import streamlit as st
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Functions to clean and classify text
def remove_pattern(input_text, pattern):
    r = re.findall(pattern, input_text)
    for i in r:
        input_text = re.sub(i, '', input_text)
    return input_text

def clean_text(text):
    text = re.sub(r'@[\w]*', '', text)
    text = re.sub('[^a-zA-Z#]', ' ', text)
    text = ' '.join([w for w in text.split() if len(w) > 3])
    stemmer = PorterStemmer()
    text = ' '.join([stemmer.stem(i) for i in text.split()])
    return text

# Load the data
train = pd.read_csv('Twitter/train.csv')
test = pd.read_csv('Twitter/test.csv')
combine = pd.concat([train, test], ignore_index=True)
combine['tidy_tweet'] = combine['tweet'].apply(clean_text)

# Train a Naive Bayes Classifier
bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
bow = bow_vectorizer.fit_transform(combine['tidy_tweet'])
combine = combine.fillna(0)
X_train, X_test, y_train, y_test = train_test_split(bow, combine['label'], test_size=0.2, random_state=69)
model_naive = MultinomialNB().fit(X_train, y_train)

# Streamlit App
st.title("Sentiment Analysis App")

input_text = st.text_area("Enter a text:")
cleaned_text = clean_text(input_text)

if st.button("Classify"):
    if len(cleaned_text) == 0:
        st.write("Please enter some text.")
    else:
        text_vector = bow_vectorizer.transform([cleaned_text])
        prediction = model_naive.predict(text_vector)

        if prediction[0] == 0:
            st.write("Sentiment: Positive")
        elif prediction[0] == 1:
            st.write("Sentiment: Negative")
        else:
            st.write("Sentiment: Neutral")
