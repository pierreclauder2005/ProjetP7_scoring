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


X=X.head(1)   # un seul client -> le 1er du dataframe

# st.dataframe(X)

# st.write(X.shape)

# Convertir le DataFrame en format JSON
input_data_json = X.to_json(orient='records')

def get_fruit_from_api():
        response = requests.post('http://localhost:5000/getPredict', json={'data': input_data_json})
        if response.status_code == 200:
            # Convertir la réponse JSON en DataFrame
            response_json = response.json()
            predictions_json = response_json['predictions']
            predictions = pd.DataFrame.from_dict(predictions_json)
            return prediction
        else:
            return None
        

def main():
    st.title("Fruit API")

    # Appel à l'API pour obtenir le fruit
    fruit = get_fruit_from_api()

    if fruit:
        st.success(f"Le fruit choisi est : {fruit}")
    else:
        st.error("Une erreur s'est produite lors de l'appel à l'API.")

if __name__ == '__main__':
    main()

        
        