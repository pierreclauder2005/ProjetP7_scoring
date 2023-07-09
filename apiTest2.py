import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration du journal
logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.info('Accès à la page d\'accueil')
    return "API Flask en cours d'exécution..."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Vérifier si les paramètres d'entrée requis sont présents
    if 'param1' not in data or 'param2' not in data:
        app.logger.error('Paramètres manquants')
        return jsonify({'error': 'Paramètres manquants'}), 400

    # Récupérer les paramètres d'entrée
    param1 = data['param1']
    param2 = data['param2']

    # Effectuer la prédiction (exemple)
    prediction = param1 + param2

    # Retourner la prédiction au format JSON
    app.logger.info(f'Prédiction : {prediction}')
    return jsonify({'prediction': prediction}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    