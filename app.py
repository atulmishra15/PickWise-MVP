import streamlit as st
import pandas as pd
from scraper import scrape_all_sources
from attribute_extractor import enrich_attributes
from buyability_score import compute_buyability_scores
from recommendation import recommend_top_n
from visualizer import (
    visualize_heatmap,
    plot_attribute_distribution,
    plot_score_breakdown,
    show_image_grid,
    plot_market_comparison,
    plot_candidate_vs_brands_comparison
)

st.set_page_config(page_title="PickWise", layout="wide")
st.title("PickWise – Smarter Choices. Sharper Assortments.")

st.subheader("Step 1: Provide scraping inputs")
category = st.selectbox("Select Category", ["Dresses", "T-Shirts", "Handbags", "Shirts"])
gender = st.selectbox("Select Gender", ["Women", "Men", "Girls", "Boys"])
season = st.selectbox("Select Season", ["SS", "FW", "Transitional"])

from PIL import Image
import requests
from io import BytesIO

# Brand logo mapping (you can update these URLs to better ones if needed)
brand_logos = {
    "Max Fashion - New": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Max_Fashion_Logo.png",
    "Max Fashion - Past": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Max_Fashion_Logo.png",
    "Shein - New": "https://upload.wikimedia.org/wikipedia/commons/f/fd/SHEIN_logo.png",
    "Shein": "https://upload.wikimedia.org/wikipedia/commons/f/fd/SHEIN_logo.png",
    "H&M": "https://upload.wikimedia.org/wikipedia/commons/5/53/H%26M-Logo.svg",
    "Zara": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Zara_Logo_2019.png",
    "Splash": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Splash_Fashions_logo.png"
}

# URL input
url_input_count = st.number_input("How many URLs do you want to input?", min_value=1, max_value=20, value=5)
for i in range(url_input_count):
    col1, col2, col3 = st.columns([1, 0.5, 3])
    with col1:
        brand = st.selectbox(f"Brand {i+1}", brand_options, key=f"brand_{i}")
    with col2:
        if brand in brand_logos:
            response = requests.get(brand_logos[brand])
            logo_img = Image.open(BytesIO(response.content))
            st.image(logo_img, width=50)
    with col3:
        url = st.text_input(f"URL for {brand}", key=f"url_{i}")
    if url:
        user_urls.append((brand, url))

uploaded_candidates = st.file_uploader("Upload Candidate Designs (CSV file)", type=["csv"])

run_button = st.button("Run Analysis")

if run_button:
    with st.spinner("Scraping and analyzing..."):
        try:
            df_new, df_past, df_comp = scrape_all_sources(category, gender, season, urls)

            if uploaded_candidates is not None:
                df_uploaded = pd.read_csv(uploaded_candidates)
                df_uploaded = enrich_attributes(df_uploaded)
                st.success("Uploaded candidates processed.")
            else:
                df_uploaded = enrich_attributes(df_new)

            enriched_past = enrich_attributes(df_past)
            enriched_comp = enrich_attributes(df_comp)

            scored_df = compute_buyability_scores(df_uploaded, enriched_past, enriched_comp)
            st.success("Buyability scores computed.")

            top_n = st.slider("Select number of top options to recommend:", 5, 20, 12)
            recommended = recommend_top_n(scored_df, top_n)
            st.subheader("Top Recommendations")
            st.dataframe(recommended)

            st.subheader("Visual Comparison")
            show_image_grid(recommended)
            plot_score_breakdown(recommended)
            visualize_heatmap(scored_df)
            plot_attribute_distribution(scored_df)

            st.markdown("#### Candidate vs Brand Comparison")
            plot_candidate_vs_brands_comparison(df_uploaded, enriched_comp)

            st.markdown("#### Brand vs Brand Comparison")
            plot_market_comparison(df_uploaded, enriched_comp)

        except Exception as e:
            st.error(f"Error during processing: {e}")
