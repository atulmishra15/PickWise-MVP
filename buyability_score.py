import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from sklearn.feature_extraction.text import TfidfVectorizer

DEFAULT_WEIGHTS = {
    "newness_to_market": 0.4,
    "newness_to_brand": 0.2,
    "variety": 0.2,
    "completeness": 0.2
}

def compute_newness_to_market(df_new, df_comp):import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances

DEFAULT_WEIGHTS = {
    "newness_brand": 0.2,
    "newness_market": 0.4,
    "variety": 0.2,
    "completeness": 0.2,
}

def normalize(series):
    try:
        series = pd.Series(series)
        if series.max() == series.min():
            return pd.Series(0.5, index=series.index)
        return (series - series.min()) / (series.max() - series.min())
    except Exception:
        return pd.Series(0.5, index=range(len(series)))

def compute_text_distance(descriptions1, descriptions2):
    corpus = descriptions1.tolist() + descriptions2.tolist()
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus)
    dist_matrix = cosine_distances(tfidf[:len(descriptions1)], tfidf[len(descriptions1):])
    return dist_matrix

def compute_newness_to_brand(df_new, df_past):
    if df_past.empty:
        return np.full(len(df_new), 0.5)
    dist_matrix = compute_text_distance(df_new['design_description'], df_past['design_description'])
    return dist_matrix.min(axis=1)

def compute_newness_to_market(df_new, df_comp):
    if df_comp.empty:
        return np.full(len(df_new), 0.5)
    dist_matrix = compute_text_distance(df_new['design_description'], df_comp['design_description'])
    return dist_matrix.min(axis=1)

def compute_variety(df):
    if 'design_description' not in df:
        return np.full(len(df), 0.5)
    dist_matrix = compute_text_distance(df['design_description'], df['design_description'])
    mean_dists = dist_matrix.mean(axis=1)
    return mean_dists

def compute_completeness(df):
    if df.empty:
        return np.full(len(df), 0.5)
    attributes = ['color', 'style', 'length', 'occasion', 'material', 'print', 'pattern']
    scores = []
    for attr in attributes:
        diversity = df[attr].nunique() if attr in df else 1
        scores.append(diversity / max(1, len(df)))
    return np.full(len(df), np.mean(scores))

def compute_buyability_scores(df_new, df_past, df_comp, weights=DEFAULT_WEIGHTS):
    df = df_new.copy()
    df['score_newness_brand'] = normalize(compute_newness_to_brand(df, df_past))
    df['score_newness_market'] = normalize(compute_newness_to_market(df, df_comp))
    df['score_variety'] = normalize(compute_variety(df))
    df['score_completeness'] = compute_completeness(df)

    df['buyability_score'] = (
        weights['newness_brand'] * df['score_newness_brand'] +
        weights['newness_market'] * df['score_newness_market'] +
        weights['variety'] * df['score_variety'] +
        weights['completeness'] * df['score_completeness']
    )
    return df

def recommend_top_n(scored_df, n=12):
    return scored_df.sort_values(by='buyability_score', ascending=False).head(n)

    tfidf = TfidfVectorizer()
    new_vecs = tfidf.fit_transform(df_new["design_description"].fillna(""))
    comp_vecs = tfidf.transform(df_comp["design_description"].fillna(""))
    distances = cosine_distances(new_vecs, comp_vecs).mean(axis=1)
    return distances

def compute_newness_to_brand(df_new, df_past):
    tfidf = TfidfVectorizer()
    new_vecs = tfidf.fit_transform(df_new["design_description"].fillna(""))
    past_vecs = tfidf.transform(df_past["design_description"].fillna(""))
    distances = cosine_distances(new_vecs, past_vecs).mean(axis=1)
    return distances

def compute_variety(df):
    tfidf = TfidfVectorizer()
    vecs = tfidf.fit_transform(df["design_description"].fillna(""))
    sim_matrix = cosine_distances(vecs)
    avg_distances = sim_matrix.mean(axis=1)
    return avg_distances

def compute_completeness(df):
    attrs = ["color", "length", "occasion", "style", "material", "print"]
    comp_scores = []
    for attr in attrs:
        diversity = df[attr].nunique() / (df.shape[0] + 1e-5)
        comp_scores.append(diversity)
    comp_array = np.array(comp_scores).mean()
    return np.repeat(comp_array, df.shape[0])

def normalize(series):
    if series.max() == series.min():
        return pd.Series(0.5, index=series.index)
    return (series - series.min()) / (series.max() - series.min())

def compute_buyability_scores(df_new, df_past, df_comp, weights=DEFAULT_WEIGHTS):
    df = df_new.copy()
    df["score_newness_market"] = normalize(compute_newness_to_market(df, df_comp))
    df["score_newness_brand"] = normalize(compute_newness_to_brand(df, df_past))
    df["score_variety"] = normalize(compute_variety(df))
    df["score_completeness"] = normalize(pd.Series(compute_completeness(df)))

    df["buyability_score"] = (
        df["score_newness_market"] * weights["newness_to_market"] +
        df["score_newness_brand"] * weights["newness_to_brand"] +
        df["score_variety"] * weights["variety"] +
        df["score_completeness"] * weights["completeness"]
    )
    return df.sort_values("buyability_score", ascending=False)

def recommend_top_n(df, n=12, prompt=""):
    if prompt:
        prompt = prompt.lower()
        mask = df["design_description"].fillna("").str.lower().str.contains(prompt)
        df_prompted = df[mask].copy()
        if df_prompted.shape[0] >= n:
            return df_prompted.head(n)
        else:
            return pd.concat([df_prompted, df[~mask]]).drop_duplicates().head(n)
    return df.head(n)
