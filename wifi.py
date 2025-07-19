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
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_state():
    try:
        with open("/home/siranj/pidrip/state.json") as f:
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


def did_it_rain():
    url = f"https://api.tomorrow.io/v4/weather/history/recent?location=12.9018743,80.1653073&timesteps=1d&apikey={WEATHER_API_KEY}"

    headers = {
        "accept": "application/json",
        "accept-encoding": "deflate, gzip, br"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        data = response.json()

        # Extract daily data
        daily_data = data.get('timelines', {}).get('daily', [])
        rain_sums = []

        for day in daily_data:
            try:
                rain_sum = day['values'].get('rainAccumulationSum')
                if rain_sum is not None:
                    rain_sums.append(rain_sum)
            except (KeyError, TypeError):
                continue  # skip malformed entries

        if rain_sums:
            average_rain = sum(rain_sums) / len(rain_sums)
            if average_rain > 7:
                send_message(
                    f"Average rain 🌧️ fall : {average_rain:.2f}mm. Skipping irrigation")
                return True
            else:
                send_message(
                    f"Average rain 🌧️ fall : {average_rain:.2f}mm. Watering.")
                return False
        else:
            send_message("No valid rainAccumulationSum data found.  Watering.")
            return True

    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
    except ValueError:
        print("Failed to parse JSON response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    delay = 1800
    try:
        if get_state() and get_state() == 'off':
            send_message("Current state is OFF, exiting.")
            exit(0)
        if did_it_rain():
            exit(0)
        open_valve()
        time.sleep(delay)
        close_valve()
    except KeyboardInterrupt:
        close_valve()
