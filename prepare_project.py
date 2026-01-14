import os
import urllib.request
import subprocess
import sys

def download_file(url, filename):
    if os.path.exists(filename):
        print(f"--- {filename} já existe. Pulando download.")
        return
    print(f"--- Baixando {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"--- {filename} baixado com sucesso.")
    except Exception as e:
        print(f"--- Erro ao baixar {filename}: {e}")

def main():
    print("=== Preparação do Projeto Vision AI ===")
    
    # 1. Instalar dependências
    print("\n[1/3] Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except Exception as e:
        print(f"Erro ao instalar dependências: {e}")

    # 2. Baixar Modelos
    print("\n[2/3] Baixando arquivos do YOLOv3 (isso pode demorar ~240MB)...")
    models = {
        "yolov3.weights": "https://pjreddie.com/media/files/yolov3.weights",
        "yolov3.cfg": "https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg?raw=true"
    }
    
    for filename, url in models.items():
        download_file(url, filename)

    # 3. Criar diretórios necessários
    print("\n[3/3] Verificando pastas...")
    os.makedirs("static/uploads", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    print("\n=== TUDO PRONTO! ===")
    print("\nAgora você pode testar rodando:")
    print("python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()
