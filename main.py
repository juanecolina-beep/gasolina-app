# =========================
# INTELIGENCIA
# =========================
min_row = df_hoy.loc[df_hoy['precio'].idxmin()]

alerta = ""
if min_row["precio"] < 1.75:
    alerta = "🚨 MUY BARATA"
elif min_row["precio"] < 1.80:
    alerta = "⚠️ Buen precio"

# Control de datos reales
sin_datos = len(precios) == 0

# Estado luz + recomendación
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

# TOP 3
top3 = df_hoy.nsmallest(3, 'precio')
top3_texto = "\\n".join([f"{i+1}. {r['estacion']} - {r['precio']}€" for i,(_,r) in enumerate(top3.iterrows())])

# =========================
# JS FINAL PRO
# =========================
js_code = f"""
// MEJOR PRECIO
document.getElementById('barata').textContent = "{'⚠️ Sin datos disponibles' if sin_datos else f'💰 {min_row['estacion']} - {min_row['precio']}€ {alerta}'}";

// ENERGÍA
document.getElementById('luz').textContent = "{precio_luz_txt} ({estado_luz}) {recomendacion}";
document.getElementById('gas').textContent = "{precio_gas} €/kWh";

// INFO SISTEMA
document.getElementById('update').textContent = "🕒 Última actualización: {fecha_hora}";
document.getElementById('total').textContent = "⛽ Estaciones analizadas: {len(precios)}";

// TOP 3 (YA NO EN CONSOLA 🔥)
document.getElementById('top3').textContent = `{top3_texto}`;

// Cache busting
const ts = Date.now();
document.getElementById('csvlink').href = "{os.path.basename(CSV_PATH)}?v=" + ts;
document.getElementById('img_gasolina').src = "historial_gasolina.png?v=" + ts;
document.getElementById('img_energia').src = "historial_energia.png?v=" + ts;
"""

with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)

print("🔥 SISTEMA PRO ACTIVO")
print(f"📊 Registros hoy: {len(df_hoy)}")
print(f"⛽ Precio mínimo: {min_row['precio']}")
print(f"⚡ Precio luz: {precio_luz}")