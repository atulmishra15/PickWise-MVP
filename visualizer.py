import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def plot_attribute_distribution(df, attribute: str, title: str = ""):
    if attribute not in df.columns:
        st.warning(f"{attribute} not found in data.")
        return

    plt.figure(figsize=(10, 4))
    sns.countplot(y=attribute, data=df, order=df[attribute].value_counts().index, palette="pastel")
    plt.title(title or f"{attribute.capitalize()} Distribution")
    st.pyplot(plt.gcf())
    plt.clf()

def compare_uploaded_vs_scraped(uploaded_df, scraped_df, attribute: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    uploaded_counts = uploaded_df[attribute].value_counts(normalize=True).sort_index()
    scraped_counts = scraped_df[attribute].value_counts(normalize=True).sort_index()
    combined = pd.DataFrame({'Uploaded': uploaded_counts, 'Scraped': scraped_counts}).fillna(0)

    combined.plot(kind='bar', ax=ax, width=0.7)
    ax.set_title(f"Comparison of {attribute} Distribution")
    ax.set_ylabel("Proportion")
    st.pyplot(fig)
    plt.clf()

def show_buyability_distribution(df):
    plt.figure(figsize=(8, 4))
    sns.histplot(df["buyability_score"], bins=20, kde=True, color='skyblue')
    plt.title("Buyability Score Distribution")
    plt.xlabel("Score")
    st.pyplot(plt.gcf())
    plt.clf()

def show_price_vs_score(df):
    if "price" not in df.columns or "buyability_score" not in df.columns:
        st.warning("Price or score columns missing.")
        return
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="price", y="buyability_score", hue="color", palette="tab10", ax=ax)
    ax.set_title("Price vs Buyability Score")
    st.pyplot(fig)
    plt.clf()
# Create Streamlit visualizations of attribute spread, comparisons, etc.
