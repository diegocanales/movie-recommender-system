import streamlit as st
from movie_recommender_system import paths
import pickle
from pathlib import Path
import pandas as pd

import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def load_model(model_path: Path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

st.title('Movie Recommender System')
st.write('Welcome to the Movie Recommender System! Please enter a movie title to get recommendations.')
df = pd.read_csv(paths.data_processed_dir() / "dataset.csv", usecols=['movie_id', "title"])
movie_list = df['title'].tolist()
movie_selected = st.selectbox('Movie Title', movie_list)
movie_id_selected = df[df['title'] == movie_selected]['movie_id'].values[0]
st.image(fetch_poster(movie_id_selected))
button_recommendations = st.button('Get Recommendations')

if button_recommendations:
    model = load_model(model_path=paths.models_dir() / "recommender.pkl")
    recommendations = model.predict(movie_selected)
    st.write(recommendations)

    movie_ids = []
    for title in recommendations:
        movie_id = df[df['title'] == title]['movie_id'].values[0]
        movie_ids.append(movie_id)
    recommended_movie_posters = [fetch_poster(movie_id) for movie_id in movie_ids]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(recommended_movie_posters[4])
