import streamlit as st
import requests

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from builtins import abs
from sklearn.metrics import roc_curve, auc, RocCurveDisplay

# Lecture du fichier résultat de l'étape précédente EDA

df = pd.read_csv('./credit_conso.csv')

# Séparation des features et Target

X = df.drop('TARGET', axis=1)
y = df['TARGET']

# Nettoyage des noms de colonnes contenant des espaces et ":"
X.columns = X.columns.str.replace(r'[\s:]', '_', regex=True)
# 2ème Nettoyage 
X.columns = X.columns.str.replace('/', '_')
# 3ème Nettoyage
X.columns = X.columns.str.replace('[-,]', '_')


# Champ de saisie pour les données d'entrée
input_data = st.text_input("Entrez les données d'entrée")

input_data= X.head(10)

# Bouton pour envoyer la requête à l'API
if st.button("Prédire"):
    # Envoyer la requête à votre API Flask
    response = requests.post('http://localhost:5000/predict', json={'data': input_data})
   
    # Vérifier la réponse de l'API
    if response.status_code == 200:
        # Récupérer les résultats de prédiction
        predictions = response.json()['predictions']
       
        # Afficher les résultats de prédiction
        st.write("Résultats de prédiction :", predictions)
    else:
        st.write("Erreur lors de la requête à l'API")