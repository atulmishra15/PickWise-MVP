import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# This function will plot pricing distribution based on the brand and category
def plot_price_distribution(product_data):
    # Create a DataFrame from the product data
    df = pd.DataFrame(product_data)

    # Check if the 'price' column exists
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Ensure prices are numeric

        # Set up the figure and plot
        plt.figure(figsize=(10, 6))
        sns.histplot(df['price'], kde=True, bins=20, color='blue')
        plt.title('Pricing Distribution', fontsize=16)
        plt.xlabel('Price', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)

        # Show the plot
        st.pyplot(plt)

# This function will visualize the assortment attributes (e.g., color, material, etc.)
def plot_assortment(product_data, attribute):
    df = pd.DataFrame(product_data)

    # Check if the attribute column exists in the data
    if attribute in df.columns:
        # Create a bar chart for the selected attribute
        plt.figure(figsize=(10, 6))
        sns.countplot(x=attribute, data=df, palette='viridis')
        plt.title(f'{attribute.capitalize()} Distribution', fontsize=16)
        plt.xlabel(attribute.capitalize(), fontsize=12)
        plt.ylabel('Count', fontsize=12)

        st.pyplot(plt)

# Streamlit interface to select brands, categories, and other filters
def visualize_assortment():
    # Sample product data for testing (replace with actual scraped data)
    sample_data = [
        {"name": "Product 1", "price": 29.99, "color": "Red", "material": "Cotton", "occasion": "Casual"},
        {"name": "Product 2", "price": 49.99, "color": "Blue", "material": "Polyester", "occasion": "Formal"},
        {"name": "Product 3", "price": 19.99, "color": "Green", "material": "Linen", "occasion": "Casual"},
        {"name": "Product 4", "price": 39.99, "color": "Black", "material": "Wool", "occasion": "Casual"},
        {"name": "Product 5", "price": 59.99, "color": "Red", "material": "Leather", "occasion": "Formal"},
        # Add more products for testing...
    ]

    # Convert sample data into a dataframe for easier manipulation
    df = pd.DataFrame(sample_data)

    st.title("Product Assortment and Pricing Analysis")

    # Allow the user to select the brand and category for analysis
    brand = st.selectbox("Select Brand", ["MaxFashion", "Zara", "Shein", "H&M", "Splash"])
    category = st.selectbox("Select Category", ["Dresses", "Handbags", "T-Shirts", "Shoes", "Kidswear"])

    st.write(f"Showing data for {brand} in {category} category")

    # Display product data (you would replace this with actual scraped data later)
    st.write(df)

    # Allow users to select which attribute they want to analyze
    attribute = st.selectbox("Select Attribute to Analyze", ["color", "material", "occasion"])

    # Show the assortment distribution for the selected attribute
    plot_assortment(sample_data, attribute)

    # Pricing distribution visualization
    st.subheader("Price Distribution")
    plot_price_distribution(sample_data)

# Run the Streamlit app
if __name__ == "__main__":
    visualize_assortment()
