import streamlit as st
import pandas as pd
from attribute_extractor import enrich_attributes_from_images as enrich_and_export_attributes
from scraper import scrape_all_sources
from buyability_score import compute_buyability_scores, recommend_top_n
from visualizer import visualize_buyability_breakdown, visualize_candidate_vs_market, visualize_brand_vs_brand

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")
st.title("🧠 PickWise")
st.caption("Smarter Choices. Sharper Assortments.")

# Sidebar Input Section
with st.sidebar:
    st.header("Configure Run")
    gender = st.selectbox("Gender", ["Women", "Men", "Kids"])
    season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])

    with st.expander("1. Scrape Brand Data"):
        brand_inputs = []
        num_urls = st.slider("Number of brand-category URLs", 1, 5, 2)
        for i in range(num_urls):
            col1, col2 = st.columns([1, 3])
            with col1:
                brand = st.selectbox(f"Brand {i+1}", ["H&M", "Zara", "MaxFashion", "Splash", "Shein"], key=f"brand_{i}")
            with col2:
                url = st.text_input(f"Category URL {i+1}", key=f"url_{i}")
            if url:
                brand_inputs.append((brand, url))
        scrape_trigger = st.button("🔍 Scrape Brand Data")

    with st.expander("2. Upload Candidate Designs"):
        candidate_files = st.file_uploader("Upload design images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
        if candidate_files:
            st.success(f"Uploaded {len(candidate_files)} images")

# Main Content Area
col1, col2 = st.columns([2, 1])

with col1:
    brand_data = {}
    candidate_data = None

    # Fix: Ensure that scraping process works properly
    if scrape_trigger and brand_inputs:
        with st.spinner("Scraping brand data..."):
            brand_data = scrape_all_sources(gender, season, brand_inputs)  # Use correct scraping logic
            if not brand_data:
                st.warning("No data scraped. Please check the category URLs and try again.")
            else:
                st.success("Scraping completed!")

    # Fix: Process candidate designs correctly
    if candidate_files:
        with st.spinner("Extracting candidate attributes..."):
            candidate_data = enrich_and_export_attributes(candidate_files)  # Process uploaded images

        for brand, df in brand_data.items():
            brand_data[brand] = enrich_and_export_attributes(df)

    # Only proceed with recommendations if data exists
    if candidate_data is not None and brand_data:
        all_market_data = pd.concat(brand_data.values(), ignore_index=True)
        scored_candidates = compute_buyability_scores(candidate_data, all_market_data)
        recommendations = recommend_top_n(scored_candidates, top_n=12)

        st.subheader("💡 Top Recommended Candidates")
        top_row = st.columns(6)
        bottom_row = st.columns(6)
        for i, row in recommendations.iterrows():
            target_col = top_row if i < 6 else bottom_row
            with target_col[i % 6]:
                st.image(row.get("image_path", ""), use_column_width=True, caption=f"Score: {row['buyability_score']:.2f}")

        st.divider()
        st.subheader("📊 Visual Insights")
        visualize_buyability_breakdown(scored_candidates)
        visualize_candidate_vs_market(candidate_data, all_market_data)
        visualize_brand_vs_brand(brand_data)

with col2:
    st.info("📘 Instructions:\n\n1. Add brand URLs by category.\n2. Upload your candidate designs.\n3. See top picks and market-fit visuals!")
