import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

def show_image_grid(df, title_col='Title', image_col='Image URL'):
    st.markdown("#### Preview of Recommended Options")
    for i in range(0, len(df), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(df):
                with cols[j]:
                    st.image(df.iloc[i + j][image_col], caption=df.iloc[i + j][title_col], use_column_width=True)

def plot_score_breakdown(df):
    st.markdown("#### Score Breakdown")
    breakdown_cols = ['Market Newness Score', 'Brand Newness Score', 'Variety Score', 'Completeness Score']
    fig, ax = plt.subplots(figsize=(10, 5))
    df[breakdown_cols].plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Buyability Score Breakdown by Option")
    ax.set_xlabel("Option Index")
    ax.set_ylabel("Score Contribution")
    st.pyplot(fig)

def visualize_heatmap(df):
    st.markdown("#### Buyability Heatmap")
    score_matrix = df[['Market Newness Score', 'Brand Newness Score', 'Variety Score', 'Completeness Score']]
    plt.figure(figsize=(10, 6))
    sns.heatmap(score_matrix, annot=True, cmap="YlGnBu", fmt=".2f")
    st.pyplot(plt.gcf())

def plot_attribute_distribution(df):
    st.markdown("#### Attribute Distribution")
    for attr in ['Color', 'Length', 'Style', 'Material', 'Occasion']:
        if attr in df.columns:
            fig, ax = plt.subplots()
            df[attr].value_counts().plot(kind='bar', ax=ax, title=f"{attr} Distribution")
            st.pyplot(fig)

def plot_market_comparison(df1, df2):
    st.markdown("#### Market Comparison: Brand vs Brand")
    common_attrs = ['Color', 'Length', 'Style', 'Material', 'Occasion']
    for attr in common_attrs:
        if attr in df1.columns and attr in df2.columns:
            fig, ax = plt.subplots()
            df1[attr].value_counts(normalize=True).plot(kind='bar', alpha=0.6, label='Brand A', ax=ax)
            df2[attr].value_counts(normalize=True).plot(kind='bar', alpha=0.6, label='Brand B', ax=ax, color='orange')
            ax.set_title(f"{attr} Comparison")
            ax.legend()
            st.pyplot(fig)

def plot_candidate_vs_brands_comparison(candidates, brands):
    st.markdown("#### Comparison: Candidates vs Competitor Brands")
    attributes = ['Color', 'Length', 'Style', 'Material', 'Occasion']
    for attr in attributes:
        if attr in candidates.columns and attr in brands.columns:
            fig, ax = plt.subplots()
            candidates[attr].value_counts(normalize=True).plot(kind='bar', label='Candidates', ax=ax)
            brands[attr].value_counts(normalize=True).plot(kind='bar', alpha=0.6, label='Market', ax=ax, color='green')
            ax.set_title(f"{attr} - Candidates vs Market")
            ax.legend()
            st.pyplot(fig)
