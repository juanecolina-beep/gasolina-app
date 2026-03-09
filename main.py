import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime, date
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

# Crear carpetas necesarias
os.makedirs(DOCS, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

CSV_PATH = os.path.join(DOCS, "precios_gasolina.csv")

# --- Función para consultar API con reintentos ---
def obtener_api(max_intentos=5, delay=10):
    HEADERS = {"User-Agent": "Mozilla/5.0"}
    for intento in range(max_intentos):
        try:
            print(f"Consultando API del Ministerio... intento {intento+1}")
            response = requests.get(URL, headers=HEADERS, timeout=20)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al consultar API (intento {intento+1}/{max_intentos}): {e}")
            if intento < max_intentos - 1:
                time.sleep(delay)
    print("No se pudo obtener datos de la API después de varios intentos")
    return None

# --- Obtener datos ---
data = obtener_api()

# --- Usar último CSV si falla la API ---
if not data:
    if os.path.exists(CSV_PATH):
        print("API caída, usando CSV anterior")
        df = pd.read_csv(CSV_PATH, sep=';')
    else:
        with open(CSV_PATH, "w", encoding="utf-8") as f:
            f.write("fecha;estacion;direccion;precio\n")
            f.write("Error;No hay datos;No hay datos;0\n")
        print(f"CSV vacío generado en {CSV_PATH}")
        exit(0)
else:
    lista = data.get("ListaEESSPrecio", [])
    precios = []
    for e in lista:
        if MARCA in e.get("Rótulo", "").upper() and MUNICIPIO in e.get("Municipio", "").upper():
            precio = e.get(TIPO)
            if precio and precio.strip():
                try:
                    precio_f = float(precio.replace(",", "."))
                    precios.append({
                        "fecha": date.today().isoformat(),
                        "estacion": e.get("Rótulo"),
                        "direccion": e.get("Dirección"),
                        "precio": precio_f
                    })
                except:
                    pass
    if not precios:
        print("No se encontraron estaciones Repsol en Seseña")
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH, sep=';')
        else:
            with open(CSV_PATH, "w", encoding="utf-8") as f:
                f.write("fecha;estacion;direccion;precio\n")
                f.write("Error;No hay datos;No hay datos;0\n")
            exit(0)
    else:
        # Guardar en SQLite
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
            SELECT 1 FROM precios_gasolina
            WHERE fecha=? AND estacion=? AND direccion=?
            """, (p["fecha"], p["estacion"], p["direccion"]))
            if cursor.fetchone():
                continue
            cursor.execute("""
            INSERT INTO precios_gasolina (fecha, estacion, direccion, precio)
            VALUES (?, ?, ?, ?)
            """, (p["fecha"], p["estacion"], p["direccion"], p["precio"]))
        conn.commit()
        df = pd.read_sql_query("SELECT * FROM precios_gasolina", conn)
        conn.close()

# --- Asegurar que la columna fecha sea datetime ---
df['fecha'] = pd.to_datetime(df['fecha'], format="%Y-%m-%d", errors='coerce')

# --- Guardar CSV actualizado ---
df.to_csv(CSV_PATH, index=False, sep=';')
print(f"CSV guardado en {CSV_PATH}")

# --- Gráfico histórico ---
if len(df) > 0:
    plt.figure(figsize=(8,5))
    for dir in df["direccion"].unique():
        sub = df[df["direccion"] == dir]
        plt.plot(sub["fecha"], sub["precio"], marker="o", label=dir)
    plt.title("Gasolina 95 Repsol - Seseña")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (€)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    grafico_path = os.path.join(DOCS, "historial_gasolina.png")
    plt.savefig(grafico_path)
    print(f"Gráfico guardado en {grafico_path}")

# --- Gasolinera más barata HOY ---
df_hoy = df[df['fecha'].dt.date == date.today()]
if len(df_hoy) > 0:
    min_row = df_hoy.loc[df_hoy['precio'].idxmin()]
    barata_texto = f"💰 {min_row['estacion']} - {min_row['direccion']}: {min_row['precio']} € ¡Mejor precio!"
else:
    barata_texto = "No hay precios válidos hoy"

# --- Generar JS para la web ---
js_code = f'document.getElementById("barata").textContent = "{barata_texto}";'
js_path = os.path.join(JS_DIR, "script.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_code)
print(f"JS actualizado en {js_path}")