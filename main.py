import json
import os
import pandas as pd
import math
from datetime import datetime

# =========================
# CONFIG
# =========================
DOCS = "docs"
JS_DIR = os.path.join(DOCS, "js")
os.makedirs(JS_DIR, exist_ok=True)

# =========================
# INPUTS (CONTROLADOS)
# =========================
precios = globals().get('precios') or []
df_hoy = globals().get('df_hoy')

precio_luz = globals().get('precio_luz')
precio_gas = globals().get('precio_gas') or 0.042
fecha_hora = globals().get('fecha_hora') or datetime.now().strftime("%Y-%m-%d %H:%M")

CSV_PATH = globals().get('CSV_PATH') or os.path.join(DOCS, 'datos.csv')

# =========================
# DIAGNÓSTICO BASE
# =========================
errores = []

if not precios:
    errores.append("Sin datos gasolina")

if df_hoy is None or df_hoy.empty:
    errores.append("df_hoy vacío")

# =========================
# LIMPIEZA DF
# =========================
if df_hoy is not None and not df_hoy.empty and 'precio' in df_hoy.columns:
    df_hoy['precio'] = pd.to_numeric(df_hoy['precio'], errors='coerce')
    df_hoy_clean = df_hoy.dropna(subset=['precio'])
else:
    df_hoy_clean = pd.DataFrame()

if df_hoy_clean.empty:
    errores.append("Sin precios válidos")

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
# LUZ ROBUSTA
# =========================
try:
    if isinstance(precio_luz, (int, float)) and not math.isnan(precio_luz):
        if precio_luz < 0.08:
            estado_luz = "🟢 Barata"
        elif precio_luz < 0.15:
            estado_luz = "🟡 Media"
        else:
            estado_luz = "🔴 Cara"

        precio_luz_txt = f"{precio_luz:.3f} €/kWh"
    else:
        raise ValueError("Precio luz inválido")

except:
    estado_luz = "Sin datos"
    precio_luz_txt = "No disponible"
    errores.append("Error precio luz")

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
# ESTADO GLOBAL
# =========================
if errores:
    estado_global = "🟡 " + " | ".join(errores)
else:
    estado_global = "🟢 OK"

# =========================
# SAFE JS
# =========================
def safe_js(text):
    return json.dumps(str(text), ensure_ascii=False)

total_estaciones = len(df_hoy_clean)

csv_filename = os.path.basename(CSV_PATH)

# =========================
# JS FINAL PRO
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
setText('status', {safe_js(estado_global)});

const ts = Date.now();

const csv = document.getElementById('csvlink');
if (csv) csv.href = "{csv_filename}?v=" + ts;

const g = document.getElementById('img_gasolina');
if (g) g.src = "historial_gasolina.png?v=" + ts;

const e = document.getElementById('img_energia');
if (e) e.src = "historial_energia.png?v=" + ts;
"""

# =========================
# WRITE JS
# =========================
with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)

# =========================
# LOGS REALES
# =========================
print("===================================")
print("🔥 MAIN EJECUTADO")
print("===================================")
print(f"📊 Registros válidos: {total_estaciones}")
print(f"⚠️ Errores: {errores if errores else 'Ninguno'}")
print(f"📁 JS generado: {os.path.join(JS_DIR, 'script.js')}")