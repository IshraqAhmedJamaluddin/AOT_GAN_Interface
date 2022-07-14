# Dependencies
from fileinput import filename
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import subprocess
import io
from base64 import encodebytes
from PIL import Image

# Your API definition
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route('/predict' , methods=['POST'])
@cross_origin()
def predict():
    try:
        org = request.files['img']
        mask = request.files['mask']
        path1 = '../src/dataset/trial/clear'
        for file_name in os.listdir(path1):
            os.remove(os.path.join(path1, file_name))
        path2 = '../src/dataset/trial/masks'
        for file_name in os.listdir(path2):
            print(file_name)
            os.remove(os.path.join(path2, file_name))
        org.save(os.path.join(path1, '1.png'))
        mask.save(os.path.join(path2, '1.png'))

        path3 = '../src'
        path4 = '../src/outputs'
        p = subprocess.run(["python", os.path.join(path3, 'test.py'), '--model', 'aotgan_yomna', '--pre_train', '../src/experiments/aotgan_clear_pconv512/G0051500.pt', '--dir_image', '../src/dataset/trial/clear/', '--dir_mask', '../src/dataset/trial/masks/', '--outputs', '../src/outputs'])
        
        result = [os.path.join(path4, '1_masked.png'), os.path.join(path4, 'predicted', '1.png')]
        encoded_imges = []
        for image_path in result:
            encoded_imges.append(get_response_image(image_path))
        return jsonify({'status': 'success', 'result': encoded_imges})
    except Exception  as e:
        print(e)
        return jsonify({'status': 'error'})
