import requests
import time

url = "192.168.1.50"

# payload = 'bkm=321&off=OFF'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)

def open_valve():
    # url = "192.168.1.50"
    payload = 'auth=321&state=ON'
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def close_valve():
    # url = "192.168.1.50"
    payload = 'auth=321&state=OFF'
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

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