import streamlit as st
from PIL import Image
import os
from attribute_extractor import extract_attributes_from_image
from buyability_score import score_candidate_products, visualize_comparison

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")
st.title("🛍️ PickWise – Smarter Choices. Sharper Assortments.")

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
        comp_data.append({"name": img.name, "attributes": attrs, "image": image})

    cand_data = []
    for img in cand_images:
        image = Image.open(img)
        attrs = extract_attributes_from_image(image)
        cand_data.append({"name": img.name, "attributes": attrs, "image": image})

    st.success("Attributes extracted for all images!")

    st.subheader("📊 Scoring Candidate Designs")
    scored_candidates = score_candidate_products(cand_data, comp_data)

    st.subheader("🏆 Top Recommendations")
    for item in scored_candidates[:12]:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(item['image'], caption=item['name'], width=150)
        with col2:
            st.markdown(f"**Score:** {item['score']:.2f}<br>**Attributes:** {item['attributes']}", unsafe_allow_html=True)

    st.subheader("🖼️ Visual Comparison")
    fig = visualize_comparison(scored_candidates, comp_data)
    st.pyplot(fig)

else:
    st.info("Upload images and click the button in the sidebar to begin analysis.")
