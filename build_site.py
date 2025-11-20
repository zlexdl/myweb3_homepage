import os
import json
import shutil
from pathlib import Path
from PIL import Image

# Configuration
BASE_DIR = Path(os.getcwd())
SOURCE_CN = BASE_DIR / "extracted_cn"
SOURCE_EN = BASE_DIR / "extracted_en"
PORTAL_DIR = BASE_DIR / "portal"
ASSETS_DIR = PORTAL_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
DATA_FILE = PORTAL_DIR / "data.json"

# Ensure directories exist
print(f"Checking source directory: {SOURCE_CN}")
if not SOURCE_CN.exists():
    print(f"Error: Source directory {SOURCE_CN} does not exist!")
    exit(1)

if os.path.exists(ASSETS_DIR):
    try:
        shutil.rmtree(ASSETS_DIR)
    except Exception as e:
        print(f"Warning: Could not clean assets dir: {e}")
        
os.makedirs(IMAGES_DIR, exist_ok=True)

def optimize_image(src_path, dest_filename, max_width=1600):
    """
    Convert image to web-friendly format (JPG/PNG), resize if too large.
    Returns the relative path for the web or None if failed.
    """
    try:
        with Image.open(src_path) as img:
            # Convert TIFF or others to RGB for JPG
            if img.mode in ('RGBA', 'P') and 'transparency' in img.info:
                # Keep PNG for transparency
                save_format = 'PNG'
                ext = '.png'
            elif img.mode != 'RGB':
                img = img.convert('RGB')
                save_format = 'JPEG'
                ext = '.jpg'
            else:
                save_format = 'JPEG'
                ext = '.jpg'

            # Resize if too big
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            final_filename = dest_filename + ext
            dest_path = IMAGES_DIR / final_filename
            
            if save_format == 'JPEG':
                img.save(dest_path, save_format, quality=80, optimize=True)
            else:
                img.save(dest_path, save_format, optimize=True)
                
            return f"assets/images/{final_filename}"
    except Exception as e:
        print(f"Error processing image {src_path}: {e}")
        return None

def read_text(path):
    if not path.exists():
        return ""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return ""

def main():
    slides_data = []
    
    # Get all slide folders from CN (assuming CN covers all structure)
    # Sort by slide number
    slide_folders = sorted([d for d in SOURCE_CN.iterdir() if d.is_dir() and d.name.startswith('slide_')])
    
    for folder in slide_folders:
        slide_id = folder.name # e.g., slide_01
        print(f"Processing {slide_id}...")
        
        # 1. Read Texts
        cn_text_path = folder / "texts" / "cn.txt"
        en_text_path = SOURCE_EN / slide_id / "texts" / "en.txt" # Guessing filename
        
        # Fallback if en.txt name is different? User said "extracted_en" structure is similar.
        # Let's check if en text file exists with slightly different name if exact match fails
        if not en_text_path.exists():
             # Try to find any txt file in that dir
             en_text_dir = SOURCE_EN / slide_id / "texts"
             if en_text_dir.exists():
                 txts = list(en_text_dir.glob("*.txt"))
                 if txts:
                     en_text_path = txts[0]

        cn_content = read_text(cn_text_path)
        en_content = read_text(en_text_path)
        
        # 2. Process Images
        # We will check extracted_cn images primarily.
        # If specific images are better in EN, we could merge, but usually they are identical visuals.
        img_list = []
        src_img_dir = folder / "images"
        
        if src_img_dir.exists():
            # Sort images to maintain order
            src_images = sorted([f for f in src_img_dir.iterdir() if f.is_file() and not f.name.startswith('.')])
            
            for idx, img_file in enumerate(src_images):
                # Generate unique name: slide_01_0.jpg
                dest_name = f"{slide_id}_{idx}"
                web_path = optimize_image(img_file, dest_name)
                if web_path:
                    img_list.append(web_path)
        
        # Structure the data
        slide_entry = {
            "id": slide_id,
            "images": img_list,
            "content": {
                "cn": cn_content,
                "en": en_content
            }
        }
        
        slides_data.append(slide_entry)

    # Save JSON
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(slides_data, f, ensure_ascii=False, indent=2)
        
    print(f"Done! Processed {len(slides_data)} slides. Data saved to {DATA_FILE}")

if __name__ == "__main__":
    main()

