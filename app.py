import streamlit as st
import pandas as pd
import tempfile
from PIL import Image
import os

from scraper import run_scraper  # category, gender, season, brand_urls
from attribute_extractor import extract_attributes
from buyability_score import compute_buyability_scores
from recommendation import get_recommendations
from visualizer import (
    plot_attribute_distribution,
    compare_uploaded_vs_scraped,
    show_buyability_distribution,
    show_price_vs_score
)

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")

st.title("👗 PickWise – Smarter Choices. Sharper Assortments.")

# --- Step 1: Category & Brand Inputs ---
st.sidebar.header("1. Competitor Scan Input")
category = st.sidebar.selectbox("Select Category", ["Women Dresses", "Handbags", "Men Casual T-Shirts", "Kids Character Tops"])
gender = st.sidebar.selectbox("Gender", ["Women", "Men", "Kids"])
season = st.sidebar.selectbox("Season", ["Spring/Summer", "Autumn/Winter"])
brand_urls = {}

st.sidebar.markdown("### Add Competitor URLs (optional)")
for brand in ["H&M", "Zara", "MaxFashion", "Splash", "Shein"]:
    brand_urls[brand] = st.sidebar.text_input(f"{brand} URL")

if st.sidebar.button("Run Scraper"):
    scraped_df = run_scraper(category, gender, season, brand_urls)
    st.session_state["scraped_df"] = scraped_df
    st.success(f"Scraped {len(scraped_df)} products across 5 brands.")
    st.dataframe(scraped_df.head())

# --- Step 2: Upload Candidate Designs ---
st.header("📤 Upload Candidate Product Designs")
uploaded_files = st.file_uploader("Upload product images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
uploaded_data = []

if uploaded_files:
    st.image([Image.open(f) for f in uploaded_files], width=100)
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            uploaded_data.append(tmp.name)

# --- Step 3: Extract Attributes ---
if st.button("🔍 Extract Attributes"):
    attr_df = extract_attributes(scraped=st.session_state.get("scraped_df", None), uploaded_images=uploaded_data)
    st.session_state["attr_df"] = attr_df
    st.dataframe(attr_df.head())
    st.success("Attributes extracted!")

# --- Step 4: Score for Buyability ---
if "attr_df" in st.session_state:
    st.header("📊 Buyability Scoring")
    scored_df = compute_buyability_scores(st.session_state["attr_df"])
    st.session_state["scored_df"] = scored_df
    st.dataframe(scored_df[["image", "brand", "buyability_score"] + [col for col in scored_df.columns if col.startswith("attr_")]].head())

# --- Step 5: Recommendations ---
if "scored_df" in st.session_state:
    st.header("🎯 Recommendations")
    budget = st.slider("Set max budget per item (AED)", min_value=30, max_value=500, value=250)
    quantity = st.slider("How many items to recommend?", min_value=5, max_value=30, value=12)

    reco_df = get_recommendations(st.session_state["scored_df"], budget=budget, n=quantity)
    st.dataframe(reco_df)
    st.session_state["reco_df"] = reco_df

# --- Step 6: Visualization & Analysis ---
if "scored_df" in st.session_state:
    st.header("📈 Assortment Visualization")
    scored_df = st.session_state["scored_df"]

    plot_attribute_distribution(scored_df, "color", "Color Spread")
    plot_attribute_distribution(scored_df, "occasion", "Occasion Mix")
    show_buyability_distribution(scored_df)
    show_price_vs_score(scored_df)

    if "scraped_df" in st.session_state:
        compare_uploaded_vs_scraped(
            pd.DataFrame(scored_df),
            st.session_state["scraped_df"],
            attribute="color"
        )

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 PickWise – Built for smarter, sharper retail.")
