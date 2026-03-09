import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
import os
import time

# --- Configuración ---
URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
MARCA = "REPSOL"
MUNICIPIO = "SESEÑA"
TIPO = "Precio Gasolina 95 E5"

DOCS = "docs"
JS_DIR = os.path.join(DOCS, "js")
os.makedirs(JS_DIR, exist_ok=True)

CSV_PATH = os.path.join(DOCS, "precios_gasolina.csv")

# --- Función para consultar API con reintentos ---
def obtener_api(max_intentos=5, delay=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    for i in range(max_intentos):
        try:
            print(f"Intento {i+1} de consulta a la API...")
            r = requests.get(URL, headers=headers, timeout=20)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Error API: {e}")
            time.sleep(delay)
    return None

# --- Obtener datos ---
data = obtener_api()

precios = []

if data:
    for e in data.get("ListaEESSPrecio", []):
        if MARCA in e.get("Rótulo", "").upper() and MUNICIPIO in e.get("Municipio", "").upper():
            precio = e.get(TIPO)
            if precio and precio.strip():
                try:
                    precios.append({
                        "fecha": datetime.now().strftime("%Y-%m-%d"),
                        "estacion": e.get("Rótulo"),
                        "direccion": e.get("Dirección"),
                        "precio": float(precio.replace(",", "."))
                    })
                except:
                    pass

# --- Guardar CSV ---
if precios:
    df = pd.DataFrame(precios)
else:
    df = pd.DataFrame([{"fecha": "Error", "estacion": "No hay datos", "direccion": "No hay datos", "precio": 0}])

df.to_csv(CSV_PATH, index=False, sep=';')
print(f"CSV guardado en {CSV_PATH}")

# --- Generar gráfico histórico ---
if not df.empty and df['precio'].max() > 0:
    plt.figure(figsize=(8,5))
    for d in df["direccion"].unique():
        sub = df[df["direccion"] == d]
        plt.plot(sub["fecha"], sub["precio"], marker="o", label=d)
    plt.title("Gasolina 95 Repsol - Seseña")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (€)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(DOCS, "historial_gasolina.png"))
    plt.close()
    print("Gráfico generado")

# --- Gasolinera más barata ---
if not df.empty and df['precio'].max() > 0:
    min_row = df.loc[df['precio'].idxmin()]
    barata_texto = f"💰 {min_row['estacion']} - {min_row['direccion']}: {min_row['precio']} € ¡Mejor precio!"
else:
    barata_texto = "No hay precios válidos"

# --- Generar JS directo ---
js_code = f'document.getElementById("barata").textContent = "{barata_texto}";'
with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)
print("JS actualizado en docs/js/script.js")