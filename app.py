import streamlit as st
import os
import json
import uuid
from scraper import run_scraper
from attribute_extractor import extract_attributes
from scoring import score_and_recommend

# Directories
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")
st.title("🛍️ PickWise – Smarter Choices. Sharper Assortments.")
st.markdown("Upload your product concepts or scan competitors to get AI-powered buy recommendations.")

# --- Buyer Input Area ---
st.sidebar.header("1️⃣ Select Source")
input_type = st.sidebar.radio("How would you like to proceed?", ["Upload Designs", "Scrape Competitors"])

if input_type == "Upload Designs":
    uploaded_files = st.sidebar.file_uploader("Upload product images (JPG/PNG)", type=["jpg", "png"], accept_multiple_files=True)
    num_to_recommend = st.sidebar.slider("How many options to recommend?", 5, 20, 12)

    uploaded_products = []
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.name}")
        with open(file_path, "wb") as f:
            f.write(file.read())
        uploaded_products.append({
            "title": file.name.replace(".jpg", "").replace(".png", ""),
            "description": "",
            "image_path": file_path
        })

    if uploaded_products:
        st.subheader("🖼️ Uploaded Designs")
        st.image([p["image_path"] for p in uploaded_products], width=150)
        if st.button("🔍 Analyze Uploaded Designs"):
            enriched = extract_attributes(uploaded_products)
            scored, reco = score_and_recommend(enriched, num_to_recommend)
            st.success("Buyability Scores & Recommendations")
            st.dataframe(scored)
            st.subheader("📌 Recommended to Buy")
            st.dataframe(reco)

elif input_type == "Scrape Competitors":
    brand = st.sidebar.selectbox("Select Brand", ["H&M", "Zara", "Max", "Splash", "Shein"])
    gender = st.sidebar.selectbox("Gender", ["Women", "Men", "Girls", "Boys"])
    season = st.sidebar.selectbox("Season", ["SS24", "AW23", "Transitional"])
    category_url = st.sidebar.text_input("Or paste category URL (optional)", "")

    st.sidebar.write("We will scrape top 150 products for this selection.")
    if st.sidebar.button("⚙️ Start Scraping"):
        with st.spinner("Scraping competitor products..."):
            scraped = run_scraper(brand=brand, gender=gender, season=season, category_url=category_url)
            enriched = extract_attributes(scraped)
            scored, reco = score_and_recommend(enriched, 20)
            st.success(f"Scraped and analyzed {len(enriched)} products from {brand}")
            st.dataframe(scored)
            st.subheader("📌 Recommended Options")
            st.dataframe(reco)

# --- Prompt Refinement (Optional) ---
st.sidebar.header("2️⃣ Refine Recommendations")
prompt_input = st.sidebar.text_input("Example: More red long dresses, fewer black bodycons")
if prompt_input:
    st.info(f"Prompt-based refinement logic to be enabled soon: '{prompt_input}'")

# --- Save/Export Options ---
if st.button("💾 Export Results"):
    st.download_button("Download JSON", data=json.dumps(reco, indent=2), file_name="recommendations.json")

st.markdown("---")
st.caption("Built with 💡 by your Product AI assistant.")
