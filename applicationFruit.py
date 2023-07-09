import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from builtins import abs
from sklearn.metrics import roc_curve, auc, RocCurveDisplay

# Lecture du fichier résultat de l'étape précédente EDA
df = pd.read_csv('./credit_conso.csv', nrows=1000)

df= df.head(10)

# Séparation des features et Target
X = df.drop('TARGET', axis=1)
y = df['TARGET']

# Nettoyage des noms de colonnes contenant des espaces et ":"
X.columns = X.columns.str.replace(r'[\s:]', '_', regex=True)
# 2ème Nettoyage 
X.columns = X.columns.str.replace('/', '_')
# 3ème Nettoyage
X.columns = X.columns.str.replace('[-,]', '_')

X=X.head(1)   # un seul client -> le 1er du dataframe


# Convertir le DataFrame en format JSON
input_data_json = X.to_json(orient='records')

# Bouton pour envoyer la requête à l'API
if st.button("Prédire"):
    response = requests.post("http://localhost:5000/getFruit", json={'data': input_data_json})
    print(response)
    print(response.text)
    if response.status_code == 200 or response.status_code == 201:
            
            response_json = response.json()
            # st.write(response_json["fruit"])
            
            predictions_json = response_json['predictions']
            st.write(predictions_json)
    else:
        st.write("Erreur lors de la requête à l'API")
    

    
    
    
        

        
        
        