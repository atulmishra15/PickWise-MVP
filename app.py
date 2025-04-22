import streamlit as st
import pandas as pd
from attribute_extractor import enrich_and_export_attributes
from buyability_score import compute_buyability_scores
from recommendation import recommend_top_n
from visualizer import visualize_buyability_breakdown, visualize_candidate_vs_market, visualize_brand_vs_brand
from scraper import scrape_all_sources
from utils import load_uploaded_images

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")
st.title("🧠 PickWise")
st.caption("Smarter Choices. Sharper Assortments.")

st.sidebar.header("1. Scrape Brand Data")
brand_inputs = []

with st.sidebar.form("brand_form"):
    num_urls = st.slider("Number of brand-category URLs", 1, 5, 2)
    for i in range(num_urls):
        col1, col2 = st.columns([1, 3])
        with col1:
            brand = st.selectbox(f"Brand {i+1}", ["H&M", "Zara", "MaxFashion", "Splash", "Shein"], key=f"brand_{i}")
        with col2:
            url = st.text_input(f"Category URL {i+1}", key=f"url_{i}")
        brand_inputs.append((brand, url))
    scrape_trigger = st.form_submit_button("Scrape Selected Brand URLs")

brand_data = {}
if scrape_trigger:
    with st.spinner("Scraping brand data..."):
        brand_data = scrape_all_sources(brand_inputs)
        st.success("Scraping completed!")

st.sidebar.header("2. Upload Candidate Designs")
candidate_files = st.sidebar.file_uploader("Upload design images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
candidate_data = None

if candidate_files:
    st.sidebar.success(f"Uploaded {len(candidate_files)} images")
    candidate_data = load_uploaded_images(candidate_files)

# Enrich attributes for candidates and brands
if candidate_data is not None:
    with st.spinner("Extracting attributes..."):
        candidate_data = enrich_and_export_attributes(candidate_data, export_path="candidate_attributes.csv")

    for brand, df in brand_data.items():
        brand_data[brand] = enrich_and_export_attributes(df)

# Compute scores and visualize
if candidate_data is not None and brand_data:
    all_market_data = pd.concat(brand_data.values(), ignore_index=True)
    scored_candidates = compute_buyability_scores(candidate_data, all_market_data)
    recommendations = recommend_top_n(scored_candidates, top_n=12)

    st.header("💡 Top Recommended Candidates")
    for i, row in recommendations.iterrows():
        st.image(row["image_path"], width=150, caption=f"Score: {row['buyability_score']:.2f}")

    st.header("📊 Visual Insights")
    visualize_buyability_breakdown(scored_candidates)
    visualize_candidate_vs_market(candidate_data, all_market_data)
    visualize_brand_vs_brand(brand_data)
