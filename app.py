import streamlit as st
import pandas as pd
from scraper import run_scraper
from attribute_extractor import extract_attributes
from buyability_score import compute_buyability_scores
from recommendation import generate_recommendations
from visualizer import show_visualizations

# --- Streamlit UI setup ---
st.set_page_config(page_title="PickWise", layout="wide")

st.title("🧠 PickWise – Smarter Choices. Sharper Assortments.")

tabs = st.tabs(["1. 🔍 Comp Scan", "2. 📥 Upload Designs", "3. 💡 Recommendations", "4. 📊 Visual Analysis"])

# --- Comp Scan Tab ---
with tabs[0]:
    st.header("📦 Scrape Competitor Products")

    brand = st.selectbox("Select Brand", ["Zara", "H&M", "MaxFashion", "Splash", "Shein"])
    category = st.selectbox("Select Category", ["Dresses", "T-Shirts", "Handbags", "Character Tops"])
    gender = st.selectbox("Select Gender", ["Women", "Men", "Kids"])
    season = st.selectbox("Select Season", ["Summer", "Winter", "All"])
    custom_url = st.text_input("Or paste a category URL (optional):")

    if st.button("Run Scraper"):
        scraped_data = run_scraper(brand, category, gender, season, custom_url)
        if scraped_data:
            st.success(f"Scraped {len(scraped_data)} products from {brand}")
            df_scraped = pd.DataFrame(scraped_data)
            st.session_state["scraped_df"] = df_scraped
            st.dataframe(df_scraped.head())
        else:
            st.warning("No products found or failed to scrape.")

# --- Upload Designs Tab ---
with tabs[1]:
    st.header("🖼️ Upload Your Design Images")
    uploaded_files = st.file_uploader("Upload up to 20 design images", type=["jpg", "png"], accept_multiple_files=True)

    if uploaded_files:
        extracted = extract_attributes(uploaded_files)
        st.session_state["uploaded_df"] = pd.DataFrame(extracted)
        st.success("Attributes extracted for uploaded images.")
        st.dataframe(st.session_state["uploaded_df"])

# --- Recommendations Tab ---
with tabs[2]:
    st.header("🎯 Get Buyability Recommendations")

    if "scraped_df" in st.session_state and "uploaded_df" in st.session_state:
        scored_df = compute_buyability_scores(
            candidate_df=st.session_state["uploaded_df"],
            brand_history_df=st.session_state["scraped_df"],
            market_df=st.session_state["scraped_df"]
        )
        st.session_state["scored_df"] = scored_df

        num_recommend = st.slider("How many to recommend?", 5, 20, 12)
        prompt = st.text_input("Prompt to guide refinement (e.g., 'more red long dresses, fewer browns')")

        recos = generate_recommendations(scored_df, num_recommend, prompt)
        st.dataframe(recos)
    else:
        st.info("Please complete scraping and upload designs first.")

# --- Visualizations Tab ---
with tabs[3]:
    st.header("📈 Visual Comparison")

    if "scraped_df" in st.session_state:
        show_visualizations(st.session_state["scraped_df"])
    else:
        st.info("Scrape competitor products to see visual insights.")
