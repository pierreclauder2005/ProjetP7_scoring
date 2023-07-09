# API en Flask permettant d'utiliser notre modèle de Classification

from flask import Flask, request
import random
import json
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("modelScoring_v2.pkl")

if model is not None:
    print("Le modèle a été chargé avec succès.")
else:
    print("Erreur lors du chargement du modèle.")


@app.route('/getScoring', methods=['POST'])
def getScoring():
    
    print("dans fonction predict !!!!! ")
    data_json = request.get_json()['data']
    print(' Hello !!!! ')
    print(data_json)
    
    data = json.loads(data_json)
    # Créer un DataFrame à partir des données
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    return json.dumps({'predictions': predictions.tolist()})
 
    
if __name__ == '__main__':
    app.run(debug=True)
