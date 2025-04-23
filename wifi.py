import requests
import time

url = "http://192.168.1.50"

headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}


def open_valve():
    payload = 'auth=321&state=ON'

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def close_valve():
    payload = 'auth=321&state=OFF'

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)



if __name__ == '__main__':
    delay = 5
    try:
        open_valve()
        time.sleep(delay)
        close_valve()
    except KeyboardInterrupt:
        close_valve()