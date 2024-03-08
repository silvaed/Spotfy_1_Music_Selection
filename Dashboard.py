import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from pandas.core.dtypes.cast import maybe_upcast
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.decomposition import IncrementalPCA
import streamlit as st

'''
first_Run  = 0 

while first_Run == 0:

    dados = pd.read_csv('https://raw.githubusercontent.com/sthemonica/music-clustering/main/Dados/Dados_totais.csv')
    dados_Alterados = dados.drop(["id","name","mode","artists_song","key","explicit"],axis=1)
    ohe = OneHotEncoder(dtype=int)
    colunas_ohe = ohe.fit_transform(dados_Alterados[['artists']]).toarray()
    dados_Alterados_dummy = dados_Alterados
    dados_Alterados_dummy = dados_Alterados_dummy.drop('artists',axis=1)
    dados_Alterados_dummy = pd.concat([dados_Alterados_dummy, pd.DataFrame(colunas_ohe, columns=ohe.get_feature_names_out(['artists']))], axis=1)


    SEED = 1224
    np.random.seed(1224)
    pca_pipeline = Pipeline([('scaler', StandardScaler()), ('PCA', PCA(n_components=0.7, random_state=SEED))])
    music_embedding_pca = pca_pipeline.fit_transform(dados_Alterados_dummy)
    projection = pd.DataFrame(data=music_embedding_pca)

    kmeans_pca_pipeline = KMeans(n_clusters=50, verbose=False, random_state=SEED)

    kmeans_pca_pipeline.fit(projection)

    dados_Alterados['cluster_pca'] = kmeans_pca_pipeline.predict(projection)

    dados_Alterados['artists_song'] = dados['artists_song']

    dados_Alterados['id'] = dados['id']

    projection['cluster_pca'] = kmeans_pca_pipeline.predict(projection)

    projection['artist'] = dados['artists']

    projection['artists_song'] = dados['artists_song']

    projection['id'] = dados['id']

    music_df = projection

    first_Run = first_Run +1


'''


st.set_page_config(layout= 'wide')

st.markdown("<h1 style='text-align: center;'>Playlist Recommendation (♪) </h1>", unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)



music_df = pd.read_csv("df_Machine_Learning.csv")




###########################################################################################################
    


# Filtering Dataframe using the filters selection 

artists_songs = music_df['artists_song'].str.split('-')
artist = []
song = []

filter_DF = False

for list_ in artists_songs:

    a = str(list_[0]).strip()
    s = str(list_[1]).strip()

    artist.append(a)
    song.append(s)

def nome_da_Musica_Artista (nome_artista_Musica,df):

    def make_clickable(link):
        # HTML anchor tag to render the hyperlink
        return f'<a target="_blank" href="{link}">Link</a>'


    cluster = list(df[df['artists_song']== nome_artista_Musica]['cluster_pca'])[0]

    ### Valor da coluna 1 e 2 OR X e Y da musica escolhida
    musica_Selecionada_X = df[df['artists_song']==nome_artista_Musica]
    musica_Selecionada_X = musica_Selecionada_X.reset_index(drop=True)
    musica_Selecionada_X = musica_Selecionada_X.iloc[0, 0]


    musica_Selecionada_Y = df[df['artists_song']==nome_artista_Musica]
    musica_Selecionada_Y = musica_Selecionada_Y.reset_index(drop=True)
    musica_Selecionada_Y = musica_Selecionada_Y.iloc[0, 1]

    # Musica no mesmo cluster
    musicas_recomendadas = df[ df['cluster_pca']== cluster] [[str(0), str(1), 'artists_song','id']]
    distancias = euclidean_distances(musicas_recomendadas[[str(0), str(1)]],[[musica_Selecionada_X,musica_Selecionada_Y]])
    musicas_recomendadas['Distancia'] = distancias

    musicas_recomendadas = musicas_recomendadas.sort_values('Distancia').head(11)
    musicas_recomendadas = musicas_recomendadas.reset_index(drop=True)
    musicas_recomendadas['link'] = 'https://open.spotify.com/track/'+musicas_recomendadas['id'].astype(str)
    musicas_recomendadas = musicas_recomendadas.drop(['id','Distancia',str(0),str(1)],axis=1)
    musicas_recomendadas = musicas_recomendadas[musicas_recomendadas['artists_song']!=nome_artista_Musica]
    musicas_recomendadas['link'] = musicas_recomendadas['link'].apply(make_clickable)


    return musicas_recomendadas



with st.sidebar.title('Filtros'):

    with st.sidebar.expander('Artist'):
        conjunto = set(artist)
        # Convertendo o conjunto de volta para uma lista
        artist_Unique = list(conjunto)
        #art_List = st.multiselect('Select a Country', artist_Unique, artist_Unique)

        # User text input for filtering
        user_input = st.text_input("Type to filter Artists:")

        # Filter options based on user input
        filtered_options = [option for option in artist_Unique if user_input.lower() in option.lower()]

        # Display a selectbox with filtered options
        if filtered_options:
            selected_option = st.selectbox("Choose an option:", filtered_options)
            st.write(f"You selected: {selected_option}")

            filtered_df = music_df[music_df['artist'] == selected_option]
            unique_songs = sorted(filtered_df['artists_song'].unique())

            if unique_songs:  # Check if the list is not empty
                selected_song = st.selectbox("Select a song:", unique_songs)
                st.write(f"You selected the song: {selected_song}")

                # Directly filter and update the DataFrame based on the selected song
                

                # Assuming 'playlist_DF' is now the filtered DataFrame you want to display
                # Display the updated DataFrame
                
            else:
                st.write("No songs found.")

                

                           
        else:
            st.write("No songs found for the selected artist.")
                


       
        
    


playlist_DF = nome_da_Musica_Artista(selected_song, music_df)    
playlist_DF = playlist_DF.to_html(escape=False, index=False)
playlist_DF = f"<style>thead th {{text-align: center;}}</style>{playlist_DF}"

st.markdown(playlist_DF, unsafe_allow_html=True)
    

  
    