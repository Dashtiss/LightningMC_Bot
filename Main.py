import requests
import Bot

def Update():
    url = f'https://raw.githubusercontent.com/Dashtiss/Lightning-MC-Bot/master/main.py?token=GHSAT0AAAAAACIXF3ZXB6MRDA7MD4I57I3UZMSC5PA'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
         print(f"Failed to retrieve file. Status code: {response.status_code}")
         return None


if __name__ == "__main__":
    Update = Update()
    if Update() is None:
        raise "File is blank"



