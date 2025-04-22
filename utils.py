import tempfile
import os
import shutil
import uuid
from datetime import datetime
from PIL import Image


def load_uploaded_images(file_list):
    """
    Saves uploaded Streamlit files to temp storage and returns metadata list.
    """
    image_data = []
    os.makedirs("temp_images", exist_ok=True)

    for file in file_list:
        ext = os.path.splitext(file.name)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join("temp_images", unique_name)

        with open(temp_path, "wb") as f:
            f.write(file.read())

        image_data.append({
            "image_path": temp_path,
            "image_name": file.name,
            "upload_time": datetime.now().isoformat()
        })

    return image_data


def clear_temp_images():
    """
    Deletes all temp images from temp_images folder.
    """
    temp_dir = "temp_images"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)


def format_score(score):
    """
    Round and format a buyability score.
    """
    return f"{score:.2f}"


def save_dataframe_csv(df, filename_prefix="output"):
    """
    Save a DataFrame to output folder with timestamped filename.
    """
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join("output", f"{filename_prefix}_{timestamp}.csv")
    df.to_csv(path, index=False)
    return path


def resize_image(input_path, output_path=None, size=(300, 300)):
    """
    Resize an image to a given size. Saves resized copy if output_path is provided.
    """
    try:
        img = Image.open(input_path)
        img = img.resize(size)
        if output_path:
            img.save(output_path)
        return img
    except Exception as e:
        print(f"Failed to resize {input_path}: {e}")
        return None


def is_image_file(filename):
    """
    Checks if a file is an image based on extension.
    """
    ext = filename.lower().split('.')[-1]
    return ext in ['jpg', 'jpeg', 'png', 'webp', 'bmp', 'tiff']


def display_image_metadata(image_info):
    """
    Format image info dict into a readable summary.
    """
    name = image_info.get("image_name", "unknown")
    path = image_info.get("image_path", "")
    time = image_info.get("upload_time", "")
    return f"🖼️ {name} | 📍 {path} | ⏱️ {time}"


def create_output_subfolder(folder_name):
    """
    Creates a named subfolder in /output and returns its path.
    """
    output_dir = os.path.join("output", folder_name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
