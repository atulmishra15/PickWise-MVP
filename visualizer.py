import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def show_score_breakdown_chart(df: pd.DataFrame):
    st.subheader("📊 Score Breakdown by Product")
    score_cols = ["score_newness_market", "score_newness_brand", "score_variety", "score_completeness"]
    fig, ax = plt.subplots(figsize=(12, 6))
    df[score_cols].plot(kind='bar', stacked=True, ax=ax, legend=True)
    ax.set_title("Score Component Breakdown (Top Recommendations)")
    ax.set_ylabel("Score Contribution")
    ax.set_xlabel("Product Index")
    st.pyplot(fig)

def show_attribute_heatmap(df: pd.DataFrame):
    st.subheader("🌈 Attribute Coverage Heatmap")
    attr_cols = ["color", "material", "style", "occasion", "print", "length"]
    attr_coverage = pd.DataFrame(columns=attr_cols)

    for attr in attr_cols:
        attr_coverage[attr] = df[attr].fillna("").apply(lambda x: x if isinstance(x, list) else [x])
    binarized = pd.DataFrame()

    for attr in attr_cols:
        exploded = attr_coverage[attr].explode().str.lower()
        bin_counts = exploded.value_counts().head(10)
        binarized = pd.concat([binarized, bin_counts], axis=1)

    binarized.columns = attr_cols[:len(binarized.columns)]
    binarized = binarized.fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(binarized.T, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5, ax=ax)
    ax.set_title("Attribute Heatmap (Top 10 Values per Attribute)")
    st.pyplot(fig)

def show_diversity_matrix(df: pd.DataFrame, distance_matrix: pd.DataFrame):
    st.subheader("🧬 Diversity Between Selected Products")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(distance_matrix, cmap="coolwarm", square=True, annot=False, ax=ax)
    ax.set_title("Pairwise Diversity (Cosine Distance)")
    st.pyplot(fig)
