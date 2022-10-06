
from flask import Flask, jsonify,request, after_this_request
from ml_pipeline import predict_cat_breed
from PIL import Image

app = Flask(__name__)


@app.route('/')
def test():
    return jsonify({'it':'works'})

@app.route('/predict', methods=['POST'])
def predict():

    # get image data
    image_data = request.files['file']
    image = Image.open(image_data).convert("RGB")

    # model does its thing
    out = predict_cat_breed(image)

    # send json back
    return jsonify(out)

if __name__ == '__main__':
    app.run(port=3500,host='0.0.0.0')