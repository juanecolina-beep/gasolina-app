import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import os
import time

# --- Configuración ---
URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
MARCA = "REPSOL"
MUNICIPIO = "SESEÑA"
TIPO = "Precio Gasolina 95 E5"
DB = "gasolina.db"

DOCS = "docs"
JS_DIR = os.path.join(DOCS, "js")
os.makedirs(JS_DIR, exist_ok=True)

CSV_PATH = os.path.join(DOCS, "precios_gasolina.csv")
GRAFICO_PATH = os.path.join(DOCS, "historial_gasolina.png")

# --- Consultar API ---
def obtener_api(max_intentos=5, delay=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    for intento in range(max_intentos):
        try:
            print(f"Intento {intento+1} de API")
            r = requests.get(URL, headers=headers, timeout=20)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Error intento {intento+1}: {e}")
            if intento < max_intentos-1:
                time.sleep(delay)
    print("No se pudo obtener datos de la API")
    return None

data = obtener_api()

# --- Leer últimos datos si falla la API ---
if not data:
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, sep=';')
        print("Usando CSV anterior")
    else:
        df = pd.DataFrame(columns=["fecha","estacion","direccion","precio"])
        df.to_csv(CSV_PATH, index=False, sep=';')
        print("CSV vacío generado")
else:
    lista = data.get("ListaEESSPrecio", [])
    precios = []
    hoy = datetime.now().strftime("%Y-%m-%d")
    for e in lista:
        if MARCA in e.get("Rótulo","").upper() and MUNICIPIO in e.get("Municipio","").upper():
            precio = e.get(TIPO)
            if precio and precio.strip():
                try:
                    precios.append({
                        "fecha": hoy,
                        "estacion": e.get("Rótulo"),
                        "direccion": e.get("Dirección"),
                        "precio": float(precio.replace(",",".")),
                    })
                except:
                    pass
    # --- Guardar en SQLite ---
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS precios_gasolina (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            estacion TEXT,
            direccion TEXT,
            precio REAL
        )
    """)
    conn.commit()
    for p in precios:
        cursor.execute("""
            SELECT 1 FROM precios_gasolina WHERE fecha=? AND estacion=? AND direccion=?
        """, (p["fecha"], p["estacion"], p["direccion"]))
        if cursor.fetchone(): 
            continue
        cursor.execute("""
            INSERT INTO precios_gasolina(fecha, estacion, direccion, precio)
            VALUES (?, ?, ?, ?)
        """, (p["fecha"], p["estacion"], p["direccion"], p["precio"]))
    conn.commit()
    df = pd.read_sql_query("SELECT * FROM precios_gasolina", conn)
    conn.close()

# --- Guardar CSV ---
df.to_csv(CSV_PATH, index=False, sep=';')
print(f"CSV guardado en {CSV_PATH}")

# --- Gráfico histórico ---
if len(df) > 0:
    plt.figure(figsize=(8,5))
    for dir in df["direccion"].unique():
        sub = df[df["direccion"]==dir]
        plt.plot(sub["fecha"], sub["precio"], marker="o", label=dir)
    plt.title("Gasolina 95 Repsol - Seseña")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (€)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAFICO_PATH)
    print(f"Gráfico guardado en {GRAFICO_PATH}")

# --- Gasolinera más barata ---
if len(df)>0:
    min_row = df.loc[df['precio'].idxmin()]
    barata_texto = f"💰 {min_row['estacion']} - {min_row['direccion']}: {min_row['precio']} € ¡Mejor precio!"
else:
    barata_texto = "No hay precios válidos"

# --- JS ---
js_code = f'document.getElementById("barata").textContent = "{barata_texto}";'
with open(os.path.join(JS_DIR,"script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)
print("JS actualizado correctamente")