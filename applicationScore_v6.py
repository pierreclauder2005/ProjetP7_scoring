# Application Streamlit permettant d'appeler notre API
# Cette application s'occupe également d'afficher les résultat

import streamlit as st
import requests
import joblib
import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
import numpy as np
from builtins import abs
# from sklearn.metrics import roc_curve, auc, RocCurveDisplay
import shap
# import time
import os


# Lecture du fichier résultat de l'étape précédente EDA  (100 premières lignes afin d'économiser la RAM)
# df = pd.read_csv('./credit_conso_vf.csv', nrows=1000)

df = pd.read_csv('./credit_conso_vf2.csv', nrows=1000)

# Séparation des features et Target
X = df.drop('TARGET', axis=1)
y = df['TARGET']

# Nettoyage des noms de colonnes contenant des espaces et ":"
X.columns = X.columns.str.replace(r'[\s:]', '_', regex=True)
# 2ème Nettoyage 
X.columns = X.columns.str.replace('/', '_')
# 3ème Nettoyage
X.columns = X.columns.str.replace('[-,]', '_')

# création Tranches d'âge via les quantiles
X['age_tranche'] = pd.qcut(X['age'], q=4, labels=['Tranche1', 'Tranche2', 'Tranche3', 'Tranche4'])
tranche_age_Min_Max= X.groupby('age_tranche')['age'].agg(['min', 'max'])
conditions = [
    X['age_tranche'] == 'Tranche1',
    X['age_tranche'] == 'Tranche2',
    X['age_tranche'] == 'Tranche3',
    X['age_tranche'] == 'Tranche4'
]

# même chose pour .... camembert comparaison

df['age_tranche'] = pd.qcut(df['age'], q=4, labels=['Tranche1', 'Tranche2', 'Tranche3', 'Tranche4'])
tranche_age_Min_Max_cam= df.groupby('age_tranche')['age'].agg(['min', 'max'])
conditions_cam = [
    df['age_tranche'] == 'Tranche1',
    df['age_tranche'] == 'Tranche2',
    df['age_tranche'] == 'Tranche3',
    df['age_tranche'] == 'Tranche4'
]


choices_cam = [str(int(tranche_age_Min_Max_cam.loc['Tranche1', 'min'])) +'-'+ str(int(tranche_age_Min_Max_cam.loc['Tranche1', 'max']))
, str(int(tranche_age_Min_Max_cam.loc['Tranche2', 'min'])) +'-'+ str(int(tranche_age_Min_Max_cam.loc['Tranche2', 'max']))
, str(int(tranche_age_Min_Max_cam.loc['Tranche3', 'min'])) +'-'+ str(int(tranche_age_Min_Max_cam.loc['Tranche3', 'max']))
, str(int(tranche_age_Min_Max_cam.loc['Tranche4', 'min'])) +'-'+ str(int(tranche_age_Min_Max_cam.loc['Tranche4', 'max']))
]


choices = [str(int(tranche_age_Min_Max.loc['Tranche1', 'min'])) +'-'+ str(int(tranche_age_Min_Max.loc['Tranche1', 'max']))
, str(int(tranche_age_Min_Max.loc['Tranche2', 'min'])) +'-'+ str(int(tranche_age_Min_Max.loc['Tranche2', 'max']))
, str(int(tranche_age_Min_Max.loc['Tranche3', 'min'])) +'-'+ str(int(tranche_age_Min_Max.loc['Tranche3', 'max']))
, str(int(tranche_age_Min_Max.loc['Tranche4', 'min'])) +'-'+ str(int(tranche_age_Min_Max.loc['Tranche4', 'max']))
]

X['tranche-age-MinMax'] = np.select(conditions, choices, default='')

df['tranche-age-MinMax'] = np.select(conditions_cam, choices_cam, default='')

# Fin quantile .....................

# Début quantile salaire
X['tranche_salaire'] = pd.qcut(X['AMT_INCOME_TOTAL'], q=4, labels=['TrancheSalaire1', 'TrancheSalaire2', 'TrancheSalaire3', 'TrancheSalaire4'])

df['tranche_salaire'] = pd.qcut(df['AMT_INCOME_TOTAL'], q=4, labels=['TrancheSalaire1', 'TrancheSalaire2', 'TrancheSalaire3', 'TrancheSalaire4'])

tranche_salaire_Min_Max= X.groupby('tranche_salaire')['AMT_INCOME_TOTAL'].agg(['min', 'max'])

tranche_salaire_Min_Max_cam= df.groupby('tranche_salaire')['AMT_INCOME_TOTAL'].agg(['min', 'max'])

conditions = [
    X['tranche_salaire'] == 'TrancheSalaire1',
    X['tranche_salaire'] == 'TrancheSalaire2',
    X['tranche_salaire'] == 'TrancheSalaire3',
    X['tranche_salaire'] == 'TrancheSalaire4'
]


conditions_cam = [
    df['tranche_salaire'] == 'TrancheSalaire1',
    df['tranche_salaire'] == 'TrancheSalaire2',
    df['tranche_salaire'] == 'TrancheSalaire3',
    df['tranche_salaire'] == 'TrancheSalaire4'
]


choices_salaire = [str(int(tranche_salaire_Min_Max.loc['TrancheSalaire1', 'min'])) +'-'+ str(int(tranche_salaire_Min_Max.loc['TrancheSalaire1', 'max']))
, str(int(tranche_salaire_Min_Max.loc['TrancheSalaire2', 'min'])) +'-'+ str(int(tranche_salaire_Min_Max.loc['TrancheSalaire2', 'max']))
, str(int(tranche_salaire_Min_Max.loc['TrancheSalaire3', 'min'])) +'-'+ str(int(tranche_salaire_Min_Max.loc['TrancheSalaire3', 'max']))
, str(int(tranche_salaire_Min_Max.loc['TrancheSalaire4', 'min'])) +'-'+ str(int(tranche_salaire_Min_Max.loc['TrancheSalaire4', 'max']))
]


choices_salaire_cam = [str(int(tranche_salaire_Min_Max_cam.loc['TrancheSalaire1', 'min'])) +'-'+ str(int(tranche_salaire_Min_Max_cam.loc['TrancheSalaire1', 'max']))
, str(int(tranche_salaire_Min_Max_cam.loc['TrancheSalaire2', 'min'])) +'-'+ str(int(tranche_salaire_Min_Max_cam.loc['TrancheSalaire2', 'max']))
, str(int(tranche_salaire_Min_Max_cam.loc['TrancheSalaire3', 'min'])) +'-'+ str(int(tranche_salaire_Min_Max_cam.loc['TrancheSalaire3', 'max']))
, str(int(tranche_salaire_Min_Max_cam.loc['TrancheSalaire4', 'min'])) +'-'+ str(int(tranche_salaire_Min_Max_cam.loc['TrancheSalaire4', 'max']))
]

X['tranche-salaire-MinMax'] = np.select(conditions, choices_salaire, default='')

df['tranche-salaire-MinMax'] = np.select(conditions_cam, choices_salaire_cam, default='')

# Fin quantile salaire

st.markdown("<h1 style='text-align: center;'>Client - Modèle de Scoring</h1>", unsafe_allow_html=True)
st.sidebar.header("Paramètres d'entrée")

# Filtre interactif pour la variable "Sexe"
sex_filter = st.sidebar.selectbox("Filtrer par Sexe", ["Tous", "Homme", "Femme"])

choices.insert(0, 'Tous')
age_filter = st.sidebar.selectbox("Filtrer par Tranche Age", choices)

choices_salaire.insert(0, 'Tous')
salaire_filter = st.sidebar.selectbox("Filtrer par Salaire", choices_salaire)

proprietaire_filter = st.sidebar.selectbox("Filtrer par Propriétaire", ["Tous", "Oui", "Non"])

# test_filter = st.sidebar.checkbox("Filtrer par Test")

# Filtrer les données en fonction du filtre sélectionné

if sex_filter != "Tous":
    sex_value = 1 if sex_filter == "Homme" else 0
    X = X[X["CODE_GENDER"] == sex_value]

if age_filter != "Tous":
    X = X[X["tranche-age-MinMax"] == age_filter]
        
if salaire_filter != "Tous":
    X = X[X["tranche-salaire-MinMax"] == salaire_filter] 
    
if proprietaire_filter != "Tous":
    proprietaire_value = 1 if proprietaire_filter == "Oui" else 0
    X = X[X["FLAG_OWN_REALTY"] == proprietaire_value]

# st.sidebar.write("Nbre clients filtrés : ",X.shape[0],"/1000")

st.sidebar.markdown("<div style='display: flex; justify-content: center;'>Nbre clients filtrés : " + str(X.shape[0]) + "/1000</div><br><br>", unsafe_allow_html=True)

# Liste des clients pour  la selection

clients= X["SK_ID_CURR"].tolist()
selected_client= st.sidebar.selectbox("Selectionnez un numéro client", clients)


selected_client_df= X[X["SK_ID_CURR"]==selected_client]
selected_client_df.drop('age_tranche', axis=1, inplace=True)
selected_client_df.drop('tranche-age-MinMax', axis=1, inplace=True)
selected_client_df.drop('tranche_salaire', axis=1, inplace=True)
selected_client_df.drop('tranche-salaire-MinMax', axis=1, inplace=True)


# Description du client
sex= selected_client_df["CODE_GENDER"]
possede_car= selected_client_df["FLAG_OWN_CAR"]
proprietaire= selected_client_df["FLAG_OWN_REALTY"]
nb_enfant= selected_client_df["CNT_CHILDREN"]
revenu= selected_client_df["AMT_INCOME_TOTAL"]
age= selected_client_df["age"]


# Affichage caractéristiques du Client selectionné
st.markdown(f"<div style='background-color: lightgray; padding: 10px;'><b>Client N° =</b> <span style='font-size: 1.2em;'>{selected_client}</span> </div>", unsafe_allow_html=True)
st.write(f"Sex: <span style='color:rgb(50, 205, 50)'>{ 'M' if sex.values[0] == 1 else 'F' }</span>", unsafe_allow_html=True)

st.write("Age: ",int(age.values[0]))   
st.write(f"Voiture: <span style='color:rgb(50, 205, 50)'>{ 'Oui' if possede_car.values[0] == 1 else 'Non' }</span>", unsafe_allow_html=True)
st.write(f"Proprietaire: <span style='color:rgb(50, 205, 50)'>{ 'Oui' if proprietaire.values[0] == 1 else 'Non' }</span>", unsafe_allow_html=True)
st.write("Nombre enfant(s):",nb_enfant.values[0])
st.write("Revenu: ",revenu.values[0])


input_client_json = selected_client_df.to_json(orient='records')


def afficher_jauge(coef, pred_0):
    if pred_0 >= 0.5 and pred_0 < 0.7 :
        couleur = 'orange'
    elif pred_0 > 0.4 and pred_0 < 0.5:
        couleur = 'orange'
    elif pred_0 >= 0.7:
        couleur = 'green'
    else:
        couleur = 'red'

    # Affichage de la jauge avec l'animation CSS et la valeur
    st.write("Coefficient de probabilité")
    st.markdown(f"""
        <div style="background-color: lightgray; border-radius: 4px; padding: 4px;">
            <div 
                style="
                    background-color: {couleur};
                    width: {coef*100}%;
                    height: 20px;
                    border-radius: 4px;
                    animation: augmenter-jauge 2s ease-out;
                    animation-fill-mode: forwards;
                    position: relative;
                "
            >
                <div
                    style="
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        color: white;
                    "
                >
                    {coef}
                </div>
            </div>
        </div>
        <style>
            @keyframes augmenter-jauge {{
                from {{ width: 0%; }}
                to {{ width: {coef*100}% ; }}
            }}
        </style>
    """, unsafe_allow_html=True)



# Bouton pour envoyer la requête à l'API
if st.sidebar.button("Prédire"): 
    st.write("<!doctype html> <html lang=en> <title>500 Internal Server Error</title> <h1>Internal Server Error</h1> <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>Erreur lors de la requête à l'API")
     
 

st.sidebar.write(
    "<style>.stButton>button { display: block; margin: 0 auto; }</style>",
    unsafe_allow_html=True
)
  




    
    
        

        
        
        