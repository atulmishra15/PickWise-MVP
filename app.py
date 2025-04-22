import streamlit as st
import pandas as pd
from scraper import scrape_all_sources
from attribute_extractor import enrich_attributes
from scoring import compute_buyability_scores
from recommendation import recommend_top_n
from visualizer import (
    visualize_heatmap,
    plot_attribute_distribution,
    plot_score_breakdown,
    show_image_grid,
    plot_market_comparison,
    plot_candidate_vs_brands_comparison
)

st.set_page_config(page_title="PickWise", layout="wide")
st.title("PickWise – Smarter Choices. Sharper Assortments.")

st.subheader("Step 1: Provide scraping inputs")
category = st.selectbox("Select Category", ["Dresses", "T-Shirts", "Handbags", "Shirts"])
gender = st.selectbox("Select Gender", ["Women", "Men", "Girls", "Boys"])
season = st.selectbox("Select Season", ["SS", "FW", "Transitional"])

st.markdown("### Enter product listing URLs (multiple URLs per brand can be separated by commas):")
urls = {}
urls["maxfashion_new"] = st.text_input("Max Fashion - New Designs URLs (comma-separated)")
urls["maxfashion_past"] = st.text_input("Max Fashion - Past Designs URLs (comma-separated)")
urls["shein_new"] = st.text_input("Shein - New Designs URLs (comma-separated)")
urls["shein"] = st.text_input("Shein - Market URLs (comma-separated)")
urls["hnm"] = st.text_input("H&M - Market URLs (comma-separated)")
urls["zara"] = st.text_input("Zara - Market URLs (comma-separated)")
urls["splash"] = st.text_input("Splash - Market URLs (comma-separated)")

uploaded_candidates = st.file_uploader("Upload Candidate Designs (CSV file)", type=["csv"])

run_button = st.button("Run Analysis")

if run_button:
    with st.spinner("Scraping and analyzing..."):
        try:
            df_new, df_past, df_comp = scrape_all_sources(category, gender, season, urls)

            if uploaded_candidates is not None:
                df_uploaded = pd.read_csv(uploaded_candidates)
                df_uploaded = enrich_attributes(df_uploaded)
                st.success("Uploaded candidates processed.")
            else:
                df_uploaded = enrich_attributes(df_new)

            enriched_past = enrich_attributes(df_past)
            enriched_comp = enrich_attributes(df_comp)

            scored_df = compute_buyability_scores(df_uploaded, enriched_past, enriched_comp)
            st.success("Buyability scores computed.")

            top_n = st.slider("Select number of top options to recommend:", 5, 20, 12)
            recommended = recommend_top_n(scored_df, top_n)
            st.subheader("Top Recommendations")
            st.dataframe(recommended)

            st.subheader("Visual Comparison")
            show_image_grid(recommended)
            plot_score_breakdown(recommended)
            visualize_heatmap(scored_df)
            plot_attribute_distribution(scored_df)

            st.markdown("#### Candidate vs Brand Comparison")
            plot_candidate_vs_brands_comparison(df_uploaded, enriched_comp)

            st.markdown("#### Brand vs Brand Comparison")
            plot_market_comparison(df_uploaded, enriched_comp)

        except Exception as e:
            st.error(f"Error during processing: {e}")
