# test via pytest 

import pytest
import sys
import os

# Ajouter chemin du répertoire parent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer le module apiScore2 depuis le répertoire parent
from apiScore2 import app

# Test pour la route racine '/'
def test_root():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "API lancée correctement"

# ..................


if __name__ == '__main__':
    pytest.main()
