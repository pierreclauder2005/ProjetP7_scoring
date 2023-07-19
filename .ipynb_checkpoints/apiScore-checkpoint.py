from flask import Flask, request
import random
import json
import joblib
import pandas as pd
import os

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000)) # ajout pour Heroku

model = joblib.load("modelScoring_v2.pkl")

if model is not None:
    print("Le modèle a été chargé avec succès.")
else:
    print("Erreur lors du chargement du modèle.")

@app.route('/_stcore/allowed-message-origins')
def allowed_message_origins():
    return ''

@app.route('/_stcore/health')
def health():
    return ''

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

@app.route("/streamlit")
def streamlit():
    # Command to run streamlit app
    os.system("streamlit run page.py")
    return "<h1>Streamlit app is running!</h1>"

if __name__ == '__main__':
    app.run(port=port, threaded=True)  # threaded=True to allow multiple requests at once
