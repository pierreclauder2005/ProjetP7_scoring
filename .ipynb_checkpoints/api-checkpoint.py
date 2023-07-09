from flask import Flask, jsonify, request
import joblib

app= Flask(__name__)

model= joblib.load("modelScoring.pkl")

@app.route('/')
def home():
    return "API Flask en cours d'exécution..."


@app.route('/predict', methods=['POST'])
def predict():
    data=request.json['data']
    predictions= model.predict(data)
    return jsonify({'predictions': predictions.tolist()})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)

    
    
    
    