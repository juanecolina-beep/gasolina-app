import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import os
import time

URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
MARCA = "REPSOL"
MUNICIPIO = "SESEÑA"
TIPO = "Precio Gasolina 95 E5"
DB = "gasolina.db"

DOCS = "docs"
JS_DIR = os.path.join(DOCS, "js")
os.makedirs(JS_DIR, exist_ok=True)

CSV_PATH = "precios_gasolina.csv"

# --- FUNCION PARA REINTENTOS ---
def obtener_api(max_intentos=3, delay=5):
    for intento in range(max_intentos):
        try:
            print(f"Consultando API del Ministerio... intento {intento+1}")
            response = requests.get(URL, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al consultar API (intento {intento+1}/{max_intentos}): {e}")
            if intento < max_intentos - 1:
                time.sleep(delay)
            else:
                print("No se pudo obtener datos de la API después de varios intentos")
                return None

data = obtener_api()

# --- Generar CSV vacío si falla la API ---
if not data:
    with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write("fecha;estacion;direccion;precio\n")
        f.write("Error;No hay datos;No hay datos;0\n")
    print(f"CSV vacío generado en {CSV_PATH}")
    exit(0)

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
                    "fecha": datetime.now().strftime("%Y-%m-%d"),
                    "estacion": e.get("Rótulo"),
                    "direccion": e.get("Dirección"),
                    "precio": precio_f
                })
            except:
                pass

if not precios:
    print("No se encontraron estaciones Repsol en Seseña")
    with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write("fecha;estacion;direccion;precio\n")
        f.write("Error;No hay datos;No hay datos;0\n")
    exit(0)

print(f"Se encontraron {len(precios)} estaciones.")

# --- Base de datos ---
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

# Guardar precios sin duplicar
for p in precios:
    cursor.execute("""
    SELECT 1 FROM precios_gasolina
    WHERE fecha=? AND estacion=? AND direccion=?
    """, (p["fecha"], p["estacion"], p["direccion"]))
    
    if cursor.fetchone():
        print("Precio ya registrado hoy:", p["precio"])
    else:
        cursor.execute("""
        INSERT INTO precios_gasolina (fecha, estacion, direccion, precio)
        VALUES (?, ?, ?, ?)
        """, (p["fecha"], p["estacion"], p["direccion"], p["precio"]))
        print("Guardado:", p["precio"])

conn.commit()

# --- DataFrame para análisis ---
df = pd.read_sql_query("SELECT * FROM precios_gasolina", conn)
conn.close()

if len(df) == 0:
    print("No hay datos para gráfico")
    exit(0)

# Gráfico histórico
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
plt.savefig(os.path.join(DOCS, "historial_gasolina.png"))
print("Gráfico guardado en docs/historial_gasolina.png")

# Guardar CSV
df.to_csv(CSV_PATH, index=False, sep=';')
print(f"CSV guardado en {CSV_PATH}")

# --- Calcular gasolinera más barata ---
min_row = df.loc[df['precio'].idxmin()]
print(f"💰 Gasolinera más barata: {min_row['estacion']} - {min_row['direccion']} : {min_row['precio']} €")

# JS para mostrar gasolinera más barata
js_code = f"""
fetch('precios_gasolina.csv?t=' + Date.now())
.then(response => response.text())
.then(text => {{
    const lines = text.split('\\n').slice(1);
    let minPrecio = Infinity;
    let minEstacion = '';
    for (let line of lines) {{
        if(!line) continue;
        const [fecha, estacion, direccion, precio] = line.split(';');
        const p = parseFloat(precio);
        if (!isNaN(p) && p < minPrecio) {{
            minPrecio = p;
            minEstacion = `${{estacion}} - ${{direccion}}`;
        }}
    }}
    document.getElementById('barata').textContent = minPrecio === Infinity ? "No hay precios válidos" : `💰 ${{minEstacion}}: ${{minPrecio}} € ¡Mejor precio!`;
}})
.catch(() => {{
    document.getElementById('barata').textContent = "No se pudo cargar el CSV";
}});
"""
with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)
print("JS guardado en docs/js/script.js")