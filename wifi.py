import requests
import time
import json
from dotenv import load_dotenv
import os
url = "http://192.168.1.50"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

load_dotenv()  # Load .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def get_state():
    try:
        with open("state.json") as f:
            return json.load(f).get("state")
    except FileNotFoundError:
        return None


def send_message(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP responses (4xx, 5xx)
        # print(response.status_code)
        # print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Telegram message failed: {e}")


def open_valve():
    payload = 'auth=321&state=ON'

    response = requests.request("POST", url, headers=headers, data=payload)
    print('watering')
    print(response.text)
    send_message("Watering plants 🌱🌿🌾")


def close_valve():
    payload = 'auth=321&state=OFF'

    response = requests.request("POST", url, headers=headers, data=payload)
    print('done')

    print(response.text)
    send_message("Watering complete 🌳🌲🌴")


if __name__ == '__main__':
    delay = 1800
    try:
        if get_state() and get_state() == 'off':
            send_message("Current state is OFF, exiting.")
            exit(0)
        open_valve()
        time.sleep(delay)
        close_valve()
    except KeyboardInterrupt:
        close_valve()
