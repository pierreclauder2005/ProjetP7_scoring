from flask import Flask, request, jsonify
import joblib
import pandas as pd
import random
import json




app = Flask(__name__)

model = joblib.load("modelScoring.pkl")
noms_variables = pd.read_csv('./noms_variables.csv')

if model is not None:
    print("Le modèle a été chargé avec succès.")
else:
    print("Erreur lors du chargement du modèle.")

@app.route('/getFruit', methods=['POST'])
def getFruit():
    data_json = request.get_json()['data']
    
    data_dict = json.loads(data_json[0])
    
    print(data_dict)

    """
    data = pd.DataFrame.from_dict(data_dict, orient='index', columns=noms_variables.columns)
    predictions = model.predict(data)
    
    """
    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
