import json

# =========================
# INTELIGENCIA SEGURA
# =========================

sin_datos = len(precios) == 0

# -------------------------
# MEJOR PRECIO (SAFE)
# -------------------------
if not sin_datos and len(df_hoy) > 0:
    min_row = df_hoy.loc[df_hoy['precio'].idxmin()]
    mejor_precio_txt = f"💰 {min_row['estacion']} - {min_row['precio']}€"
    if min_row["precio"] < 1.75:
        alerta = "🚨 MUY BARATA"
    elif min_row["precio"] < 1.80:
        alerta = "⚠️ Buen precio"
    else:
        alerta = ""
else:
    min_row = None
    mejor_precio_txt = "⚠️ Sin datos disponibles"
    alerta = ""

# -------------------------
# LUZ (SAFE)
# -------------------------
if precio_luz is not None:
    if precio_luz < 0.08:
        estado_luz = "🟢 Barata"
        recomendacion = "💡 Aprovecha"
    elif precio_luz < 0.15:
        estado_luz = "🟡 Media"
        recomendacion = "⚖️ Normal"
    else:
        estado_luz = "🔴 Cara"
        recomendacion = "🚫 Evita consumo"
    precio_luz_txt = f"{precio_luz} €/kWh"
else:
    estado_luz = "Sin datos"
    recomendacion = ""
    precio_luz_txt = "No disponible"

# -------------------------
# TOP 3 (SAFE)
# -------------------------
if not sin_datos and len(df_hoy) > 0:
    top3 = df_hoy.nsmallest(3, 'precio')
    top3_texto = "\\n".join([
        f"{i+1}. {r['estacion']} - {r['precio']}€"
        for i, (_, r) in enumerate(top3.iterrows())
    ])
else:
    top3_texto = "Sin datos disponibles"

# =========================
# SANITIZAR PARA JS (CLAVE)
# =========================
def safe_js(text):
    return json.dumps(text, ensure_ascii=False)

# =========================
# JS FINAL PRO
# =========================
js_code = f"""
// MEJOR PRECIO
document.getElementById('barata').textContent = {safe_js(mejor_precio_txt + (" " + alerta if alerta else ""))};

// ENERGÍA
document.getElementById('luz').textContent = {safe_js(f"{precio_luz_txt} ({estado_luz}) {recomendacion}")};
document.getElementById('gas').textContent = {safe_js(f"{precio_gas} €/kWh")};

// INFO SISTEMA
document.getElementById('update').textContent = {safe_js(f"🕒 Última actualización: {fecha_hora}")};
document.getElementById('total').textContent = {safe_js(f"⛽ Estaciones analizadas: {len(precios)}")};

// TOP 3
document.getElementById('top3').textContent = {safe_js(top3_texto)};

// CACHE BUSTING
const ts = Date.now();
document.getElementById('csvlink').href = "{os.path.basename(CSV_PATH)}?v=" + ts;
document.getElementById('img_gasolina').src = "historial_gasolina.png?v=" + ts;
document.getElementById('img_energia').src = "historial_energia.png?v=" + ts;
"""

# =========================
# ESCRIBIR JS
# =========================
with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)

# =========================
# LOGS PRO
# =========================
print("🔥 SISTEMA PRO ACTIVO")
print(f"📊 Registros hoy: {len(df_hoy) if 'df_hoy' in globals() else 0}")
print(f"⛽ Precio mínimo: {min_row['precio'] if min_row is not None else 'N/A'}")
print(f"⚡ Precio luz: {precio_luz}")