import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from sklearn.preprocessing import MultiLabelBinarizer

# Default weights (can be overridden via UI sliders)
DEFAULT_WEIGHTS = {
    "newness_to_market": 0.4,
    "newness_to_brand": 0.2,
    "variety": 0.2,
    "completeness": 0.2
}

def compute_buyability_scores(df: pd.DataFrame, past_brand_df: pd.DataFrame, competitor_df: pd.DataFrame, weights: dict = DEFAULT_WEIGHTS) -> pd.DataFrame:
    enriched_df = df.copy()

    # Extract and binarize relevant attributes
    attributes = ["style", "material", "color", "print", "length", "occasion", "neckline", "sleeve_type", "texture"]
    mlb = MultiLabelBinarizer()
    all_tags = enriched_df[attributes].fillna('').agg(lambda x: list(set(filter(None, x))), axis=1)
    tag_matrix = mlb.fit_transform(all_tags)

    # --- 1. Newness to Market ---
    comp_tags = competitor_df[attributes].fillna('').agg(lambda x: list(set(filter(None, x))), axis=1)
    comp_matrix = mlb.transform(comp_tags)
    dist_to_market = cosine_distances(tag_matrix, comp_matrix).mean(axis=1)

    # --- 2. Newness to Brand ---
    brand_tags = past_brand_df[attributes].fillna('').agg(lambda x: list(set(filter(None, x))), axis=1)
    brand_matrix = mlb.transform(brand_tags)
    dist_to_brand = cosine_distances(tag_matrix, brand_matrix).mean(axis=1)

    # --- 3. Variety Within Selection ---
    dist_within = cosine_distances(tag_matrix)
    diversity_scores = dist_within.mean(axis=1)

    # --- 4. Completeness Score (balance of attributes)
    def completeness(row):
        return np.mean([1 if row[attr] else 0 for attr in attributes])
    completeness_scores = enriched_df.apply(completeness, axis=1)

    # Weighted Final Score
    enriched_df["score_newness_market"] = dist_to_market
    enriched_df["score_newness_brand"] = dist_to_brand
    enriched_df["score_variety"] = diversity_scores
    enriched_df["score_completeness"] = completeness_scores

    enriched_df["buyability_score"] = (
        weights["newness_to_market"] * dist_to_market +
        weights["newness_to_brand"] * dist_to_brand +
        weights["variety"] * diversity_scores +
        weights["completeness"] * completeness_scores
    )

    return enriched_df.sort_values(by="buyability_score", ascending=False).reset_index(drop=True)


def recommend_top_n(df: pd.DataFrame, top_n: int = 12, prompt_filters: str = "") -> pd.DataFrame:
    # Simple text filter (future: NLP)
    prompt = prompt_filters.lower()
    if prompt:
        if "red" in prompt:
            df.loc[df['color'].str.contains("red", na=False), 'buyability_score'] += 0.05
        if "floral" in prompt and "less" in prompt:
            df.loc[df['print'].str.contains("floral", na=False), 'buyability_score'] -= 0.05
        if "formal" in prompt:
            df.loc[df['occasion'].str.contains("formal", na=False), 'buyability_score'] += 0.05

    top_df = df.sort_values(by="buyability_score", ascending=False).head(top_n).copy()
    top_df['tags'] = top_df.apply(lambda row: list(filter(None, [row.get(attr) for attr in ["style", "material", "color", "print", "length", "occasion"]])), axis=1)
    return top_df
