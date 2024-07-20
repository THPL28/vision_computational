
# Vision Computational

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.63.0-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5.2-orange)

## Descrição

O projeto Vision Computational é uma aplicação de visão computacional construída com FastAPI. Ele permite o upload de imagens e a detecção de objetos utilizando um modelo de rede neural treinado com YOLOv3. O objetivo é fornecer uma interface simples para realizar tarefas de detecção de objetos em imagens.



## Funcionalidades
Upload de Imagens: Permite o upload de imagens para o servidor.
Detecção de Objetos: Utiliza YOLOv3 para detectar objetos nas imagens enviadas.

## Pré-requisitos
Python 3.8 ou superior
Pip (Python package installer)

## Instalação
Clone o repositório:

git clone https://github.com/THPL28/vision_computational.git
cd vision_computational

## Crie um ambiente virtual:

python -m venv venv
Ative o ambiente virtual:

No Windows:

.\venv\Scripts\activate

No Linux/Mac:

source venv/bin/activate

Instale as dependências:

pip install -r requirements.txt

## Baixe os arquivos de configuração e pesos do YOLOv3:

yolov3.cfg
yolov3.weights
Coloque esses arquivos na raiz do projeto.

## Executando a Aplicação
Inicie o servidor FastAPI:

uvicorn app.main:app --reload
Acesse a documentação interativa no navegador:

Swagger UI: http://127.0.0.1:8000/docs
Redoc: http://127.0.0.1:8000/redoc

## Testando a API
Via cURL
Envie uma imagem para o endpoint /detect-objects/:

curl -X POST "http://127.0.0.1:8000/detect-objects/" -F "file=@path_to_your_image.jpg"
Via Python (requests)

## Estrutura do Projeto

```plaintext
Vision_Computational/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── vision.py
│   └── services/
│       ├── __init__.py
│       └── vision_service.py
├── models/
│   ├── __init__.py
│   └── vision_model.py
├── tests/
│   ├── __init__.py
│   └── test_vision.py
├── requirements.txt
└── README.md
