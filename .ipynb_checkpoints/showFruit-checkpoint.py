import streamlit as st
import requests

def get_fruit_from_api():
    response = requests.post("http://localhost:5000/getFruit")
    if response.status_code == 200:
        result = response.json()
        return result["fruit"]
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
