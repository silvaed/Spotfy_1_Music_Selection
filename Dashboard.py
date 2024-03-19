
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import streamlit as st

st.set_page_config(layout='wide')

st.markdown("<h1 style='text-align: center;'>Playlist Recommendation (♪) </h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Load the dataset
music_df = pd.read_csv("df_Machine_Learning.csv")

# Splitting the 'artists_song' column into 'artist' and 'song'
artists_songs = music_df['artists_song'].str.split('-')
artist = []
song = []

for list_ in artists_songs:
    a = str(list_[0]).strip()
    s = str(list_[1]).strip()

    artist.append(a)
    song.append(s)

def recommend_song_artist(song_artist_name, df):
    def make_clickable(link):
        # HTML anchor tag to render the hyperlink
        return f'<a target="_blank" href="{link}">Link</a>'

    cluster = list(df[df['artists_song'] == song_artist_name]['cluster_pca'])[0]

    # X and Y values OR columns 1 and 2 of the selected song
    selected_song_X = df[df['artists_song'] == song_artist_name].reset_index(drop=True).iloc[0, 0]
    selected_song_Y = df[df['artists_song'] == song_artist_name].reset_index(drop=True).iloc[0, 1]

    # Songs in the same cluster
    recommended_songs = df[df['cluster_pca'] == cluster][[str(0), str(1), 'artists_song', 'id']]
    distances = euclidean_distances(recommended_songs[[str(0), str(1)]], [[selected_song_X, selected_song_Y]])
    recommended_songs['Distance'] = distances

    recommended_songs = recommended_songs.sort_values('Distance').head(11).reset_index(drop=True)
    recommended_songs['link'] = 'https://open.spotify.com/track/' + recommended_songs['id'].astype(str)
    recommended_songs = recommended_songs.drop(['id', 'Distance', str(0), str(1)], axis=1)
    recommended_songs = recommended_songs[recommended_songs['artists_song'] != song_artist_name]
    recommended_songs['link'] = recommended_songs['link'].apply(make_clickable)

    return recommended_songs

with st.sidebar:
    st.title('Filters')
    user_input = st.text_input("Type to filter Artists:")

    # Filtering options based on user input
    filtered_options = [option for option in set(artist) if user_input.lower() in option.lower()]

    if filtered_options:
        selected_option = st.selectbox("Choose an option:", filtered_options)
        st.write(f"You selected: {selected_option}")

        filtered_df = music_df[music_df['artist'] == selected_option]
        unique_songs = sorted(filtered_df['artists_song'].unique())

        if unique_songs:  # Check if the list is not empty
            selected_song = st.selectbox("Select a song:", unique_songs)
            st.write(f"You selected the song: {selected_song}")
        else:
            st.write("No songs found.")
    else:
        st.write("No songs found for the selected artist.")

# Generate and display the playlist DataFrame
playlist_DF = recommend_song_artist(selected_song, music_df)
playlist_DF_html = playlist_DF.to_html(escape=False, index=False)
playlist_DF_styled = f"<style>thead th {{text-align: center;}}</style>{playlist_DF_html}"

st.markdown(playlist_DF_styled, unsafe_allow_html=True)
