import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Spotify Tracks & Genres Analysis", page_icon="🎵", layout="wide")

@st.cache_data
def load_data():
    genre_df = pd.read_csv("spotify_genres_clustered.csv")
    year_df = pd.read_csv("spotify_years_cleaned.csv")
    return genre_df, year_df

genre_data, year_data = load_data()

st.title("🎵 Spotify Tracks & Genres Database Analysis")
st.write("Bu uygulama, Spotify müzik veri setindeki ses özelliklerini, yıllara göre değişimleri ve tür kümelemelerini analiz eder.")

# Sidebar Seçimleri
st.sidebar.header("Analiz Paneli")
analysis_type = st.sidebar.radio("Analiz Türü Seçin", ["Yıllara Göre Müzik Trendleri", "Müzik Türleri Kümeleme (K-Means)"])

if analysis_type == "Yıllara Göre Müzik Trendleri":
    st.subheader("📈 Yıllara Göre Ses Özelliklerinin Değişimi (1921 - 2020)")
    
    sound_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'valence']
    selected_features = st.multiselect("Görüntülenecek Ses Özellikleri", sound_features, default=['danceability', 'energy', 'acousticness'])
    
    if selected_features:
        fig = px.line(year_data, x='year', y=selected_features, title="Yıllara Göre Ses Özellikleri Trendi")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Lütfen en az bir ses özelliği seçin.")

else:
    st.subheader("🎧 Müzik Türleri ve Küme Analizi")
    st.write("K-Means ile kümelenmiş müzik türlerinin popülarite ve özellik dağılımları:")
    
    clusters = sorted(genre_data['cluster'].unique().tolist())
    selected_cluster = st.selectbox("Küme (Cluster) Seçin", clusters)
    
    cluster_df = genre_data[genre_data['cluster'] == selected_cluster]
    st.write(f"Seçilen Kümedeki Tür Sayısı: {len(cluster_df)}")
    
    # En popüler ilk 10 tür
    top_genres = cluster_df.nlargest(10, 'popularity')
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x='popularity', y='genres', data=top_genres, palette='viridis', ax=ax)
    ax.set_xlabel("Popülarite")
    ax.set_ylabel("Müzik Türü")
    st.pyplot(fig)