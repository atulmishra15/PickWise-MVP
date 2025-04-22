import streamlit as st
import pandas as pd
import plotly.express as px
from attribute_extraction import extract_attributes
from buyability_score import score_buyability
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="PickWise – Smarter Choices. Sharper Assortments.", layout="wide")
st.title("👗 PickWise – Smarter Choices. Sharper Assortments.")

# Sidebar Controls
st.sidebar.header("📥 Upload CSVs")
candidate_file = st.sidebar.file_uploader("Upload candidate designs", type=["csv"])
brand_file = st.sidebar.file_uploader("Upload brand history", type=["csv"])
competitor_file = st.sidebar.file_uploader("Upload competitor assortment", type=["csv"])
top_n = st.sidebar.slider("🎯 Select Top N Recommendations", 1, 20, 12)

# Prompt input for refining results (UI only)
st.sidebar.header("🎨 Refinement Prompt")
user_prompt = st.sidebar.text_area("Give us a direction", placeholder="e.g., more reds, fewer florals, longer lengths...")

# Main Execution
if candidate_file and brand_file and competitor_file:
    with st.spinner("🔍 Processing..."):
        candidates_df = pd.read_csv(candidate_file)
        brand_df = pd.read_csv(brand_file)
        competitor_df = pd.read_csv(competitor_file)

        # Extract attributes
        st.subheader("🔎 Step 1: Attribute Extraction")
        enriched_candidates = extract_attributes(candidates_df)
        st.success("✅ Attributes extracted")

        # Score buyability
        st.subheader("📊 Step 2: Buyability Scoring")
        scored_df = score_buyability(enriched_candidates, brand_df, competitor_df)
        top_df = scored_df.sort_values(by="buyability_score", ascending=False).head(top_n)
        st.success("✅ Scored and ranked")

        # Show Top N with Images
        st.subheader(f"🏆 Top {top_n} Recommendations")
        for _, row in top_df.iterrows():
            cols = st.columns([1, 2])
            try:
                response = requests.get(row['image_url'])
                img = Image.open(BytesIO(response.content))
                cols[0].image(img, width=150)
            except:
                cols[0].warning("No Image")
            with cols[1]:
                st.markdown(f"**{row['product_name']}**")
                st.markdown(f"Score: `{row['buyability_score']:.2f}`")
                st.markdown(f"• Brand Newness: `{row['score_brand']:.2f}`")
                st.markdown(f"• Market Newness: `{row['score_market']:.2f}`")
                st.markdown(f"• Variety: `{row['score_variety']:.2f}`")
                st.markdown(f"• Completeness: `{row['score_completeness']:.2f}`")

        # Score Breakdown Visualization
        st.subheader("📈 Score Breakdown – Stacked View")
        breakdown = top_df[['product_name', 'score_brand', 'score_market', 'score_variety', 'score_completeness']].melt(
            id_vars='product_name', var_name='Score Type', value_name='Score'
        )
        fig = px.bar(
            breakdown,
            x="product_name",
            y="Score",
            color="Score Type",
            title="Buyability Score Components",
            barmode="stack"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Attribute Heatmap
        st.subheader("🧪 Attribute Variety Heatmap")
        attribute_cols = [col for col in enriched_candidates.columns if col.startswith('attr_')]
        attr_counts = enriched_candidates[attribute_cols].apply(pd.Series.value_counts).fillna(0).astype(int)
        fig2 = px.imshow(attr_counts, labels=dict(x="Attribute Value", y="Attribute Type", color="Frequency"),
                         title="Attribute Distribution Across Candidate Set")
        st.plotly_chart(fig2, use_container_width=True)

        # Download CSV
        st.download_button("📥 Download Top N CSV", top_df.to_csv(index=False), file_name="top_recommendations.csv")

else:
    st.info("Please upload all three datasets (candidate, brand, competitor) to get started.")

st.markdown("---")
st.caption("Built with ❤️ by PickWise · v1 MVP")
