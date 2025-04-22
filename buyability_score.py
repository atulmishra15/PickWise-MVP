import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
import streamlit as st

def tfidf_cosine_distance(base_set: pd.Series, candidates: pd.Series) -> np.ndarray:
    vectorizer = TfidfVectorizer()
    all_texts = pd.concat([base_set, candidates], ignore_index=True).fillna('')
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    base_vecs = tfidf_matrix[:len(base_set)]
    cand_vecs = tfidf_matrix[len(base_set):]
    distances = cosine_distances(cand_vecs, base_vecs)
    return distances.mean(axis=1)

def jaccard_diversity_score(df: pd.DataFrame, columns: list) -> np.ndarray:
    scores = []
    for idx, row in df.iterrows():
        similarity_sum = 0
        comparisons = 0
        for jdx, other in df.iterrows():
            if idx == jdx:
                continue
            similarity = sum(row[col] == other[col] for col in columns if col in df.columns)
            similarity_sum += similarity
            comparisons += 1
        scores.append(1 - (similarity_sum / (comparisons * len(columns))) if comparisons > 0 else 0)
    return np.array(scores)

def score_buyability(candidates: pd.DataFrame, brand_history: pd.DataFrame, competitors: pd.DataFrame) -> pd.DataFrame:
    # Streamlit sliders for interactive weight control
    st.sidebar.markdown("### 🧮 Weight Settings")
    wt_brand = st.sidebar.slider("Newness to Brand", 0.0, 1.0, 0.2)
    wt_market = st.sidebar.slider("Newness to Market", 0.0, 1.0, 0.4)
    wt_variety = st.sidebar.slider("Variety", 0.0, 1.0, 0.2)
    wt_completeness = st.sidebar.slider("Completeness", 0.0, 1.0, 0.2)

    candidates = candidates.copy()

    # Core attribute columns used in extraction
    attribute_cols = [
        'color', 'material', 'style', 'length', 'pattern',
        'neckline', 'sleeve_type', 'fit', 'occasion', 'print_type'
    ]
    used_columns = [col for col in attribute_cols if col in candidates.columns]

    # Distance-based scores
    brand_dist = tfidf_cosine_distance(brand_history['product_name'], candidates['product_name'])
    market_dist = tfidf_cosine_distance(competitors['product_name'], candidates['product_name'])

    # Variety score
    variety_score = jaccard_diversity_score(candidates, used_columns)

    # Completeness score: attribute coverage
    attr_spread = candidates[used_columns].nunique() / len(candidates)
    completeness_score = candidates.apply(
        lambda row: sum(row[col] in candidates[col].unique() for col in used_columns) / len(used_columns), axis=1
    )

    # Normalize all scores to [0, 1]
    def normalize(arr): return (arr - np.min(arr)) / (np.max(arr) - np.min(arr) + 1e-5)

    norm_brand = normalize(brand_dist)
    norm_market = normalize(market_dist)
    norm_variety = normalize(variety_score)
    norm_completeness = normalize(completeness_score)

    # Final weighted buyability score
    candidates['buyability_score'] = (
        wt_brand * norm_brand +
        wt_market * norm_market +
        wt_variety * norm_variety +
        wt_completeness * norm_completeness
    )

    # Optional: break out scores for debugging
    candidates['score_brand'] = norm_brand
    candidates['score_market'] = norm_market
    candidates['score_variety'] = norm_variety
    candidates['score_completeness'] = norm_completeness

    return candidates.sort_values(by='buyability_score', ascending=False)
