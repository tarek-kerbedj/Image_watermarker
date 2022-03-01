#Importing Libraries
import math
from time import perf_counter
import os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from tkinter import ttk,LabelFrame,Entry
from os import makedirs
from os.path import isdir,join
import tkinter
from tkinter import filedialog
## in case you wanna use the simplistic GUI
root = tkinter.Tk()
folder = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
output_folder=filedialog.askdirectory(parent=root,initialdir="/",title='Please select output directory')
# insert a word here
text = ""
## in case you wanna use the command line only
#folder=input('Choose an input directory... \n')
#output_folder=input('Choose an output directory ... \n')
#if not isdir(output):
        #if the folder doesnt exist , create one
 #           makedirs(output)

# setting a custom threshold value to make the images black and white
thresh = 120
fn = lambda x : 255 if x > thresh else 0
# select a custom font , with font size
font = ImageFont.truetype("micross.ttf", 20)
# extracting images paths , and folder names at the same time
img_paths=[(os.path.join(folder,file),file) for file in os.listdir(folder) if file.endswith(".png") or file.endswith(".jpg")]
def extract(img):
    # extract region of watermark 
    width, height = img.size 
    # apply binarization to see the dominating pixels
    im1 = img.crop((0, height-50,100 , height)).convert('L').point(fn,'1')
    pixels = list(im1.getdata())
    most_common = max(pixels, key = pixels.count)
    return most_common,width,height

def apply_watermark(img_path):
        img1,img_name = img_path
        name = img_name.split('.')[0]
        # Opening Image , adding an alpha channel & Creating New Text Layer
        img = Image.open(img1).convert('RGBA')
        value,width,height=extract(img)
        txt = Image.new('RGBA', img.size, (255,255,255,0))        
        d = ImageDraw.Draw(txt)
        #width, height = img.size 
        textwidth, textheight = d.textsize(text, font)
        x = 0
        y = height-50  
        # Applying Text depending on the dominant pixel value
        v = abs(value-255)
        d.text((x,y), text, fill=(v,v,v,125), font=font)
  #Combining Original Image with Text and Saving
        watermarked = Image.alpha_composite(img, txt)
        #watermarked.save(str(random.random())+'watermark'+".png")
        watermarked.save(output_folder+'/'+name+'_watermark'+".png")

t1=perf_counter()
with ThreadPoolExecutor() as executor:
    executor.map(apply_watermark,img_paths)
t2=perf_counter()
print(f'done in {t2-t1} seconds')
print(f'processed {len(img_paths)} images')
