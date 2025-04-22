import re
import os
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Basic fashion lexicons
COLORS = ['red', 'blue', 'black', 'white', 'green', 'yellow', 'pink', 'purple', 'orange', 'brown', 'beige', 'grey', 'gold', 'silver']
OCCASIONS = ['casual', 'party', 'work', 'formal', 'evening', 'wedding', 'beach', 'holiday', 'daily']
DESIGNS = ['floral', 'solid', 'striped', 'checked', 'graphic', 'embroidered', 'printed', 'polka dot', 'lace', 'denim', 'frill', 'ruffle']
MATERIALS = ['cotton', 'polyester', 'linen', 'denim', 'silk', 'satin', 'wool', 'nylon', 'leather', 'chiffon', 'knit']
STYLES = ['bodycon', 'maxi', 'midi', 'mini', 'a-line', 'shift', 'wrap', 'shirt', 'fit & flare', 'kaftan', 'tunic']

# Helper to extract terms from text
def find_in_text(text, terms):
    found = []
    for term in terms:
        if re.search(r'\b' + re.escape(term) + r'\b', text, flags=re.IGNORECASE):
            found.append(term.lower())
    return found

def extract_attributes_from_text(title, description):
    combined = f"{title} {description}".lower()
    attributes = {
        "color": find_in_text(combined, COLORS),
        "occasion": find_in_text(combined, OCCASIONS),
        "design": find_in_text(combined, DESIGNS),
        "material": find_in_text(combined, MATERIALS),
        "style": find_in_text(combined, STYLES),
    }
    return attributes

# Optional: Extract visible text from image (OCR)
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

# Optional: Image-based color detection
def detect_dominant_color(image_path):
    try:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (50, 50))
        pixels = img.reshape((-1, 3))
        pixels = np.float32(pixels)
        n_colors = 3
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
        return f"rgb({int(dominant[0])},{int(dominant[1])},{int(dominant[2])})"
    except Exception as e:
        print(f"Color detection error: {e}")
        return "unknown"

# Entry point: products from scrapes or uploads
def extract_attributes(products):
    enriched_products = []
    for product in products:
        title = product.get("title", "")
        description = product.get("description", "")
        image_path = product.get("image_path", None)

        attrs = extract_attributes_from_text(title, description)

        if image_path and os.path.exists(image_path):
            # Optional image-based augmentation
            image_text = extract_text_from_image(image_path)
            image_attrs = extract_attributes_from_text(image_text, "")
            for k in attrs:
                attrs[k] = list(set(attrs[k] + image_attrs.get(k, [])))
            attrs["dominant_color_rgb"] = detect_dominant_color(image_path)

        product["attributes"] = attrs
        enriched_products.append(product)

    return enriched_products
# Add your real attribute extraction logic from uploaded product images
