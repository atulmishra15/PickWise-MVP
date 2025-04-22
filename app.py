# app.py

import streamlit as st
import pandas as pd
from scraper import scrape_category
from attribute_extractor import extract_attributes_from_images, extract_attributes_from_df
from buyability_score import calculate_buyability_score

st.set_page_config(page_title="PickWise", layout="wide")

st.title("🛍️ PickWise – Smarter Choices. Sharper Assortments.")
st.markdown("Select mode to provide candidate products – either scrape from brand websites or upload your own designs.")

mode = st.radio("Choose Input Mode:", ["Scrape from Brands", "Upload Candidate Designs"])

candidate_df = None

if mode == "Scrape from Brands":
    with st.form("scrape_form"):
        brand = st.selectbox("Select Brand", ["H&M", "Zara", "Max", "Splash", "Shein"])
        category = st.selectbox("Select Category", ["Dresses", "T-Shirts", "Handbags", "Character Tops"])
        gender = st.selectbox("Select Gender", ["Women", "Men", "Kids"])
        season = st.selectbox("Select Season", ["Spring", "Summer", "Fall", "Winter"])
        url = st.text_input("Category URL (optional):")
        submitted = st.form_submit_button("Scrape Products")

        if submitted:
            with st.spinner("Scraping products..."):
                candidate_df = scrape_category(brand, category, gender, season, url)
                st.success(f"{len(candidate_df)} products scraped.")
                candidate_df = extract_attributes_from_df(candidate_df)
                st.dataframe(candidate_df.head())

elif mode == "Upload Candidate Designs":
    uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    if uploaded_files:
        with st.spinner("Extracting attributes from images..."):
            candidate_df = extract_attributes_from_images(uploaded_files)
            st.success("Attribute extraction complete.")
            st.dataframe(candidate_df.head())

# --- BUYABILITY SCORING ---
if candidate_df is not None and not candidate_df.empty:
    st.subheader("📊 Buyability Scoring & Recommendations")

    try:
        past_brand_df = pd.read_csv("data/past_brand_products.csv")
        market_df = pd.read_csv("data/competitor_products.csv")

        attr_cols = ['color', 'pattern', 'occasion', 'material', 'design']
        numerical_cols = ['price']

        scored_df = calculate_buyability_score(
            candidate_df,
            past_brand_df,
            market_df,
            attr_cols,
            numerical_cols
        )

        st.success("Scoring complete.")
        st.dataframe(scored_df[['product_name', 'buyability_score'] + attr_cols + numerical_cols])

        top_n = st.slider("Number of products to recommend", min_value=1, max_value=min(20, len(scored_df)), value=10)
        top_recos = scored_df.head(top_n)

        st.subheader(f"✅ Top {top_n} Recommended Products")
        st.dataframe(top_recos)

        st.download_button(
            label="Download Recommendations",
            data=top_recos.to_csv(index=False),
            file_name="recommended_products.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Scoring failed: {e}")
else:
    st.info("Provide candidate products via scraping or upload to proceed.")
