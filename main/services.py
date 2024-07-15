# main/services.py
import requests
import base64

def upload_image(api_key, image_file):
    url = 'https://api.imgbb.com/1/upload'
    payload = {
        'key': api_key,
        'image': base64.b64encode(image_file)
    }
    response = requests.post(url, data=payload)
    return response.json()
