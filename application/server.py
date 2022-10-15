
from flask import Flask, jsonify,request, render_template
from ml_pipeline import predict_cat_breed
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():

    # get image data
    image_data = request.files['file']
    #image = Image.open(image_data).convert("RGB")
    image = Image.open(image_data)

    #predict cat breed
    out = predict_cat_breed(image)

    # send json back
    return jsonify(out)

if __name__ == '__main__':
    app.run(debug=True, port=3500,host='0.0.0.0')