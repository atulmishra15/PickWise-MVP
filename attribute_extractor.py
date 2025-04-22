import pandas as pd
import re

def extract_attributes(text: str) -> dict:
    attributes = {
        "color": None,
        "length": None,
        "style": None,
        "material": None,
        "occasion": None,
        "pattern": None,
        "neckline": None,
        "sleeve_type": None,
        "category": None,
    }

    text = text.lower()

    # Color
    color_keywords = ['black', 'white', 'red', 'blue', 'green', 'yellow', 'pink', 'grey', 'brown', 'beige', 'purple', 'orange', 'gold', 'silver']
    attributes["color"] = next((word for word in color_keywords if word in text), None)

    # Length
    if "maxi" in text or "long" in text:
        attributes["length"] = "long"
    elif "mini" in text or "short" in text:
        attributes["length"] = "short"
    elif "midi" in text or "knee" in text:
        attributes["length"] = "midi"

    # Style
    if "bodycon" in text:
        attributes["style"] = "bodycon"
    elif "a-line" in text or "flared" in text:
        attributes["style"] = "a-line"
    elif "shift" in text:
        attributes["style"] = "shift"
    elif "shirt" in text:
        attributes["style"] = "shirt"

    # Material
    material_keywords = ['cotton', 'denim', 'linen', 'polyester', 'satin', 'lace', 'chiffon', 'velvet', 'leather']
    attributes["material"] = next((word for word in material_keywords if word in text), None)

    # Occasion
    if "party" in text or "evening" in text:
        attributes["occasion"] = "party"
    elif "casual" in text:
        attributes["occasion"] = "casual"
    elif "formal" in text or "office" in text:
        attributes["occasion"] = "formal"

    # Pattern
    if "floral" in text:
        attributes["pattern"] = "floral"
    elif "striped" in text or "stripes" in text:
        attributes["pattern"] = "striped"
    elif "checked" in text or "checkered" in text:
        attributes["pattern"] = "checked"
    elif "graphic" in text or "printed" in text:
        attributes["pattern"] = "graphic"

    # Neckline
    if "v-neck" in text or "v neck" in text:
        attributes["neckline"] = "v-neck"
    elif "round neck" in text or "crew neck" in text:
        attributes["neckline"] = "round neck"
    elif "halter" in text:
        attributes["neckline"] = "halter"

    # Sleeve type
    if "sleeveless" in text:
        attributes["sleeve_type"] = "sleeveless"
    elif "long sleeve" in text or "full sleeve" in text:
        attributes["sleeve_type"] = "long sleeve"
    elif "short sleeve" in text or "half sleeve" in text:
        attributes["sleeve_type"] = "short sleeve"

    # Category (basic logic)
    if "dress" in text:
        attributes["category"] = "dress"
    elif "handbag" in text or "bag" in text:
        attributes["category"] = "handbag"
    elif "t-shirt" in text or "tee" in text:
        attributes["category"] = "t-shirt"
    elif "shirt" in text:
        attributes["category"] = "shirt"

    return attributes

def enrich_attributes(df: pd.DataFrame) -> pd.DataFrame:
    enriched_data = []

    for _, row in df.iterrows():
        name = row.get("name", "")
        price = row.get("price", "")
        brand = row.get("brand", "")
        base_attrs = extract_attributes(name)
        enriched_row = {
            "name": name,
            "price": price,
            "brand": brand,
            **base_attrs
        }
        enriched_data.append(enriched_row)

    return pd.DataFrame(enriched_data)
