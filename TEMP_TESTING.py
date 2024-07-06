from flask import Flask, request, jsonify
from io import BytesIO
from PIL import Image
import os


def upload_image(request,name='NEW_TEST'):
    request=request.files
    image_data = request['image']
    
    ext='.png'
    
    image = Image.open(BytesIO(image_data))
    image.save(f'images/TESTING_NEW_VER.png')
    
    return 'Image uploaded and processed successfully'


