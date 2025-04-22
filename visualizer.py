import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Function to visualize the breakdown of buyability score
def visualize_buyability_breakdown(scored_candidates):
    st.header("Buyability Breakdown")

    # Prepare the data
    buyability_data = scored_candidates[['image_name', 'buyability_score']]
    
    # Set the figure size
    plt.figure(figsize=(10, 6))
    
    # Create a bar plot
    sns.barplot(x='image_name', y='buyability_score', data=buyability_data)
    plt.xticks(rotation=90)
    plt.title('Buyability Score Breakdown for Candidates')
    plt.xlabel('Candidate Design')
    plt.ylabel('Buyability Score')

    # Show the plot
    st.pyplot(plt)

# Function to compare candidates with market data (brands)
def visualize_candidate_vs_market(candidate_data, all_market_data):
    st.header("Candidate vs Market Comparison")
    
    # Assuming that candidate_data and all_market_data contain the necessary columns for comparison
    merged_data = pd.merge(candidate_data, all_market_data, on=["color", "occasion", "print", "pattern", "texture"], how="left")
    
    # Set the figure size
    plt.figure(figsize=(10, 6))
    
    # Create a scatter plot to compare the attributes
    sns.scatterplot(data=merged_data, x='buyability_score', y='market_score', hue='brand', style='brand', palette='Set1')

    plt.title('Candidates vs Market Comparison')
    plt.xlabel('Candidate Buyability Score')
    plt.ylabel('Market Competitor Score')

    # Show the plot
    st.pyplot(plt)

# Function to compare different brands with each other
def visualize_brand_vs_brand(brand_data):
    st.header("Brand vs Brand Comparison")

    # Merge all brand data into a single dataframe for comparison
    all_brands_data = pd.concat(brand_data.values(), ignore_index=True)

    # Set the figure size
    plt.figure(figsize=(10, 6))
    
    # Create a boxplot to compare brands
    sns.boxplot(x='brand', y='buyability_score', data=all_brands_data, palette='Set2')

    plt.title('Brand vs Brand Buyability Score Comparison')
    plt.xlabel('Brand')
    plt.ylabel('Buyability Score')

    # Show the plot
    st.pyplot(plt)
