from flask import Flask, jsonify, request
import joblib
import pandas as pd


app = Flask(__name__)

model = joblib.load("modelScoring.pkl")

if model is not None:
    print("Le modèle a été chargé avec succès.")
else:
    print("Erreur lors du chargement du modèle.")


@app.route('/getPredict', methods=['POST'])
def getPredict():
    data_json = request.get_json()['data']
    data = pd.DataFrame.from_records(data_json, columns=model.feature_names_)
    predictions = model.predict(data)
    return json.dumps({'predictions': predictions.tolist()})
    # return jsonify({'predictions': predictions.tolist()})


if __name__ == '__main__':
    app.run(debug=True)

    
      

        
    
    

    

