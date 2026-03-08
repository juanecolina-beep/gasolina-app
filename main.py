import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import os

URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
MARCA = "REPSOL"
MUNICIPIO = "SESEÑA"
TIPO = "Precio Gasolina 95 E5"
DB = "gasolina.db"

# Carpeta donde GitHub Pages sirve la web
DOCS = "docs"
os.makedirs(DOCS, exist_ok=True)

print("Consultando API del Ministerio...")

try:
    response = requests.get(URL, timeout=15)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("Error al consultar API:", e)
    exit(1)

lista = data.get("ListaEESSPrecio", [])

# Filtrar estaciones REPSOL en Seseña
precios = []
for e in lista:
    if MARCA in e.get("Rótulo", "").upper() and MUNICIPIO in e.get("Municipio", "").upper():
        precio = e.get(TIPO)
        if precio and precio.strip():
            try:
                precio_f = float(precio.replace(",", "."))
                precios.append({
                    "estacion": e.get("Rótulo"),
                    "direccion": e.get("Dirección"),
                    "precio": precio_f
                })
            except:
                pass

if not precios:
    print("No se encontraron estaciones Repsol en Seseña")
    exit(0)

print(f"Se encontraron {len(precios)} estaciones.")

# Base de datos
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

hoy_str = datetime.now().strftime("%Y-%m-%d")

# Guardar precios sin duplicar
for p in precios:
    cursor.execute("""
    SELECT * FROM precios_gasolina
    WHERE fecha=? AND estacion=? AND direccion=?
    """, (hoy_str, p["estacion"], p["direccion"]))
    
    if cursor.fetchone():
        print("Precio ya registrado hoy:", p["precio"])
    else:
        cursor.execute("""
        INSERT INTO precios_gasolina (fecha, estacion, direccion, precio)
        VALUES (?, ?, ?, ?)
        """, (hoy_str, p["estacion"], p["direccion"], p["precio"]))
        print("Guardado:", p["precio"])

conn.commit()

# DataFrame para análisis
df = pd.read_sql_query("SELECT * FROM precios_gasolina", conn)
conn.close()

if len(df) == 0:
    print("No hay datos para gráfico")
    exit(0)

# Gráfico histórico por dirección
plt.figure(figsize=(8,5))
for dir in df["direccion"].unique():
    sub = df[df["direccion"] == dir]
    plt.plot(sub["fecha"], sub["precio"], marker="o", label=dir)

plt.title(f"Gasolina 95 Repsol - Seseña")
plt.xlabel("Fecha")
plt.ylabel("Precio (€)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Guardar en la carpeta docs para que GitHub Pages lo sirva
ruta_grafico = os.path.join(DOCS, "historial_gasolina.png")
plt.savefig(ruta_grafico)
print(f"Gráfico guardado en {ruta_grafico}")

# Guardar CSV en docs también
ruta_csv = os.path.join(DOCS, "precios_gasolina.csv")
df.to_csv(ruta_csv, index=False)
print(f"CSV guardado en {ruta_csv}")