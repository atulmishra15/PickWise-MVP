import pandas as pd
from PIL import Image
import io
import os
import csv
import numpy as np
from sklearn.preprocessing import LabelEncoder

# You can adjust these attributes based on what your model detects or your feature engineering
categories = ['Color', 'Material', 'Style', 'SleeveType', 'Neckline', 'Pattern']

def extract_attributes_from_image(image: Image) -> dict:
    """
    This function takes an image and extracts attributes like color, material, style, etc.
    This is a placeholder, you can replace this with an actual attribute extraction model.
    """
    # For demonstration, we will return random attributes; replace this with actual model logic
    return {
        'Color': 'Red',
        'Material': 'Cotton',
        'Style': 'Casual',
        'SleeveType': 'Short',
        'Neckline': 'V-Neck',
        'Pattern': 'Solid'
    }

def enrich_attributes_from_images(image_files: list) -> pd.DataFrame:
    """
    This function will take a list of image files and extract attributes from each one.
    It then returns the attributes as a DataFrame.
    """
    data = []
    for image_file in image_files:
        # Open the image file and extract attributes
        image = Image.open(image_file)
        attributes = extract_attributes_from_image(image)

        # Add the image path and attributes to the data list
        attributes['image_path'] = image_file.name  # Store the image filename for reference
        data.append(attributes)

    # Convert the list of attributes into a DataFrame
    df = pd.DataFrame(data)
    
    # Optional: Encode categorical columns to numeric values using LabelEncoder
    label_encoder = LabelEncoder()
    for col in categories:
        df[col] = label_encoder.fit_transform(df[col])

    return df

def enrich_and_export_attributes(image_files: list) -> pd.DataFrame:
    """
    This function will enrich attributes from images and save the resulting DataFrame as CSV.
    It will return the enriched DataFrame.
    """
    # Enrich the attributes from the uploaded images
    enriched_data = enrich_attributes_from_images(image_files)

    # Save the enriched attributes as a CSV
    enriched_data.to_csv("candidate_attributes.csv", index=False)

    # Return the enriched DataFrame
    return enriched_data
