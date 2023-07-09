# Application Streamlit permettant d'appeler notre API
# Cette application s'occupe également d'afficher les résultat

import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from builtins import abs
from sklearn.metrics import roc_curve, auc, RocCurveDisplay

# Lecture du fichier résultat de l'étape précédente EDA  (100 premières lignes afin d'économiser la RAM)
df = pd.read_csv('./credit_conso_vf.csv', nrows=100)

# Séparation des features et Target
X = df.drop('TARGET', axis=1)
y = df['TARGET']

# Nettoyage des noms de colonnes contenant des espaces et ":"
X.columns = X.columns.str.replace(r'[\s:]', '_', regex=True)
# 2ème Nettoyage 
X.columns = X.columns.str.replace('/', '_')
# 3ème Nettoyage
X.columns = X.columns.str.replace('[-,]', '_')

# X=X.head(1)   # un seul client -> le 1er du dataframe pour le test

# Convertir le DataFrame en format JSON
# input_data_json = X.to_json(orient='records')


st.header("Affichage Client - Modèle de Scoring ")

st.sidebar.header("Paramètres d'entrée")


# Liste des clients pour  la selection

clients= X["SK_ID_CURR"].tolist()
selected_client= st.sidebar.selectbox("Selectionnez un numéro client", clients)

st.write("Client N° = ",selected_client)
st.write("\n")

selected_client_df= X[X["SK_ID_CURR"]==selected_client]

# Déscription du client
sex= selected_client_df["CODE_GENDER"]
possede_car= selected_client_df["FLAG_OWN_CAR"]
proprietaire= selected_client_df["FLAG_OWN_REALTY"]
nb_enfant= selected_client_df["CNT_CHILDREN"]
revenu= selected_client_df["AMT_INCOME_TOTAL"]

input_client_json = selected_client_df.to_json(orient='records')

# Bouton pour envoyer la requête à l'API
if st.sidebar.button("Prédire"):
    response = requests.post("http://localhost:5000/getScoring", json={'data': input_client_json})
    print(response)
    print(response.text)
    if response.status_code == 200 or response.status_code == 201:
        response_json = response.json()
        predictions_json = response_json['predictions']
        # st.write(predictions_json)
        if predictions_json[0]==0:
            client="Bon Client"
        else:
            client="Mauvais Client"
        st.write(predictions_json[0],": ",client)
        
        st.write("Sex: ",sex.values[0])
        st.write("Voiture (O/N): ",possede_car.values[0])
        st.write("Proprietaire: ",proprietaire.values[0])
        st.write("Nombre enfant(s):",nb_enfant.values[0])
        st.write("Revenu: ",revenu.values[0])
       
    else:
        st.write("Erreur lors de la requête à l'API")
    

    
    
    
        

        
        
        