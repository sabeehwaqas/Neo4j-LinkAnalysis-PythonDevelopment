from flask import Flask, request, jsonify
from io import BytesIO
from PIL import Image

filetypes=('.jpg', '.jpeg', '.png', '.gif')

def image_upload(File,name):
    if 'image' not in File:
        return jsonify({'error': 'No file part'}), 400
    ext=False
    file = File['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    image_data = file.read()

    for a in filetypes:
        if file.filename.lower().endswith(a):
            ext=a
    if ext==False:
        return jsonify({'error': 'Invalid file type'}), 400        
    
    image = Image.open(BytesIO(image_data))
    # image.save(f'images/{name}{ext}')
    image.save(f'images/TESTING_NEW_VER.png')

    return jsonify({'message':'Image uploaded and processed successfully'}), 200


