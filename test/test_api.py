# test via pytest 

import pytest
import sys
import os
import pandas as pd
import json



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


# Fonction de test pour prédiction du modèle
def test_prediction_model():
    client = app.test_client()
    
    # récupération 1 ligne client (au format du modèle entrainé) à partir d'un fichier test CSV
    test_client = pd.read_csv('premiere_ligne.csv')
            
    test_client.rename(columns=lambda x: x.replace('-', '_'), inplace=True)
    test_client.rename(columns=lambda x: x.replace(',', '_'), inplace=True)
        
    # Convertir les données en JSON
    # data_json = test_client.to_json(orient='records')
    
    data_json = json.dumps(test_client.to_dict(orient='records'))
    
    # Test de la route '/getScoring' en effectuant une requête POST avec notre donnée test: data_json
    response = client.post('/getScoring', json={'data': data_json})

    # 1er test sur la réponse ( OK -> code 200)
    assert response.status_code == 200

    result_data = json.loads(response.data.decode('utf-8'))
        
    # Vérification existance de la clef 'predictions'
    assert 'predictions' in result_data
        
    # Récuperation de la prédiction pour notre client test
    predictions = result_data['predictions']
    
    # Vérification du nombre de prédiction. Dans notre cas -> 1 (qui est notre client test)
    assert len(predictions) == len(test_client)
    
    # Vérification de la prédiction 0 ou 1
    assert predictions[0] == 0 or predictions[0] == 1
            
    print("Test N°3: Prédiction du modèle et route: /getScoring  OK !")

    
# ..................

# Fonction erreur qui lève une exception erreur => empechera le deploiement de l'API sur Heroku
#def test_erreur():
#    assert 3==4

# .....................    
    
if __name__ == '__main__':
    pytest.main()

    
    




