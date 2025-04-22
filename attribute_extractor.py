import os
import pandas as pd
from PIL import Image
import random
from datetime import datetime

def detect_attributes_from_filename(name):
    name = name.lower()
    category_specific = {
        "dress": {
            "length": ["short", "midi", "long"],
            "silhouette": ["a-line", "bodycon", "wrap", "fit & flare", "shift"],
            "neckline": ["v-neck", "round", "collar", "high-neck"],
            "sleeve_type": ["sleeveless", "short", "long", "puff", "cap"]
        },
        "handbag": {
            "material": ["leather", "canvas", "synthetic", "jute"],
            "closure_type": ["zipper", "magnetic", "buckle", "drawstring"],
            "pattern": ["plain", "quilted", "printed", "woven"],
            "detailing": ["studs", "fringe", "embroidery", "chains"]
        },
        "t-shirt": {
            "sleeve_type": ["short", "long", "cap", "raglan"],
            "neckline": ["crew neck", "v-neck", "polo", "scoop"],
            "print": ["graphic", "striped", "solid", "logo"],
            "material": ["cotton", "jersey", "polyester"]
        }
    }

    detected_category = "dress"  # Default fallback
    if "handbag" in name:
        detected_category = "handbag"
    elif "tshirt" in name or "t-shirt" in name or "tee" in name:
        detected_category = "t-shirt"

    base_attributes = {
        "color": random.choice(["red", "blue", "black", "white", "green", "pink", "yellow"]),
        "occasion": random.choice(["casual", "formal", "party", "work"]),
        "print": random.choice(["solid", "floral", "striped", "graphic", "abstract"]),
        "pattern": random.choice(["plain", "checks", "animal", "polka", "geom"]),
        "texture": random.choice(["ribbed", "pleated", "ruched", "sheer", "quilted"]),
        "detailing": random.choice(["ruffles", "embroidery", "cutouts", "lace", "sequins"])
    }

    specific = category_specific.get(detected_category, {})
    for key, options in specific.items():
        base_attributes[key] = random.choice(options)

    return base_attributes

def enrich_attributes_from_images(images_or_df):
    enriched_data = []
    if isinstance(images_or_df, list):
        for image_file in images_or_df:
            try:
                image_name = image_file.name
                attrs = detect_attributes_from_filename(image_name)
                attrs["source"] = "candidate"
                attrs["image_name"] = image_name
                enriched_data.append(attrs)
            except Exception as e:
                print(f"Error processing {image_file.name}: {e}")
    elif isinstance(images_or_df, pd.DataFrame):
        for _, row in images_or_df.iterrows():
            name = row.get("image_name") or row.get("name") or f"product_{datetime.now().timestamp()}"
            attrs = detect_attributes_from_filename(name)
            attrs.update(row.to_dict())
            enriched_data.append(attrs)

    return pd.DataFrame(enriched_data)

def enrich_and_export_attributes(images_or_df, export_path=None):
    df = enrich_attributes_from_images(images_or_df)
    if export_path:
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        df.to_csv(export_path, index=False)
    return df
