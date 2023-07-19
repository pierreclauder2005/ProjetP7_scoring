# Importer les bibliothèques nécessaires
import subprocess
import threading

# Définir la fonction pour exécuter l'API Flask en tâche de fond
def run_flask():
    subprocess.call(["gunicorn", "apiScore:app"])

# Exécuter l'API Flask en tâche de fond dans un thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Exécuter votre page principale Streamlit
subprocess.call(["streamlit", "run", "applicationScore_v6.py"])
