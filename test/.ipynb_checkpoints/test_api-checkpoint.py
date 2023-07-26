# test via pytest 

import pytest
import sys
import os


# Ajouter chemin du répertoire parent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer le module apiScore2 depuis le répertoire parent
from apiScore2 import app, model as model_charge


# Definition des fonctions de test pour execution pytest

# Test pour la route racine '/'
def test_root():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "API lancée correctement"
    print("Test N°1: Test de la route Racine de l'API OK ! ")
    
    
# Test chargement du modèle   
def test_chargement_model():
    # Vérifier que le modèle est chargé correctement
    assert model_charge is not None
    print("Test N°2: Le modèle est chargé correctement !")


    
    
import pytest
import json
import pandas as pd
from apiScore2 import app

# Fonction de test pour prédiction du modèle
def test_prediction_model():
    client = app.test_client()
    
    # récupération 1 ligne client (au format du modèle entrainé) à partir d'un fichier test CSV
    test_client = pd.read_csv('premiere_ligne.csv')

    # Convertir les données en JSON
    data_json = test_client.to_json(orient='records')

    # Test de la route '/getScoring' en effectuant une requête POST avec notre donnée test: data_json
    response = client.post('/getScoring', json=data_json)

    # 1er test sur la réponse ( OK -> code 200)
    assert response.status_code == 200

    # récupération réponse JSON
    reponse_data = json.loads(response.data.decode('utf-8'))

    # Vérifier que la prédiction a été effectuée correctement
    assert 'predictions' in reponse_data
    predictions = reponse_data['predictions']

    # Ajoutez ici les assertions pour vérifier les prédictions du modèle
    # par exemple :
    assert len(predictions) == len(test_data)
    # Ajoutez vos autres assertions ici en fonction des résultats attendus

    print("Test N°3: Prédiction du modèle OK !")


    
    
# ..................

# Fonction erreur qui lève une exception erreur => empechera le deploiement de l'API sur Heroku
#def test_erreur():
#    assert 3==4

# .....................    
    
if __name__ == '__main__':
    pytest.main()

    
    




