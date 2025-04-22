import streamlit as st
import pandas as pd
from scraper import scrape_all_sources
from attribute_extractor import enrich_attributes
from scoring import compute_buyability_scores
from recommendation import recommend_top_n
from visualizer import visualize_heatmap, plot_attribute_distribution

st.set_page_config(page_title="PickWise", layout="wide")
st.title("PickWise – Smarter Choices. Sharper Assortments.")

st.subheader("Step 1: Provide category scraping links")
category = st.selectbox("Select Category", ["Dresses", "T-Shirts", "Handbags", "Shirts"])
gender = st.selectbox("Select Gender", ["Women", "Men", "Girls", "Boys"])
season = st.selectbox("Select Season", ["SS", "FW", "Transitional"])

st.markdown("### Enter product listing URLs:")
urls = {}
urls["maxfashion_new"] = st.text_input("Max Fashion - New Designs URL")
urls["maxfashion_past"] = st.text_input("Max Fashion - Past Designs URL")
urls["shein_new"] = st.text_input("Shein - New Designs URL")
urls["shein"] = st.text_input("Shein - Market URL")
urls["hnm"] = st.text_input("H&M - Market URL")
urls["zara"] = st.text_input("Zara - Market URL")
urls["splash"] = st.text_input("Splash - Market URL")

run_button = st.button("Run Analysis")

if run_button:
    with st.spinner("Scraping and analyzing..."):
        try:
            df_new, df_past, df_comp = scrape_all_sources(category, gender, season, urls)

            enriched_new = enrich_attributes(df_new)
            enriched_past = enrich_attributes(df_past)
            enriched_comp = enrich_attributes(df_comp)

            scored_df = compute_buyability_scores(enriched_new, enriched_past, enriched_comp)
            st.success("Buyability scores computed.")

            top_n = st.slider("Select number of top options to recommend:", 5, 20, 12)
            recommended = recommend_top_n(scored_df, top_n)
            st.subheader("Top Recommendations")
            st.dataframe(recommended)

            st.subheader("Visual Comparison")
            visualize_heatmap(scored_df)
            plot_attribute_distribution(scored_df)

        except Exception as e:
            st.error(f"Error during processing: {e}")
