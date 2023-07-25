# test via pytest 

import pytest
import sys
import os
import apiScore2

# Ajouter chemin du répertoire parent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer le module apiScore2 depuis le répertoire parent
from apiScore2 import app


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
    assert apiScore2.model is not None
    print("Test N°2: Le modèle est chargé correctement !")


# ..................

# Fonction erreur qui lève une exception erreur => empechera le deploiement de l'API sur Heroku
#def test_erreur():
#    assert 3==4

# .....................    
    
if __name__ == '__main__':
    pytest.main()

    
    




