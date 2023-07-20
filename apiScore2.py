from flask import Flask, request
import random
import json
import joblib
import pandas as pd
import os

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))  # ajout pour Heroku


@app.route('/')
def root():
    return "API lancée correctement"


@app.route('/_stcore/allowed-message-origins')
def allowed_message_origins():
    return ''

@app.route('/_stcore/health')
def health():
    return ''

@app.route('/getScoring', methods=['POST'])
def getScoring():
    model = joblib.load("modelScoring_v2.pkl")  # déplacer le chargement du modèle ici
    
    if model is not None:
        print("Le modèle a été chargé avec succès.")
    else:
        print("Erreur lors du chargement du modèle.")
        return json.dumps({'error': 'Erreur lors du chargement du modèle.'})
    
    print("dans fonction predict !!!!! ")
    #data_json = request.get_json()['data']
    #print("get_json")
    print(' Hello !!!! ')
    #print(data_json)
    
    #data = json.loads(data_json)
    # print("data")
    #df = pd.DataFrame(data)
    
    #predictions = model.predict(df)
    # print("predictions")
    # return json.dumps({'predictions': predictions.tolist()})
    return json.dumps({'message': 'API fonctionne correctement'})
     
if __name__ == '__main__':
    app.run(port=port)
    #app.run(debug=True)
