import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import time

import os


script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
mac = '0000032C9B953E1F'
apip = "192.168.1.162" 
image_width = 296

Palet = [
    (0, 0, 0, 255),
    (255, 255, 255, 255),
    (255, 0, 0, 255)
]

from datetime import datetime, date

# Target date
target_date = date(2025, 8, 8)
olddays = None

# Define your ticket update function
def update_days(days):
    print(f"Days until: {days}")
    canvas_width, canvas_height = 296, 152
    canvas = Image.new('RGB', (canvas_width, canvas_height), color=Palet[1])
    draw = ImageDraw.Draw(canvas)

    font = ImageFont.truetype(os.path.join(script_dir,"Beon-Regular.ttf"), size=40)  # Use a TrueType font
    titlefont = ImageFont.truetype(os.path.join(script_dir,"Beon-Regular.ttf"), size=100)  # Use a TrueType font
    draw.text((4,100),f"days until WHY", fill=Palet[0], font=font)
    text = f"{days}"
    bbox = draw.textbbox((0, 0), text, font=titlefont)
    text_width = bbox[2] - bbox[0]
    x = (image_width - text_width) // 2

    draw.text((x, 2), text, font=titlefont, fill=Palet[0])

    canvas.save(os.path.join(script_dir,'whydays.jpg'), 'JPEG', quality=100)
    print('image generated')
    uploadimage()

def uploadimage():
 # Save the image as JPEG with maximum quality
    image_path = os.path.join(script_dir,'whydays.jpg')
    dither = 0
    # Prepare the HTTP POST request
    url = "http://" + apip + "/imgupload"
    payload = {"dither": dither, "mac": mac}  # Additional POST parameter
    files = {"file": open(image_path, "rb")}  # File to be uploaded

    # Send the HTTP POST request
    try:
        response = requests.post(url, data=payload, files=files)

        # Check the response status
        if response.status_code == 200:
            print(f"{mac} Image uploaded successfully! {image_path}")
        else:
            print(f"{mac} Failed to upload the image.")
    except:
        print(f"{mac} Failed to upload the image.")
    print('succesfully uploaded')

while True:
    # Today's date
    today = date.today()
    days_remaining = (target_date - today).days
    if olddays != days_remaining:
        update_days(days_remaining)
        print(f"Days until 8 August 2025: {days_remaining}")  
        olddays = days_remaining 
    time.sleep(60)

 
