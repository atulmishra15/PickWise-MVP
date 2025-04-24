import pandas as pd
from PIL import Image, UnidentifiedImageError
import torch
from torchvision import transforms
from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel
import spacy
import spacy.cli
import re
import streamlit as st

# Cached model loaders for Streamlit performance
@st.cache_resource
def load_blip_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    model.eval()
    return processor, model

@st.cache_resource
def load_clip_model():
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    model.eval()
    return processor, model

@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

# Load models
processor_blip, model_blip = load_blip_model()
clip_processor, clip_model = load_clip_model()
nlp = load_spacy_model()

categories = ['Color', 'Material', 'Style', 'SleeveType', 'Neckline', 'Pattern']

attribute_keywords = {
    'Color': ["red", "blue", "green", "yellow", "black", "white", "pink", "purple", "orange", "beige", "brown", "grey"],
    'Material': ["cotton", "denim", "linen", "leather", "silk", "wool", "polyester"],
    'Style': ["casual", "formal", "boho", "elegant", "sporty", "classic"],
    'SleeveType': ["sleeveless", "short sleeve", "long sleeve", "cap sleeve", "three-quarter sleeve"],
    'Neckline': ["v-neck", "round neck", "boat neck", "collared", "square neck"],
    'Pattern': ["solid", "floral", "striped", "checked", "polka dot", "printed"]
}

# Generate caption using BLIP Large
def generate_caption(image: Image.Image) -> str:
    inputs = processor_blip(images=image, return_tensors="pt")
    with torch.no_grad():
        out = model_blip.generate(**inputs.to("cpu"))
    caption = processor_blip.decode(out[0], skip_special_tokens=True)
    return caption

# Fallback CLIP tag suggestion
def generate_clip_tags(image: Image.Image) -> list:
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = clip_model.get_image_features(**inputs.to("cpu"))
    return outputs.tolist()  # Placeholder for future label projection

# Parse attributes from caption using NLP
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
        try:
            image = Image.open(image_file)
            attributes = extract_attributes_from_image(image)
            attributes['image_path'] = image_file.name
            data.append(attributes)
        except UnidentifiedImageError:
            st.warning(f"Could not process {image_file.name}: Unrecognized image format")
        except Exception as e:
            st.warning(f"Error processing {image_file.name}: {e}")

    df = pd.DataFrame(data)
    return df

def enrich_and_export_attributes(image_files: list) -> pd.DataFrame:
    enriched_data = enrich_attributes_from_images(image_files)
    enriched_data.to_csv("candidate_attributes.csv", index=False)
    return enriched_data
