import pyotp
from PIL import Image
from pyzbar.pyzbar import decode
import re

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
                return "Not found secret_key on QR code."
        else:
            return "Not found secret_key on QR code."
    except Exception as e:
        return f"err: {str(e)}"

# Thay đổi đường dẫn đến hình ảnh QR code của bạn
qr_image_path = "cypentest.png"
otp = generate_otp_from_qr(qr_image_path)
print(f"Cypentest {otp}")