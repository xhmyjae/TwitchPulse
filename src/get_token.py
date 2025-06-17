import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

def generate_app_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Nouveau token généré : {token}")
        return token
    else:
        raise Exception(f"❗ Erreur génération token : {response.status_code} - {response.text}")

# Exemple d'utilisation
if __name__ == "__main__":
    token = generate_app_access_token()
