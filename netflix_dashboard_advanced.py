import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------- Data Loading & Cleaning ----------------------
df = pd.read_csv("netflix_titles.csv")

# Clean and preprocess data
df['date_added'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month_name()

# Fix chained assignment warning (Pandas 3.0+ safe)
df.fillna({'country': 'Unknown', 'type': 'Unknown', 'listed_in': 'Unknown'}, inplace=True)

# ---------------------- Streamlit Config ----------------------
st.set_page_config(layout='wide', page_title="Netflix Dashboard")

# ---------------------- Theme Toggle ----------------------
mode = st.toggle("🌗 Toggle Dark Mode", value=True)

# ---------------------- Theme CSS ----------------------
if mode:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
        html, body, .stApp {
            background: linear-gradient(to bottom, #141414, #000000);
            color: white;
            font-family: 'Bebas Neue', sans-serif;
        }
        h1, h2, h3, h4 {
            color: #E50914;
            text-align: center;
        }
        .stMetric {
            background-color: #1a1a1a;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 10px;
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #1a1a1a;
            border-right: 1px solid #E50914;
        }
        footer {visibility: hidden;}
        footer:after {
            content: '🚀 Made with ❤️ by Prashanth Oruganti';
            visibility: visible;
            display: block;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #aaa;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        html, body, .stApp {
            background-color: #f9f9f9;
            color: #111;
            font-family: Arial, sans-serif;
        }
        h1, h2, h3, h4 {
            color: #e50914;
            text-align: center;
        }
        .stMetric {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 10px;
            color: #111 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #ddd;
        }
        footer {visibility: hidden;}
        footer:after {
            content: '🚀 Made with ❤️ by Prashanth Oruganti';
            visibility: visible;
            display: block;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #555;
        }
        </style>
    """, unsafe_allow_html=True)



# ---------------------- Logo + Title ----------------------
st.markdown("""
    <div style='text-align:center; padding-top: 10px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg' width='180' style='background: transparent; box-shadow: none;'>
        <h2 style='font-size: 28px; margin-top: 0;'><span style='color: #E50914;'>📺</span> Netflix Analytics Dashboard</h2>
    </div>
""", unsafe_allow_html=True)

# ---------------------- Metrics ----------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Titles", len(df))
col2.metric("Total Movies", df[df['type'] == 'Movie'].shape[0])
col3.metric("Total TV Shows", df[df['type'] == 'TV Show'].shape[0])
col4.metric("Countries", df['country'].nunique())

# ---------------------- Charts Row 1 ----------------------
c1, c2 = st.columns(2)

with c1:
    type_counts = df['type'].value_counts()
    fig = px.pie(names=type_counts.index, values=type_counts.values, title="Content by Type", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    year_data = df['year_added'].value_counts().sort_index()
    fig = px.bar(x=year_data.index, y=year_data.values, title="Titles Added Over Years",
                 labels={'x': 'Year', 'y': 'Count'})
    st.plotly_chart(fig, use_container_width=True)

# ---------------------- Charts Row 2 ----------------------
c3, c4 = st.columns(2)

with c3:
    genres = df['listed_in'].str.split(',').explode().str.strip()
    top_genres = genres.value_counts().head(10)
    fig = px.bar(top_genres, orientation='h', title="Top 10 Genres")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    top_countries = df['country'].str.split(',').explode().str.strip().value_counts().head(10)
    fig = px.bar(top_countries, orientation='h', title="Top 10 Countries by Titles")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------- Charts Row 3 ----------------------
st.subheader("📋 Most Frequent Directors and Titles")
tab1, tab2 = st.tabs(["🎬 Top Directors", "📺 Top Shows"])
with tab1:
    top_directors = df['director'].dropna().value_counts().head(10)
    st.dataframe(top_directors.reset_index().rename(columns={'index': 'Director', 'director': 'Titles'}))

with tab2:
    top_titles = df['title'].value_counts().head(10)
    st.dataframe(top_titles.reset_index().rename(columns={'index': 'Title', 'title': 'Frequency'}))
