import requests

url = "http://127.0.0.1:8000/detect-objects/"
file_path = "carro.jpg"  # Substitua pelo caminho da sua imagem

with open(file_path, "rb") as image_file:
    files = {"file": image_file}
    response = requests.post(url, files=files)

print(response.json())
