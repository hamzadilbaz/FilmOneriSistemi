import pickle
import streamlit as st
import requests 

movies_list = pickle.load(open('movies_list.pkl', 'rb'))
titles_list = movies_list['title']
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie = st.selectbox(
    'Which movie would you like to get recommendations for?',  
    titles_list.values)

def fetchPoster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=3b75df80a2ffd6aa0e2fd29724231936&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(selected_movie):
    movie_index = movies_list[movies_list['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    re_movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []  
    for i in re_movie_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetchPoster(movie_id))
        recommended_movies.append(movies_list.iloc[i[0]].title)

    return  recommended_movies,recommended_movies_posters

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

