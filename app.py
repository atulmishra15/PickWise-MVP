import streamlit as st
from scraper import scrape_products
from attribute_extractor import extract_attributes
from buyability_score import compute_buyability_scores
from recommendation import recommend_products
from visualizer import show_visualizations

st.set_page_config(page_title="PickWise", layout="wide")

st.title("PickWise – Smarter Choices. Sharper Assortments.")
st.markdown("Upload your candidate designs and let PickWise guide your assortment decisions.")

brand = st.selectbox("Select Brand", ["Max", "Splash", "Shein", "H&M", "Zara"])
category = st.selectbox("Select Category", ["Women Dresses", "Handbags", "Men Casual T-Shirts", "Kids Character Tops"])
num_options = st.slider("How many options do you want to buy?", min_value=1, max_value=20, value=12)

uploaded_files = st.file_uploader("Upload candidate product images", accept_multiple_files=True)

if st.button("Generate Recommendations") and uploaded_files:
    st.info("Extracting attributes and scraping competitors...")
    candidates = extract_attributes(uploaded_files)
    market_data = scrape_products(category, region="UAE")
    scores = compute_buyability_scores(candidates, market_data, brand, category)
    recommendations = recommend_products(scores, num_options)

    st.success("Recommendations Ready!")
    show_visualizations(recommendations)
    for reco in recommendations:
        st.image(reco["image"])
        st.write(reco["explanation"])
