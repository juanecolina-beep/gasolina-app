import json
import os
import pandas as pd
import math

# =========================
# SEGURIDAD BASE
# =========================
precios = globals().get('precios', [])
df_hoy = globals().get('df_hoy', pd.DataFrame())

precio_luz = globals().get('precio_luz', None)
precio_gas = globals().get('precio_gas', 0.042)
fecha_hora = globals().get('fecha_hora', "N/A")

CSV_PATH = globals().get('CSV_PATH', 'datos.csv')
JS_DIR = globals().get('JS_DIR', 'js')

sin_datos = precios is None or len(precios) == 0

# =========================
# LIMPIEZA DF
# =========================
if not df_hoy.empty and 'precio' in df_hoy.columns:
    df_hoy['precio'] = pd.to_numeric(df_hoy['precio'], errors='coerce')
    df_hoy_clean = df_hoy.dropna(subset=['precio'])
else:
    df_hoy_clean = pd.DataFrame()

# =========================
# MEJOR PRECIO
# =========================
if not sin_datos and not df_hoy_clean.empty:
    min_row = df_hoy_clean.loc[df_hoy_clean['precio'].idxmin()]
    mejor_precio_txt = f"💰 {min_row.get('estacion','?')} - {min_row.get('precio','?')}€"

    precio_min = float(min_row.get("precio", 999))

    if precio_min < 1.75:
        alerta = "🚨 MUY BARATA"
    elif precio_min < 1.80:
        alerta = "⚠️ Buen precio"
    else:
        alerta = ""
else:
    min_row = None
    mejor_precio_txt = "⚠️ Sin datos disponibles"
    alerta = ""

# =========================
# LUZ
# =========================
if isinstance(precio_luz, (int, float)) and not math.isnan(precio_luz):
    if precio_luz < 0.08:
        estado_luz = "🟢 Barata"
        recomendacion = "💡 Aprovecha"
    elif precio_luz < 0.15:
        estado_luz = "🟡 Media"
        recomendacion = "⚖️ Normal"
    else:
        estado_luz = "🔴 Cara"
        recomendacion = "🚫 Evita consumo"

    precio_luz_txt = f"{precio_luz:.3f} €/kWh"
else:
    estado_luz = "Sin datos"
    recomendacion = ""
    precio_luz_txt = "No disponible"

# =========================
# TOP 3
# =========================
if not sin_datos and not df_hoy_clean.empty:
    top3 = df_hoy_clean.nsmallest(3, 'precio')

    top3_texto = "\n".join([
        f"{i+1}. {r.get('estacion','?')} - {r.get('precio','?')}€"
        for i, (_, r) in enumerate(top3.iterrows())
    ])
else:
    top3_texto = "Sin datos disponibles"

# =========================
# SAFE JS
# =========================
def safe_js(text):
    return json.dumps(str(text), ensure_ascii=False)

# =========================
# JS FINAL
# =========================
total_estaciones = len(precios) if not sin_datos else 0

js_code = f"""
document.getElementById('barata').textContent = {safe_js(mejor_precio_txt + (" " + alerta if alerta else ""))};

document.getElementById('luz').textContent =
{safe_js(f"{precio_luz_txt} ({estado_luz}) {recomendacion}")};

document.getElementById('gas').textContent =
{safe_js(f"{float(precio_gas):.3f} €/kWh")};

document.getElementById('update').textContent =
{safe_js(f"🕒 Última actualización: {fecha_hora}")};

document.getElementById('total').textContent =
{safe_js(f"⛽ Estaciones analizadas: {total_estaciones}")};

document.getElementById('top3').textContent =
{safe_js(top3_texto)};

const ts = Date.now();
document.getElementById('csvlink').href =
"{os.path.basename(CSV_PATH)}?v=" + ts;

document.getElementById('img_gasolina').src =
"historial_gasolina.png?v=" + ts;

document.getElementById('img_energia').src =
"historial_energia.png?v=" + ts;
"""

# =========================
# ESCRITURA
# =========================
os.makedirs(JS_DIR, exist_ok=True)

with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)

# =========================
# LOGS
# =========================
print("🔥 SISTEMA PRO ULTRA ESTABLE ACTIVO")
print(f"📊 Registros: {total_estaciones}")
print(f"⛽ Min precio: {min_row['precio'] if min_row is not None else 'N/A'}")
print(f"⚡ Luz: {precio_luz}")