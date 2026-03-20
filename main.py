import requests, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3, os, time
from datetime import datetime

# Config
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
CSV_PATH = os.path.join(DOCS, f"precios_gasolina_{fecha_hoy}.csv")

# =========================
# Funciones energía robustas
# =========================
def obtener_precio_luz():
    try:
        url = "https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real"
        params = {
            "start_date": f"{fecha_hoy}T00:00",
            "end_date": f"{fecha_hoy}T23:59",
            "time_trunc": "hour"
        }
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        valores = data.get("included", [])[0].get("attributes", {}).get("values", [])
        precios = [v.get("value") for v in valores if v.get("value") is not None]
        if precios:
            return round(sum(precios)/len(precios)/1000, 3)
    except Exception as e:
        print("⚠️ Error obteniendo luz:", e)
    return None

def obtener_precio_gas():
    return 0.042  # €/kWh fijo TUR

# =========================
# API gasolina
# =========================
def obtener_api(max_intentos=5, delay=10):
    headers = {"User-Agent":"Mozilla/5.0"}
    for i in range(max_intentos):
        try:
            r = requests.get(URL, headers=headers, timeout=20)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Intento {i+1} error API gasolina: {e}")
            if i < max_intentos-1: time.sleep(delay)
    return None

# =========================
# Datos gasolina
# =========================
data = obtener_api()
precios = []
if data:
    for e in data.get("ListaEESSPrecio", []):
        if MARCA in e.get("Rótulo","").upper() and MUNICIPIO in e.get("Municipio","").upper():
            precio = e.get(TIPO)
            if precio and precio.strip():
                try:
                    precios.append({
                        "fecha": fecha_hoy,
                        "estacion": e.get("Rótulo"),
                        "direccion": e.get("Dirección"),
                        "precio": float(precio.replace(",","."))
                    })
                except:
                    pass

# CSV diario
df_hoy = pd.DataFrame(precios) if precios else pd.DataFrame([{
    "fecha": fecha_hoy,"estacion":"No hay datos","direccion":"No hay datos","precio":0
}])
df_hoy.to_csv(CSV_PATH, index=False, sep=';')

# =========================
# SQLite gasolina + energía
# =========================
precio_luz = obtener_precio_luz()
precio_gas = obtener_precio_gas()
conn = sqlite3.connect(DB)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS precios_gasolina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT, estacion TEXT, direccion TEXT, precio REAL
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS energia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT, luz REAL, gas REAL
)""")
conn.commit()

for p in precios:
    cursor.execute("SELECT 1 FROM precios_gasolina WHERE fecha=? AND estacion=? AND direccion=?",
                   (p["fecha"], p["estacion"], p["direccion"]))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO precios_gasolina (fecha, estacion, direccion, precio) VALUES (?,?,?,?)",
                       (p["fecha"], p["estacion"], p["direccion"], p["precio"]))

cursor.execute("SELECT 1 FROM energia WHERE fecha=?", (fecha_hoy,))
if not cursor.fetchone():
    cursor.execute("INSERT INTO energia (fecha, luz, gas) VALUES (?,?,?)",
                   (fecha_hoy, precio_luz if precio_luz else 0, precio_gas))
conn.commit()
conn.close()

# =========================
# Gráficos gasolina
# =========================
df_all = pd.read_sql_query("SELECT * FROM precios_gasolina", sqlite3.connect(DB))
plt.figure(figsize=(8,5))
for dir in df_all["direccion"].unique():
    sub = df_all[df_all["direccion"]==dir]
    plt.plot(sub["fecha"], sub["precio"], marker="o", label=dir)
plt.title("Gasolina 95 Repsol - Seseña")
plt.xlabel("Fecha")
plt.ylabel("Precio (€)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(DOCS,"historial_gasolina.png"))

# Gráfico energía
plt.figure(figsize=(8,5))
plt.plot([fecha_hoy], [precio_luz if precio_luz else 0], marker="o", color="orange", label="Luz €/kWh")
plt.plot([fecha_hoy], [precio_gas], marker="o", color="red", label="Gas €/kWh")
plt.title("Energía - Luz y Gas")
plt.xlabel("Fecha")
plt.ylabel("€/kWh")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(DOCS,"historial_energia.png"))

# =========================
# JS dinámico final
# =========================
min_row = df_hoy.loc[df_hoy['precio'].idxmin()]
barata_texto = f"💰 {min_row['estacion']} - {min_row['direccion']}: {min_row['precio']} € ¡Mejor precio!"

if precio_luz is not None:
    if precio_luz < 0.08: estado_luz="🟢 Barata"
    elif precio_luz < 0.15: estado_luz="🟡 Media"
    else: estado_luz="🔴 Cara"
else:
    estado_luz = "⚪ Sin datos"
    precio_luz = "No disponible"

js_code = f"""
document.getElementById('barata').textContent = "{barata_texto}";
document.getElementById('luz').textContent = "{precio_luz} €/kWh ({estado_luz})";
document.getElementById('gas').textContent = "{precio_gas} €/kWh";

const ts = Date.now();
document.getElementById('csvlink').href = "{os.path.basename(CSV_PATH)}?v=" + ts;
document.getElementById('csvlink').download = "{os.path.basename(CSV_PATH)}";
document.getElementById('img_gasolina').src = "historial_gasolina.png?v=" + ts;
document.getElementById('img_energia').src = "historial_energia.png?v=" + ts;
"""

with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)

print("✅ JS actualizado con valores reales y refresco de gráficos/CSV 🚀")