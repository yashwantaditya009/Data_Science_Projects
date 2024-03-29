# -*- coding: utf-8 -*-
"""Blackcoffer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1glqtYnxuXVvD1BasmtKypJMM3xYsLUI5
"""

import requests
from bs4 import BeautifulSoup
import nltk
import pandas as pd
import openpyxl
import numpy as np
import re
from textblob import TextBlob
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
nltk.download('cmudict')

df = pd.read_excel('Input.xlsx')
df

lst = df['URL'].to_numpy()
titles = []
for item in lst:
    a = re.split(r'/',item)
    titles.append(a[3])

titles

# Removing "-" symbol from the titles
titles_without_dash = [title.replace('-', ' ') for title in titles]

# Creating a DataFrame from the titles
data = pd.DataFrame({'Titles': titles_without_dash})

# Saving the DataFrame to Excel file
data.to_excel('Output Data.xlsx', index=False)

df_output = pd.read_excel('Output Data.xlsx')
df_output['Titles'] = df_output['Titles'].str.title()
df_output

def get_positive_score(text):
    return TextBlob(text).sentiment.polarity

def get_negative_score(text):
    return TextBlob(text).sentiment.subjectivity

def get_polarity_score(text):
    return TextBlob(text).sentiment.polarity

def get_subjectivity_score(text):
    return TextBlob(text).sentiment.subjectivity

def get_avg_sentence_length(text):
    sentences = nltk.sent_tokenize(text)
    return sum(len(nltk.word_tokenize(sentence)) for sentence in sentences) / len(sentences)

def get_percentage_complex_words(text):
    words = nltk.word_tokenize(text)
    complex_words = [word for word, tag in nltk.pos_tag(words) if tag in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']]
    return (len(complex_words) / len(words)) * 100

def get_fog_index(text):
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    num_complex_words = len([word for word, tag in nltk.pos_tag(words) if tag in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']])
    avg_sentence_length = sum(len(nltk.word_tokenize(sentence)) for sentence in sentences) / len(sentences)
    return 0.4 * (avg_sentence_length + (num_complex_words / len(sentences)))

def get_avg_words_per_sentence(text):
    sentences = nltk.sent_tokenize(text)
    return len(nltk.word_tokenize(text)) / len(sentences)

def get_complex_word_count(text):
    words = nltk.word_tokenize(text)
    return len([word for word, tag in nltk.pos_tag(words) if tag in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']])

def get_word_count(text):
    words = nltk.word_tokenize(text)
    return len(words)

def get_syllables_per_word(text):
    words = nltk.word_tokenize(text)
    syllable_count = sum(nltk.syllable_count(word) for word in words)
    return syllable_count / len(words)

def get_personal_pronouns(text):
    words = nltk.word_tokenize(text)
    personal_pronouns = ['I', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours', 'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs']
    return len([word for word in words if word.lower() in personal_pronouns])

def get_avg_word_length(text):
    words = nltk.word_tokenize(text)
    return sum(len(word) for word in words) / len(words)

# Define the function to calculate the number of syllables per word
def get_syllables_per_word(text):
    words = nltk.word_tokenize(text)
    cmudict = nltk.corpus.cmudict.dict()
    syllable_count = sum(len(cmudict.get(word.lower(), [0])) for word in words)
    return syllable_count / len(words)

# Assuming you have already loaded the DataFrame 'df_output'

# Apply the functions to calculate the scores and metrics and add them as columns to the DataFrame
df_output['POSITIVE SCORE'] = df_output['Titles'].apply(get_positive_score)
df_output['NEGATIVE SCORE'] = df_output['Titles'].apply(get_negative_score)
df_output['POLARITY SCORE'] = df_output['Titles'].apply(get_polarity_score)
df_output['SUBJECTIVITY SCORE'] = df_output['Titles'].apply(get_subjectivity_score)
df_output['AVG SENTENCE LENGTH'] = df_output['Titles'].apply(get_avg_sentence_length)
df_output['PERCENTAGE OF COMPLEX WORDS'] = df_output['Titles'].apply(get_percentage_complex_words)
df_output['FOG INDEX'] = df_output['Titles'].apply(get_fog_index)
df_output['AVG NUMBER OF WORDS PER SENTENCE'] = df_output['Titles'].apply(get_avg_words_per_sentence)
df_output['COMPLEX WORD COUNT'] = df_output['Titles'].apply(get_complex_word_count)
df_output['WORD COUNT'] = df_output['Titles'].apply(get_word_count)
df_output['SYLLABLE PER WORD'] = df_output['Titles'].apply(get_syllables_per_word)
df_output['PERSONAL PRONOUNS'] = df_output['Titles'].apply(get_personal_pronouns)
df_output['AVG WORD LENGTH'] = df_output['Titles'].apply(get_avg_word_length)

# Display the updated DataFrame
print(df_output)

URL_ID=df.URL_ID
URL=df.URL

display(URL.shape, URL_ID.shape)



new_set = pd.concat([URL_ID, URL, df_output], axis=1)
new_set

new_set.shape

new_set.to_excel('Output Data Structure.xlsx', index=False)