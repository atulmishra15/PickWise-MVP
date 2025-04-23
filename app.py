import streamlit as st
from PIL import Image
import os
import pandas as pd
from attribute_extractor import extract_attributes_from_image
from buyability_score import compute_buyability_scores, recommend_top_n
import matplotlib.pyplot as plt

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")
st.title("🛒️ PickWise – Smarter Choices. Sharper Assortments.")

st.markdown("Upload your **competitor products** and **candidate designs** to get buyability scores and recommendations.")

# --- Upload Section ---
st.sidebar.header("Step 1: Upload Images")
comp_images = st.sidebar.file_uploader("Upload Competitor Product Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
cand_images = st.sidebar.file_uploader("Upload Candidate Designs (Max 50)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if len(cand_images) > 50:
    st.sidebar.error("⚠️ You can upload up to 50 candidate designs only.")
    cand_images = cand_images[:50]

# --- Run Analysis Button ---
if st.sidebar.button("🔍 Run PickWise Analysis") and comp_images and cand_images:
    st.subheader("🔧 Extracting Attributes...")

    comp_data = []
    for img in comp_images:
        image = Image.open(img)
        attrs = extract_attributes_from_image(image)
        attrs["image"] = image
        attrs["name"] = img.name
        attrs["design_description"] = " ".join(str(v) for k, v in attrs.items() if k not in ["image", "name"])
        comp_data.append(attrs)

    cand_data = []
    for img in cand_images:
        image = Image.open(img)
        attrs = extract_attributes_from_image(image)
        attrs["image"] = image
        attrs["name"] = img.name
        attrs["design_description"] = " ".join(str(v) for k, v in attrs.items() if k not in ["image", "name"])
        cand_data.append(attrs)

    st.success("Attributes extracted for all images!")

    st.subheader("📊 Scoring Candidate Designs")
    df_candidates = pd.DataFrame(cand_data)
    df_competitors = pd.DataFrame(comp_data)

    df_candidates['design_description'] = df_candidates.get('design_description', pd.Series("", index=df_candidates.index))
    df_competitors['design_description'] = df_competitors.get('design_description', pd.Series("", index=df_competitors.index))

    df_past = pd.DataFrame(columns=df_candidates.columns)

    def normalize(series):
        try:
            if isinstance(series, pd.Series):
                if series.max() == series.min():
                    return pd.Series(0.5, index=series.index)
                return (series - series.min()) / (series.max() - series.min())
            else:
                return pd.Series(series).apply(lambda x: 0.5)
        except Exception:
            return pd.Series(0.5, index=range(len(series)))

    scored_df = compute_buyability_scores(df_candidates, df_past, df_competitors)
    top_recommendations = recommend_top_n(scored_df, n=12)

    st.subheader("🏆 Top Recommendations")
    for _, item in top_recommendations.iterrows():
        with st.container():
            cols = st.columns([1, 2, 5])
            with cols[0]:
                st.image(item['image'], caption=item['name'], width=150)
            with cols[1]:
                st.metric(label="Score", value=f"{item['buyability_score']:.2f}")
            with cols[2]:
                st.markdown("<br>" + "<br>".join([f"**{k}:** {v}" for k, v in item.drop(['image', 'name', 'buyability_score']).to_dict().items()]), unsafe_allow_html=True)

    st.subheader("🖼️ Visual Comparison")
    def visualize_comparison(scored_df, df_competitors):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(scored_df['buyability_score'], bins=10, alpha=0.7, label='Candidates', color='skyblue')
        ax.set_title('Buyability Score Distribution')
        ax.set_xlabel('Score')
        ax.set_ylabel('Frequency')
        ax.legend()
        return fig

    fig = visualize_comparison(scored_df, df_competitors)
    st.pyplot(fig)

else:
    st.info("Upload images and click the button in the sidebar to begin analysis.")
