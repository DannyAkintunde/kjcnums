from imgurpython import ImgurClient
from imgbb import ImgBB
import tempfile
import os

def upload_image_to_imgur(image_file):
    try:
        # Authenticate with Imgur API (anonymous authentication)
        #client_id = 'b942f9a4196beca'
        #client_secret = '8d89418f1578ab91d659ae83daf6d95c0eeecbb6'
        #client = ImgurClient(client_id, client_secret)

        imgbb = ImgBB('38d76241532304dbc771bd929c512a0e')
        # Create a temporary file to save the uploaded image
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        for chunk in image_file.chunks():
            temp_file.write(chunk)
        temp_file.close()
        # Upload image to Imgur
        #image = client.upload_from_path(temp_file.name)
        image = imgbb.uplode(temp_file.name)

        os.remove(temp_file.name)



        # Return the URL of the uploaded image
        return image
    except Exception as e:
    # Handle any exceptions, such as network errors or authentication failures
        print("An error occurred:", str(e))
        return None
