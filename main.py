import json
import os
import pandas as pd
import math
from datetime import datetime

# =========================
# DEFAULT SAFE VALUES
# =========================
precios = globals().get('precios') or []
df_hoy = globals().get('df_hoy')

precio_luz = globals().get('precio_luz')
precio_gas = globals().get('precio_gas') or 0.042
fecha_hora = globals().get('fecha_hora') or datetime.now().strftime("%Y-%m-%d %H:%M")

CSV_PATH = globals().get('CSV_PATH') or 'datos.csv'
JS_DIR = globals().get('JS_DIR') or 'js'

sin_datos = (df_hoy is None or df_hoy.empty or len(precios) == 0)

# =========================
# SAFE DF
# =========================
if df_hoy is not None and not df_hoy.empty and 'precio' in df_hoy.columns:
    df_hoy['precio'] = pd.to_numeric(df_hoy['precio'], errors='coerce')
    df_hoy_clean = df_hoy.dropna(subset=['precio'])
else:
    df_hoy_clean = pd.DataFrame()

# =========================
# MEJOR PRECIO
# =========================
if not df_hoy_clean.empty:
    min_row = df_hoy_clean.loc[df_hoy_clean['precio'].idxmin()]
    precio_min = float(min_row['precio'])

    mejor_precio_txt = f"💰 {min_row.get('estacion','?')} - {precio_min:.3f}€"

    if precio_min < 1.75:
        alerta = "🚨 MUY BARATA"
    elif precio_min < 1.85:
        alerta = "⚠️ Buen precio"
    else:
        alerta = "🔥 Caro"
else:
    mejor_precio_txt = "⚠️ Sin datos disponibles"
    alerta = ""

# =========================
# LUZ SAFE
# =========================
if isinstance(precio_luz, (int, float)) and not math.isnan(precio_luz):
    if precio_luz < 0.08:
        estado_luz = "🟢 Barata"
    elif precio_luz < 0.15:
        estado_luz = "🟡 Media"
    else:
        estado_luz = "🔴 Cara"

    precio_luz_txt = f"{precio_luz:.3f} €/kWh"
else:
    estado_luz = "Sin datos"
    precio_luz_txt = "No disponible"

# =========================
# TOP 3
# =========================
if not df_hoy_clean.empty:
    top3 = df_hoy_clean.nsmallest(3, 'precio')
    top3_texto = "\n".join(
        f"{i+1}. {r['estacion']} - {float(r['precio']):.3f}€"
        for i, (_, r) in enumerate(top3.iterrows())
    )
else:
    top3_texto = "Sin datos disponibles"

# =========================
# SAFE JS ESCAPE
# =========================
def safe_js(text):
    return json.dumps(str(text), ensure_ascii=False)

total_estaciones = len(df_hoy_clean)

# =========================
# JS FINAL (ROBUSTO)
# =========================
js_code = f"""
function setText(id, value) {{
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}}

setText('barata', {safe_js(mejor_precio_txt + " " + alerta)});
setText('luz', {safe_js(f"{precio_luz_txt} ({estado_luz})")});
setText('gas', {safe_js(f"{precio_gas:.3f} €/kWh")});
setText('update', {safe_js(f"🕒 {fecha_hora}")});
setText('total', {safe_js(f"⛽ Estaciones: {total_estaciones}")});
setText('top3', {safe_js(top3_texto)});

const ts = Date.now();

const csv = document.getElementById('csvlink');
if (csv) csv.href = "{os.path.basename(CSV_PATH)}?v=" + ts;

const g = document.getElementById('img_gasolina');
if (g) g.src = "historial_gasolina.png?v=" + ts;

const e = document.getElementById('img_energia');
if (e) e.src = "historial_energia.png?v=" + ts;
"""

os.makedirs(JS_DIR, exist_ok=True)

with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)

print("✅ SCRIPT GENERADO CORRECTAMENTE")
print(f"📊 Registros: {total_estaciones}")