import pandas as pd
from PIL import Image
import torch
from torchvision import transforms
from transformers import BlipProcessor, BlipForConditionalGeneration
import spacy
import re

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()

# Load spaCy NLP model for attribute parsing
nlp = spacy.load("en_core_web_sm")

categories = ['Color', 'Material', 'Style', 'SleeveType', 'Neckline', 'Pattern']

# Helper to extract caption from image
def generate_caption(image: Image.Image) -> str:
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# Attribute keyword patterns
attribute_keywords = {
    'Color': ["red", "blue", "green", "yellow", "black", "white", "pink", "purple", "orange", "beige", "brown", "grey"],
    'Material': ["cotton", "denim", "linen", "leather", "silk", "wool", "polyester"],
    'Style': ["casual", "formal", "boho", "elegant", "sporty", "classic"],
    'SleeveType': ["sleeveless", "short sleeve", "long sleeve", "cap sleeve", "three-quarter sleeve"],
    'Neckline': ["v-neck", "round neck", "boat neck", "collared", "square neck"],
    'Pattern': ["solid", "floral", "striped", "checked", "polka dot", "printed"]
}

# NLP-based parser for attributes
def parse_attributes_from_caption(caption: str) -> dict:
    doc = nlp(caption.lower())
    attributes = {cat: "Unknown" for cat in categories}

    for token in doc:
        for attr, keywords in attribute_keywords.items():
            for keyword in keywords:
                if keyword in token.text:
                    attributes[attr] = keyword.capitalize()

    return attributes

def extract_attributes_from_image(image: Image) -> dict:
    caption = generate_caption(image)
    attributes = parse_attributes_from_caption(caption)
    return attributes

def enrich_attributes_from_images(image_files: list) -> pd.DataFrame:
    data = []
    for image_file in image_files:
        image = Image.open(image_file)
        attributes = extract_attributes_from_image(image)
        attributes['image_path'] = image_file.name
        data.append(attributes)

    df = pd.DataFrame(data)
    return df

def enrich_and_export_attributes(image_files: list) -> pd.DataFrame:
    enriched_data = enrich_attributes_from_images(image_files)
    enriched_data.to_csv("candidate_attributes.csv", index=False)
    return enriched_data
