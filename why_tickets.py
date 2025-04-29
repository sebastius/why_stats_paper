import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import time

import os

import paho.mqtt.client as mqtt

available_number = None
total_size = None
image_width = 296
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
mac = '00000FFFFFF'
apip = "192.168.1.162" 

Palet = [
    (0, 0, 0, 255),
    (255, 255, 255, 255),
    (255, 0, 0, 255)
]

def on_message(client, userdata, msg):
    global available_number, total_size

    topic = msg.topic
    payload = msg.payload.decode()

    try:
        value = int(payload)
    except ValueError:
        print(f"Invalid number received on topic {topic}: {payload}")
        return

    if topic == 'why2025/ticketshop/quotas/Event Visitors/available_number':
        available_number = value
        update_tickets(available_number)
    elif topic == 'why2025/ticketshop/quotas/Event Visitors/total_size':
        total_size = value

    # If both values are known, calculate and print used tickets
    if available_number is not None and total_size is not None:
        used = total_size - available_number
        print(f"Used tickets: {used}")

# Define your ticket update function
def update_tickets(available):
    print(f"Available tickets: {available}")
    canvas_width, canvas_height = 296, 152
    canvas = Image.new('RGB', (canvas_width, canvas_height), color=Palet[1])
    draw = ImageDraw.Draw(canvas)

    font = ImageFont.truetype(os.path.join(script_dir,"Beon-Regular.ttf"), size=35)  # Use a TrueType font
    titlefont = ImageFont.truetype(os.path.join(script_dir,"Beon-Regular.ttf"), size=100)  # Use a TrueType font
    draw.text((4,100),f"tickets remaining", fill=Palet[0], font=font)
    text = f"{available}"
    bbox = draw.textbbox((0, 0), text, font=titlefont)
    text_width = bbox[2] - bbox[0]
    x = (image_width - text_width) // 2

    draw.text((x, 2), text, font=titlefont, fill=Palet[0])

    canvas.save(os.path.join(script_dir,'whytickets.jpg'), 'JPEG', quality=100)
    print('image generated')
    uploadimage()

def uploadimage():
 # Save the image as JPEG with maximum quality
    image_path = os.path.join(script_dir,'whytickets.jpg')
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

client = mqtt.Client()

client.on_message = on_message

client.connect("mqtt.why2025.org", 1883, 60)
client.subscribe("why2025/ticketshop/quotas/Event Visitors/available_number")
client.subscribe("why2025/ticketshop/quotas/Event Visitors/total_size")

# Start the MQTT client loop
client.loop_forever()
