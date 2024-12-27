from flask import Flask, render_template, request, redirect, url_for
import pyotp
from PIL import Image
from pyzbar.pyzbar import decode
import re
import os
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # secret key for session

# check temp exist or not
if not os.path.exists('temp'):
    os.makedirs('temp')

# generate t-otp
def generate_new_otp():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    return totp.now(), secret

def extract_secret_key(data):
    match = re.search(r'secret=([^&]+)', data)
    if match:
        return match.group(1)
    return None

def generate_otp_from_qr(image_path):
    try:
        image = Image.open(image_path)
        decoded_objects = decode(image)

        if decoded_objects:
            extracted_data = decoded_objects[0].data.decode('utf-8').strip()

            secret_key = extract_secret_key(extracted_data)

            if secret_key:
                totp = pyotp.TOTP(secret_key)
                otp = totp.now()
                return otp
            else:
                return "Secret key not found or invalid."
        else:
            return "Secret key not found or invalid."
    except Exception as e:
        return f"err: {str(e)}"

@app.route('/')
def index():
    otp_list = []

    qr_images_dir = "temp"
    if not os.path.exists(qr_images_dir):
        return "please make sure /temp already."

    qr_images = os.listdir(qr_images_dir)
    for qr_image in qr_images:
        image_path = os.path.join(qr_images_dir, qr_image)
        otp = generate_otp_from_qr(image_path)
        otp_list.append({'qr_name': qr_image, 'otp': otp})

    return render_template('index.html', otp_list=otp_list)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['qr_image']
        if file:
            file.save(os.path.join('temp', file.filename))
            time.sleep(1)
            return redirect(url_for('index'))

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)