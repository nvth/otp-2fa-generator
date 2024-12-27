import base64
from PIL import Image
from io import BytesIO
import argparse
import os

parser = argparse.ArgumentParser(description='Decode base64 image data from a text file')
parser.add_argument('filename', type=str, help='Name of the text file containing base64 image data')

args = parser.parse_args()

with open(args.filename, 'r') as file:
    base64_image = file.read()


#validate extension image
comma_index = base64_image.find(',')
if comma_index != -1:
    base64_image = base64_image[comma_index+1:]
#decode
image_data = base64.b64decode(base64_image)
#generate image qr
image = Image.open(BytesIO(image_data))

filename_no_extension = os.path.splitext(args.filename)[0]

image.save(f"{filename_no_extension}"".png")