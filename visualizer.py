import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from PIL import Image
import io

def show_image_grid(df, image_col="image", title_col="title"):
    st.markdown("#### Image Grid")
    cols = st.columns(4)
    for idx, row in df.iterrows():
        with cols[idx % 4]:
            try:
                if isinstance(row[image_col], str):
                    img = Image.open(row[image_col])
                elif isinstance(row[image_col], (io.BytesIO, bytes)):
                    img = Image.open(io.BytesIO(row[image_col]))
                else:
                    img = row[image_col]
                st.image(img, caption=row.get(title_col, ""), use_column_width=True)
            except Exception as e:
                st.write("Image not available")

def plot_score_breakdown(df):
    st.markdown("#### Buyability Score Breakdown")
    if 'Buyability Score' not in df.columns:
        st.warning("No score breakdown available.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    score_columns = [col for col in df.columns if 'score' in col.lower() and col != 'Buyability Score']
    df_melt = df.melt(id_vars=["title"], value_vars=score_columns, var_name="Criteria", value_name="Score Component")
    sns.barplot(data=df_melt, x="title", y="Score Component", hue="Criteria", ax=ax)
    ax.set_title("Score Component Breakdown by Product")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

def visualize_heatmap(df):
    st.markdown("#### Attribute Heatmap")
    if df.empty:
        st.warning("No data to display.")
        return

    numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric attributes for heatmap.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap of Attributes")
    st.pyplot(fig)

def plot_attribute_distribution(df):
    st.markdown("#### Attribute Distribution")
    attr_cols = ['color', 'length', 'material', 'print', 'occasion', 'style']
    for attr in attr_cols:
        if attr in df.columns:
            fig, ax = plt.subplots()
            df[attr].value_counts().plot(kind='bar', ax=ax)
            ax.set_title(f"Distribution of {attr.capitalize()}")
            st.pyplot(fig)

def plot_market_comparison(candidates_df, competitors_df):
    st.markdown("#### Market Positioning: Candidates vs Competitors")
    common_attrs = ['color', 'length', 'style']
    for attr in common_attrs:
        if attr in candidates_df.columns and attr in competitors_df.columns:
            fig, ax = plt.subplots()
            cand_counts = candidates_df[attr].value_counts()
            comp_counts = competitors_df[attr].value_counts()
            combined = pd.DataFrame({
                "Candidates": cand_counts,
                "Competitors": comp_counts
            }).fillna(0)
            combined.plot(kind="bar", ax=ax)
            ax.set_title(f"{attr.capitalize()} Comparison")
            st.pyplot(fig)
