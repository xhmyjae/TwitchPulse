import asyncio
import websockets
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OAUTH_TOKEN = os.getenv("TWITCH_OAUTH")
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
NICK = os.getenv("TWITCH_NICK")
CHANNEL_NAME = os.getenv("TWITCH_CHANNEL")
CHANNEL = "#" + CHANNEL_NAME

def parse_message(message):
    if "PRIVMSG" not in message:
        return None

    try:
        parts = message.split("PRIVMSG")[1].strip()
        username = message.split("!")[0][1:]
        content = parts.split(":", 1)[1].strip()

        return {
            "username": username,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
    except:
        return None

def is_stream_live(channel_name):
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {OAUTH_TOKEN.replace('oauth:', '')}"
    }
    params = {"user_login": channel_name.lower()}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❗ Erreur API Twitch : {response.status_code} - {response.text}")
        return False

    data = response.json()
    return len(data["data"]) > 0

async def listen():
    uri = "wss://irc-ws.chat.twitch.tv:443"
    async with websockets.connect(uri) as websocket:
        await websocket.send(f"PASS {OAUTH_TOKEN}")
        await websocket.send(f"NICK {NICK}")
        await websocket.send(f"JOIN {CHANNEL}")

        print(f"✅ Connecté au chat de {CHANNEL}")

        json_file = "./data/chat_messages.json"
        if not os.path.exists(json_file):
            with open(json_file, "w") as f:
                json.dump([], f)

        while True:
            try:
                message = await websocket.recv()
                parsed_message = parse_message(message)

                if parsed_message:
                    with open(json_file, "r") as f:
                        messages = json.load(f)

                    messages.append(parsed_message)

                    with open(json_file, "w") as f:
                        json.dump(messages, f, indent=2)

                    print(f"{parsed_message['username']}: {parsed_message['content']}")

            except Exception as e:
                print(f"Erreur : {e}")
                break

async def main():
    print(f"🔎 Vérification si {CHANNEL_NAME} est en live...")

    if is_stream_live(CHANNEL_NAME):
        print(f"🎥 {CHANNEL_NAME} est EN LIVE ! Connexion au chat...")
        await listen()
    else:
        print(f"❌ {CHANNEL_NAME} n’est pas en live. Fin du programme.")

if __name__ == "__main__":
    asyncio.run(main())