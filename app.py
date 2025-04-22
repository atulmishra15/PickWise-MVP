import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from attribute_extractor import extract_attributes_from_images, extract_attributes_from_scraped_df
from scraper import scrape_products
from buyability_score import compute_buyability_scores, recommend_top_n

st.set_page_config(page_title="PickWise", layout="wide")
st.image("pickwise_logo.png", width=180)
st.title("👗 PickWise – Smarter Choices. Sharper Assortments.")
st.markdown("Upload your candidate designs or scrape top 150 products per brand/category to begin scoring and recommendations.")

# --- Inputs ---
input_mode = st.radio("Choose input mode:", ["Upload Design Images", "Scrape from Brand URLs"])

if input_mode == "Upload Design Images":
    uploaded_files = st.file_uploader("Upload up to 20 images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        input_df = extract_attributes_from_images(uploaded_files)
    else:
        st.stop()
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", ["Dresses", "Handbags", "T-Shirts", "Tops"])
    with col2:
        gender = st.selectbox("Gender", ["Women", "Men", "Kids"])
    with col3:
        season = st.selectbox("Season", ["Spring/Summer", "Autumn/Winter"])

    input_df = scrape_products(category=category, gender=gender, season=season)
    input_df = extract_attributes_from_scraped_df(input_df)

# --- Past data (mock for now) ---
@st.cache_data
def load_mock_reference_data():
    # Replace with real data sources later
    past_brand = pd.read_csv("data/past_brand_catalog.csv")
    competitors = pd.read_csv("data/competitor_catalog.csv")
    return past_brand, competitors

past_brand_df, competitor_df = load_mock_reference_data()

# --- Weights ---
st.sidebar.header("Scoring Weights")
newness_market_wt = st.sidebar.slider("Newness to Market", 0.0, 1.0, 0.4)
newness_brand_wt = st.sidebar.slider("Newness to Brand", 0.0, 1.0, 0.2)
variety_wt = st.sidebar.slider("Variety Within Selection", 0.0, 1.0, 0.2)
completeness_wt = st.sidebar.slider("Completeness", 0.0, 1.0, 0.2)

weights = {
    "newness_to_market": newness_market_wt,
    "newness_to_brand": newness_brand_wt,
    "variety": variety_wt,
    "completeness": completeness_wt
}

# --- Compute Scores ---
scored_df = compute_buyability_scores(input_df, past_brand_df, competitor_df, weights)

# --- Prompt Filter ---
prompt_input = st.text_input("Want to nudge the assortment? (e.g., 'more red long dresses, less floral')")
top_n = st.slider("How many options do you want?", 1, 20, 12)

recommended = recommend_top_n(scored_df, top_n=top_n, prompt_filters=prompt_input)

# --- Visualize Recommendations ---
st.subheader(f"🧠 Top {top_n} Recommendations")

for i, row in recommended.iterrows():
    st.markdown(f"**Option {i+1}:** `{', '.join(row['tags'])}`")
    st.progress(min(row["buyability_score"], 1.0))

# --- Score Breakdown Chart ---
st.subheader("📊 Buyability Score Breakdown")
score_columns = ["score_newness_market", "score_newness_brand", "score_variety", "score_completeness"]

fig, ax = plt.subplots(figsize=(10, 4))
recommended[score_columns].plot(kind='bar', stacked=True, ax=ax)
ax.set_xticks(range(len(recommended)))
ax.set_xticklabels([f"Option {i+1}" for i in range(len(recommended))], rotation=0)
ax.set_ylabel("Score")
ax.legend(loc="upper right")
st.pyplot(fig)

# --- Download ---
st.download_button("Download Recommended Assortment CSV", recommended.to_csv(index=False), file_name="pickwise_recommendations.csv", mime="text/csv")
