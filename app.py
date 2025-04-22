import os
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
import streamlit as st
from attribute_extractor import enrich_attributes_from_images
from scraper import scrape_all_sources
from scoring import compute_buyability_scores
from recommendation import get_top_n_recommendations
from visualizer import visualize_buyability_breakdown, visualize_candidate_vs_market

st.set_page_config(page_title="PickWise", layout="wide")
st.title("🛍️ PickWise – Smarter Choices. Sharper Assortments.")

st.markdown("Upload candidate images and compare against multiple brand categories. Scrape live data, analyze buyability, and visualize insights.")

# Sidebar: Brand-URL collection
st.sidebar.header("🔗 Input Brand Category URLs")
brand_inputs = []
num_urls = st.sidebar.number_input("How many URLs do you want to compare?", min_value=1, max_value=10, value=3)
brand_options = ["H&M", "Zara", "Max", "Splash", "Shein"]

for i in range(num_urls):
    cols = st.sidebar.columns([1, 3])
    brand = cols[0].selectbox(f"Brand #{i+1}", brand_options, key=f"brand_{i}")
    url = cols[1].text_input(f"Category URL #{i+1}", key=f"url_{i}")
    if brand and url:
        brand_inputs.append((brand, url))

# Candidate Images
st.header("📸 Upload Candidate Designs")
candidate_images = st.file_uploader("Upload images (JPG/PNG)", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if st.button("🚀 Run Analysis") and brand_inputs and candidate_images:
    with st.spinner("Scraping competitor products..."):
        scraped_data = scrape_all_sources(brand_inputs)

    with st.spinner("Extracting attributes from candidates and market data..."):
        candidate_df = enrich_attributes_from_images(candidate_images)
        market_df = enrich_attributes_from_images(scraped_data)

    with st.spinner("Scoring buyability and generating recommendations..."):
        scored_candidates = compute_buyability_scores(candidate_df, market_df)
        top_n = st.slider("Select Top N Recommendations", 5, 20, 12)
        top_recos = get_top_n_recommendations(scored_candidates, top_n)

    st.success("Done! Scroll down to see results.")

    st.header("🎯 Top Recommendations")
    st.dataframe(top_recos)

    st.header("📊 Buyability Breakdown")
    visualize_buyability_breakdown(scored_candidates)

    st.header("🧭 Candidate vs Market Visuals")
    visualize_candidate_vs_market(scored_candidates, market_df)
else:
    st.warning("Please upload candidate images and enter at least one brand-category URL.")
