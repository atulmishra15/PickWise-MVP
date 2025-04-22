import streamlit as st
import pandas as pd
import tempfile
import os
from scraper import scrape_all_sources
from attribute_extractor import enrich_attributes
from buyability_score import compute_buyability_scores, recommend_top_n, DEFAULT_WEIGHTS
from visualizer import show_score_breakdown_chart, show_attribute_heatmap, show_diversity_matrix
from sklearn.metrics.pairwise import cosine_distances

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")
st.image("pickwise_logo.png", width=200)
st.title("PickWise: Smarter Choices. Sharper Assortments.")

st.sidebar.header("1. Input Controls")
mode = st.sidebar.radio("Choose input mode:", ["Live Scraping", "Upload Candidate Images"])

category = st.sidebar.selectbox("Category", ["dresses", "handbags", "t-shirts"])
gender = st.sidebar.selectbox("Gender", ["women", "men", "kids"])
season = st.sidebar.selectbox("Season", ["spring", "summer", "autumn", "winter"])
top_n = st.sidebar.slider("Top N Recommendations", 6, 30, 12)

st.sidebar.header("2. Scoring Weights")
newness_market = st.sidebar.slider("Newness to Market", 0.0, 1.0, DEFAULT_WEIGHTS["newness_to_market"])
newness_brand = st.sidebar.slider("Newness to Brand", 0.0, 1.0, DEFAULT_WEIGHTS["newness_to_brand"])
variety = st.sidebar.slider("Variety", 0.0, 1.0, DEFAULT_WEIGHTS["variety"])
completeness = st.sidebar.slider("Completeness", 0.0, 1.0, DEFAULT_WEIGHTS["completeness"])

weights = {
    "newness_to_market": newness_market,
    "newness_to_brand": newness_brand,
    "variety": variety,
    "completeness": completeness
}

st.sidebar.header("3. Optional Prompt Refinement")
prompt = st.sidebar.text_input("e.g., more red long dresses, less floral prints")

if mode == "Live Scraping":
    if st.button("Run Scraper and Generate Recommendations"):
        with st.spinner("Scraping products and computing recommendations..."):
            df_new, df_past, df_comp = scrape_all_sources(category, gender, season)
            df_enriched = enrich_attributes(df_new)
            df_scored = compute_buyability_scores(df_enriched, df_past, df_comp, weights)
            df_top = recommend_top_n(df_scored, top_n, prompt)

            st.success("Done! Here are your recommendations:")
            st.dataframe(df_top)

            # Visualizations
            show_score_breakdown_chart(df_top)
            show_attribute_heatmap(df_top)
            similarity_matrix = cosine_distances(df_top[["score_newness_market", "score_newness_brand", "score_variety", "score_completeness"]])
            show_diversity_matrix(df_top, similarity_matrix)

elif mode == "Upload Candidate Images":
    uploaded_files = st.file_uploader("Upload candidate product images", type=["jpg", "png"], accept_multiple_files=True)
    if st.button("Process Uploaded Designs") and uploaded_files:
        with st.spinner("Extracting attributes and computing scores..."):
            temp_dir = tempfile.mkdtemp()
            for file in uploaded_files:
                with open(os.path.join(temp_dir, file.name), "wb") as f:
                    f.write(file.read())

            df_new, df_past, df_comp = scrape_all_sources(category, gender, season)
            df_enriched = enrich_attributes(temp_dir, from_images=True)
            df_scored = compute_buyability_scores(df_enriched, df_past, df_comp, weights)
            df_top = recommend_top_n(df_scored, top_n, prompt)

            st.success("Done! Here are your recommendations:")
            st.dataframe(df_top)

            # Visualizations
            show_score_breakdown_chart(df_top)
            show_attribute_heatmap(df_top)
            similarity_matrix = cosine_distances(df_top[["score_newness_market", "score_newness_brand", "score_variety", "score_completeness"]])
            show_diversity_matrix(df_top, similarity_matrix)
