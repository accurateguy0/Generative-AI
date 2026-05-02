from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # model = joblib.load('model.pkl') # Uncomment when you have a real model
    # prediction = model.predict([data['features']])
    return jsonify({"status": "success", "message": "Model received data!", "input": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
