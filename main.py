import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import os
import time

# Configuración
URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
MARCA = "REPSOL"
MUNICIPIO = "SESEÑA"
TIPO = "Precio Gasolina 95 E5"
DB = "gasolina.db"

DOCS = "docs"
JS_DIR = os.path.join(DOCS, "js")
os.makedirs(DOCS, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

fecha_hoy = datetime.now().strftime("%Y-%m-%d")
CSV_PATH = os.path.join(DOCS, f"precios_gasolina_{fecha_hoy}.csv")  # CSV diario

# Función para consultar API
def obtener_api(max_intentos=5, delay=10):
    HEADERS = {"User-Agent": "Mozilla/5.0"}
    for intento in range(max_intentos):
        try:
            print(f"Consultando API del Ministerio... intento {intento+1}")
            response = requests.get(URL, headers=HEADERS, timeout=20)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error (intento {intento+1}/{max_intentos}): {e}")
            if intento < max_intentos - 1:
                time.sleep(delay)
    print("No se pudo obtener datos de la API después de varios intentos")
    return None

# Obtener datos
data = obtener_api()

precios = []
if data:
    lista = data.get("ListaEESSPrecio", [])
    for e in lista:
        if MARCA in e.get("Rótulo", "").upper() and MUNICIPIO in e.get("Municipio", "").upper():
            precio = e.get(TIPO)
            if precio and precio.strip():
                try:
                    precios.append({
                        "fecha": fecha_hoy,
                        "estacion": e.get("Rótulo"),
                        "direccion": e.get("Dirección"),
                        "precio": float(precio.replace(",", "."))
                    })
                except:
                    pass

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
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO precios_gasolina (fecha, estacion, direccion, precio)
        VALUES (?, ?, ?, ?)
        """, (p["fecha"], p["estacion"], p["direccion"], p["precio"]))
conn.commit()

df = pd.read_sql_query("SELECT * FROM precios_gasolina", conn)
conn.close()

# Guardar CSV diario
df_hoy = df[df['fecha'] == fecha_hoy]
if len(df_hoy) == 0:
    df_hoy = pd.DataFrame([{"fecha": fecha_hoy, "estacion":"No hay datos", "direccion":"No hay datos", "precio":0}])
df_hoy.to_csv(CSV_PATH, index=False, sep=';')
print(f"CSV diario guardado en {CSV_PATH}")

# Generar gráfico histórico
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
plt.savefig(os.path.join(DOCS, "historial_gasolina.png"))
print("Gráfico guardado")

# Gasolinera más barata hoy
min_row = df_hoy.loc[df_hoy['precio'].idxmin()]
barata_texto = f"💰 {min_row['estacion']} - {min_row['direccion']}: {min_row['precio']} € ¡Mejor precio!"

# Generar JS que apunte al CSV del día
js_code = f"""
document.getElementById("barata").textContent = "{barata_texto}";
const csv_link = document.getElementById("csvlink");
csv_link.href = "{os.path.basename(CSV_PATH)}?v=" + Date.now();
csv_link.download = "{os.path.basename(CSV_PATH)}";
"""
with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)
print("JS actualizado")