from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
from model_files.ml_predict import predict_plant, Network

app = Flask("Plant Disease Detector")
CORS(app)

@app.route('/', methods=['POST'])
def predict():
    try:
        key_dict = request.get_json()
        image = key_dict["image"]
        imgdata = base64.b64decode(image)
        model = Network()
        result, remedy = predict_plant(model, imgdata)
        plant = result.split("___")[0]
        disease = " ".join((result.split("___")[1]).split("_"))
        response = {
            "plant": plant,
            "disease": disease,
            "remedy": remedy,
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

