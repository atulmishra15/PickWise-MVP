import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def visualize_buyability_breakdown(scored_candidates: pd.DataFrame):
    """Displays bar chart of buyability scores broken down by candidate."""
    if scored_candidates is None or scored_candidates.empty:
        st.warning("No candidate scores available for visualization.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    scored_sorted = scored_candidates.sort_values(by="buyability_score", ascending=False)
    sns.barplot(x="image_name", y="buyability_score", data=scored_sorted, palette="viridis", ax=ax)
    ax.set_title("Buyability Score per Candidate")
    ax.set_xlabel("Candidate Image")
    ax.set_ylabel("Score")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
    plt.clf()

def visualize_candidate_vs_market(candidates: pd.DataFrame, market: pd.DataFrame):
    """Displays attribute heatmap comparing candidate vs market distribution."""
    if candidates.empty or market.empty:
        st.warning("Insufficient data for candidate vs market visualization.")
        return

    comparison_attributes = ["color", "length", "style", "material", "pattern", "sleeve_type", "neckline"]

    candidate_summary = candidates[comparison_attributes].apply(lambda x: x.value_counts()).fillna(0)
    market_summary = market[comparison_attributes].apply(lambda x: x.value_counts()).fillna(0)

    candidate_norm = candidate_summary.div(candidate_summary.sum(axis=0), axis=1).fillna(0)
    market_norm = market_summary.div(market_summary.sum(axis=0), axis=1).fillna(0)

    combined = pd.concat([
        candidate_norm.add_suffix(" (Candidate)"),
        market_norm.add_suffix(" (Market)")
    ], axis=1).fillna(0)

    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(combined, annot=True, cmap="YlGnBu", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Candidate vs Market Attribute Distribution")
    st.pyplot(fig)
    plt.clf()

def visualize_brand_vs_brand(markets: dict):
    """Displays a heatmap comparing multiple brand distributions."""
    if not markets or len(markets) < 2:
        st.warning("Need at least two brands to compare.")
        return

    comparison_attributes = ["color", "length", "style", "material", "pattern", "sleeve_type", "neckline"]

    summaries = {}
    for brand, df in markets.items():
        summary = df[comparison_attributes].apply(lambda x: x.value_counts()).fillna(0)
        summaries[brand] = summary.div(summary.sum(axis=0), axis=1).fillna(0)

    combined = pd.concat([
        summaries[brand].add_suffix(f" ({brand})") for brand in summaries
    ], axis=1).fillna(0)

    fig, ax = plt.subplots(figsize=(16, 12))
    sns.heatmap(combined, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Brand vs Brand Attribute Distribution")
    st.pyplot(fig)
    plt.clf()
