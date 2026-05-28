import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not api_key:
    print("ERROR: No se encontró OPENAI_API_KEY en el archivo .env")
else:
    print("OK: API key cargada correctamente")

print(f"Modelo configurado: {model}")
