# buyability_score.py

import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

def preprocess_features(df, categorical_cols, numerical_cols):
    enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    scaled = MinMaxScaler()

    cat_features = enc.fit_transform(df[categorical_cols])
    num_features = scaled.fit_transform(df[numerical_cols])

    return np.hstack([cat_features, num_features])

def compute_distance_matrix(A, B):
    return cosine_distances(A, B)

def compute_variety_score(option_features):
    # Measure how distinct items are from each other
    dists = cosine_distances(option_features)
    avg_distance = np.mean(dists)
    return avg_distance

def compute_completeness_score(df, attr_cols):
    completeness_score = 0
    for col in attr_cols:
        val_counts = df[col].nunique()
        completeness_score += val_counts
    max_possible = len(attr_cols) * 5  # assuming good coverage if at least 5 values/attr
    return min(completeness_score / max_possible, 1.0)

def calculate_buyability_score(candidate_df, past_brand_df, market_df, attr_cols, numerical_cols):
    candidate_feats = preprocess_features(candidate_df, attr_cols, numerical_cols)
    brand_feats = preprocess_features(past_brand_df, attr_cols, numerical_cols)
    market_feats = preprocess_features(market_df, attr_cols, numerical_cols)

    # Newness to Brand (lower similarity = higher score)
    brand_dist = np.mean(compute_distance_matrix(candidate_feats, brand_feats), axis=1)

    # Newness to Market
    market_dist = np.mean(compute_distance_matrix(candidate_feats, market_feats), axis=1)

    # Variety (overall)
    variety = compute_variety_score(candidate_feats)

    # Completeness (attribute coverage)
    completeness = compute_completeness_score(candidate_df, attr_cols)

    # Final Weighted Score
    scores = (
        0.2 * brand_dist +
        0.4 * market_dist +
        0.2 * variety +
        0.2 * completeness
    )
    candidate_df['buyability_score'] = scores
    return candidate_df.sort_values(by='buyability_score', ascending=False)
# Implement distance-based buyability scoring here using brand and market comparison
