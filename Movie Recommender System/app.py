import streamlit as st
import pickle
import pandas as pd
import movieposters as mp


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:7]
    
    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

def show(l):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header(l[0][0])
        st.image(l[0][1])

    with col2:
        st.header(l[1][0])
        st.image(l[1][1])

    with col3:
        st.header(l[2][0])
        st.image(l[2][1])

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header(l[3][0])
        st.image(l[3][1])

    with col5:
        st.header(l[4][0])
        st.image(l[4][1])

    with col6:
        st.header(l[5][0])
        st.image(l[5][1])

movie_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movie_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('My Movie Recommender System - 21/02/2022')

selected_movie = st.selectbox('Enter Movie Name',movies['title'].values)
l = []
if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    for i in recommendations:
        link = mp.get_poster(title=i)
        l.append([i,link])
    show(l)