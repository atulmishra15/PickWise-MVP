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
