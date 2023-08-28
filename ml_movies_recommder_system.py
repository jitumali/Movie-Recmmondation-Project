# -*- coding: utf-8 -*-
"""ml-movies-recommder-system.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TGFuZOf5pXytb8fXpRncChzGo1CGQLYD
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
import ast #ast.literal_eval() convert string into list

movies = pd.read_csv('/content/drive/MyDrive/ML project for resume/Movies recommender systen/tmdb_5000_movies.csv')
credits = pd.read_csv('/content/drive/MyDrive/ML project for resume/Movies recommender systen/tmdb_5000_credits.csv')

movies.head(1)

credits.head(1)

movies=movies.merge(credits,on='title')

movies.head(1)

#genres
#id
#keyword
#title
#overview
#cast
#crew

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.info()

movies.head()

movies.isnull().sum()

movies.dropna(inplace=True) #delete null record

movies.duplicated().sum()

movies.iloc[0].genres

#'[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'
#['Action','Adventure','Fantasy','sciFi']

import ast #convert string into list

def convert(obj):
  L=[]
  for i in ast.literal_eval(obj):
    L.append(i['name'])
  return L

movies['genres']= movies['genres'].apply(convert)

movies.head()

movies['keywords']=movies['keywords'].apply(convert)

movies.head()

def convert3(obj):
  L=[]
  counter=0;
  for i in ast.literal_eval(obj):
    if counter != 3:
      L.append(i['name'])
      counter+=1
    else:
      break
  return L

movies['cast']=movies['cast'].apply(convert3)

movies['crew'][0]

def fetch_director(obj):
  L=[]
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      L.append(i['name'])
      break;
  return L

movies['crew']=movies['crew'].apply(fetch_director)

movies.head()

movies['overview'][0]

movies['overview']=movies['overview'].apply(lambda x:x.split()) #in lambda function x is input and split() method convert the string into list]

movies.head()

#remove space from 2 word
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

movies['tag'] = movies['overview']+ movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.head()

new_df = movies[['movie_id','title','tag']]

new_df

new_df['tag']=new_def['tag'].apply(lambda x:" ".join(x)) #convert this function  list into string

new_df['tag'][0]

new_df['tag']=new_def['tag'].apply(lambda x:x.lower())

new_df.head()

import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
  y = [];
  for i in text.split():
    y.append(ps.stem(i))

  return " ".join(y)

new_df['tag']=new_df['tag'].apply(stem)

new_df['tag'][0]

new_df['tag'][1]

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=500,stop_words="english")

vectors = cv.fit_transform(new_df['tag']).toarray()

vectors

vectors[0]

cv.get_feature_names_out()

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

similarity[1]

def recommend(movie):
  movie_index = new_df[new_df['title']== movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  for i in movies_list:
    print(new_df.iloc[i[0]].title)

recommend('Avatar')

import pickle

pickle.dump(new_df,open('movies.pkl','wb'))

pickle.dump(new_df.to_dict(),open('movies_dict.pkl','wb'))

pickle.dump(similarity,open('similarity.pkl','wb'))