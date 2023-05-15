import os
import math
import random
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from tkinter import filedialog, Tk

def extract_watermark(img):
    # Extract region of watermark
    width, height = img.size
    # Apply binarization to see the dominating pixels
    thresh = 120
    fn = lambda x: 255 if x > thresh else 0
    im1 = img.crop((0, height - 50, 100, height)).convert('L').point(fn, '1')
    pixels = list(im1.getdata())
    most_common = max(pixels, key=pixels.count)
    return most_common, width, height

def apply_watermark(img_path, output_folder, text, font_size=20):
    img1, img_name = img_path
    name = os.path.splitext(img_name)[0]
    # Opening Image, adding an alpha channel & Creating New Text Layer
    img = Image.open(img1).convert('RGBA')
    value, width, height = extract_watermark(img)
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)
    font = ImageFont.truetype("micross.ttf", font_size)
    textwidth, textheight = d.textsize(text, font)
    x = 0
    y = height - 50
    # Applying Text depending on the dominant pixel value
    v = abs(value - 255)
    d.text((x, y), text, fill=(v, v, v, 125), font=font)
    # Combining Original Image with Text and Saving
    watermarked = Image.alpha_composite(img, txt)
    watermarked.save(os.path.join(output_folder, f'{name}_watermark.png'))

def watermark_images(folder, output_folder, text, font_size):
    img_paths = [(os.path.join(folder, file), file) for file in os.listdir(folder) if file.endswith((".png", ".jpg"))]
    t1 = perf_counter()
    with ProcessPoolExecutor() as executor:
        executor.map(lambda img_path: apply_watermark(img_path, output_folder, text, font_size), img_paths)
    t2 = perf_counter()
    print(f'Done in {t2 - t1} seconds')
    print(f'Processed {len(img_paths)} images')

def select_directory(title='Please select a directory'):
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(parent=root, initialdir="/", title=title)
    return folder