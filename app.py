import streamlit as st
import pandas as pd
import os
from scraper import scrape_category_data  # assume this returns a DataFrame
from attribute_extractor import extract_attributes_from_df
from buyability_score import compute_buyability_scores
from recommendation import refine_recommendations

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")

st.title("🧠 PickWise – Smarter Choices. Sharper Assortments.")
st.markdown("Start with either scraping competitor data or uploading your candidate designs.")

# --- Tabs for user flow ---
tab1, tab2 = st.tabs(["🛍️ Scrape Competitor Data", "📤 Upload Candidate Designs"])

with tab1:
    st.header("Scrape Top 150 Products")

    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox("Select Brand", ["H&M", "Zara", "MaxFashion", "Splash", "Shein"])
    with col2:
        category_url = st.text_input("Paste Category URL (optional)")

    category = st.selectbox("Select Category", ["Dresses", "Handbags", "Casual T-Shirts", "Character Tops"])
    gender = st.selectbox("Gender", ["Women", "Men", "Kids"])
    season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])

    if st.button("Scrape"):
        with st.spinner("Scraping in progress..."):
            scraped_df = scrape_category_data(brand, category, gender, season, category_url)
            st.success(f"Scraped {len(scraped_df)} products.")
            st.dataframe(scraped_df.head())

        st.session_state["scraped_df"] = scraped_df

with tab2:
    st.header("Upload Your Candidate Designs")
    uploaded_files = st.file_uploader("Upload product images (PNG, JPG)", accept_multiple_files=True)

    if uploaded_files:
        uploaded_paths = []
        for file in uploaded_files:
            path = os.path.join("uploads", file.name)
            with open(path, "wb") as f:
                f.write(file.read())
            uploaded_paths.append(path)

        st.session_state["uploaded_files"] = uploaded_paths
        st.success(f"Uploaded {len(uploaded_paths)} files.")

# --- Common Assortment Builder ---

if "scraped_df" in st.session_state or "uploaded_files" in st.session_state:
    st.header("🔍 Extract Attributes + Score Products")

    if "scraped_df" in st.session_state:
        raw_df = st.session_state["scraped_df"]
    else:
        # Placeholder for visual-only uploaded images
        raw_df = pd.DataFrame({"image_path": st.session_state["uploaded_files"]})

    # Step 1: Extract Attributes
    st.subheader("Step 1 – Attribute Extraction")
    enriched_df = extract_attributes_from_df(raw_df)
    st.dataframe(enriched_df.head())

    # Step 2: Buyability Scoring
    st.subheader("Step 2 – Compute Buyability Score")
    scored_df = compute_buyability_scores(enriched_df)
    st.dataframe(scored_df.head())

    # Step 3: Recommendation Filters
    st.subheader("Step 3 – Buyer Prompt & Refinement")

    prompt = st.text_input("Give Refinement Prompt (e.g., more red, reduce browns)")
    price_min = st.number_input("Min Price (if available)", min_value=0, value=0)
    price_max = st.number_input("Max Price (if available)", min_value=0, value=500)
    top_n = st.slider("How many products to recommend?", 5, 30, 12)

    if st.button("Get Recommendations"):
        final_reco = refine_recommendations(
            scored_df,
            prompt=prompt,
            top_n=top_n,
            price_min=price_min,
            price_max=price_max
        )

        st.success(f"Here are your top {len(final_reco)} picks:")

        for idx, row in final_reco.iterrows():
            st.image(row.get("image_url", row.get("image_path", "")), width=200, caption=f"{row.get('title', '')} | Score: {round(row['buyability_score'],2)}")

        st.dataframe(final_reco)

# Footer
st.markdown("---")
st.caption("Built with 💡 by PickWise · MVP v1.1")
