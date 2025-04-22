# app.py
import streamlit as st
from scraper import scrape_category
from utils import extract_attributes, calculate_buyability_scores, recommend_products
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")
st.title("🧠 PickWise – Smarter Choices. Sharper Assortments.")

st.sidebar.header("👗 Competitive Scan Inputs")
brand = st.sidebar.selectbox("Select Brand", ["H&M", "Zara", "MaxFashion", "Splash", "Shein"])
category = st.sidebar.selectbox("Select Category", ["Dresses", "Handbags", "T-Shirts", "Character Tops"])
gender = st.sidebar.selectbox("Select Gender", ["Women", "Men", "Kids"])
season = st.sidebar.selectbox("Select Season", ["All Year", "Spring/Summer", "Autumn/Winter"])
category_url = st.sidebar.text_input("Paste Category URL (Optional)")

if st.sidebar.button("Scrape Now"):
    st.session_state["scraped_data"] = scrape_category(brand, category, gender, season, category_url)
    st.success("Scraping Complete! Proceed to Attribute Extraction")

st.header("📥 Upload Your Candidate Designs")
candidate_files = st.file_uploader("Upload candidate images", type=["jpg", "png"], accept_multiple_files=True)

if candidate_files:
    st.image([Image.open(f) for f in candidate_files], width=100, caption=[f.name for f in candidate_files])
    extracted = extract_attributes(candidate_files)
    st.session_state["candidate_attrs"] = extracted
    st.success("Attributes Extracted")

if "scraped_data" in st.session_state and "candidate_attrs" in st.session_state:
    st.header("🧮 Scoring & Recommendations")
    scraped_df = st.session_state["scraped_data"]
    candidate_df = st.session_state["candidate_attrs"]

    scored_df = calculate_buyability_scores(candidate_df, scraped_df)
    st.write("Buyability Scores:", scored_df)

    n_to_buy = st.slider("Number of options to recommend", 5, min(20, len(scored_df)), 10)
    recommended_df = recommend_products(scored_df, n_to_buy)
    st.write("Recommended Selection:", recommended_df)

    st.download_button("Download Recommendation CSV", data=recommended_df.to_csv(), file_name="pickwise_recommendations.csv")
