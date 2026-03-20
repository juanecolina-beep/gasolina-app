# =========================
# SQLite gasolina + energía
# =========================
conn = sqlite3.connect(DB)
cursor = conn.cursor()

# Tabla gasolina
cursor.execute("""
CREATE TABLE IF NOT EXISTS precios_gasolina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    estacion TEXT,
    direccion TEXT,
    precio REAL
)
""")

# Tabla energía
cursor.execute("""
CREATE TABLE IF NOT EXISTS energia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    luz REAL,
    gas REAL
)
""")
conn.commit()

# Insert gasolina si no existe
for p in precios:
    cursor.execute("""
    SELECT 1 FROM precios_gasolina WHERE fecha=? AND estacion=? AND direccion=?
    """, (p["fecha"], p["estacion"], p["direccion"]))
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO precios_gasolina (fecha, estacion, direccion, precio)
        VALUES (?, ?, ?, ?)
        """, (p["fecha"], p["estacion"], p["direccion"], p["precio"]))

# Insert energía si no existe
cursor.execute("SELECT 1 FROM energia WHERE fecha=?", (fecha_hoy,))
if not cursor.fetchone():
    cursor.execute("""
    INSERT INTO energia (fecha, luz, gas) VALUES (?, ?, ?)
    """, (fecha_hoy, precio_luz if precio_luz else 0, precio_gas))
conn.commit()
conn.close()

# =========================
# JS actualizado para web
# =========================
barata_texto = f"💰 {df_hoy.loc[df_hoy['precio'].idxmin()]['estacion']} - {df_hoy.loc[df_hoy['precio'].idxmin()]['direccion']}: {df_hoy.loc[df_hoy['precio'].idxmin()]['precio']} € ¡Mejor precio!"

estado_luz = "Sin datos"
if precio_luz is not None:
    if precio_luz < 0.08:
        estado_luz = "🟢 Barata"
    elif precio_luz < 0.15:
        estado_luz = "🟡 Media"
    else:
        estado_luz = "🔴 Cara"

js_code = f"""
document.getElementById('barata').textContent = "{barata_texto}";

var luzElem = document.getElementById('luz');
if(luzElem) {{
    luzElem.textContent = "{precio_luz if precio_luz else 'No disponible'} €/kWh ({estado_luz})";
}}

var gasElem = document.getElementById('gas');
if(gasElem) {{
    gasElem.textContent = "{precio_gas} €/kWh";
}}

// CSV
const csv_link = document.getElementById('csvlink');
csv_link.href = "{os.path.basename(CSV_PATH)}?v=" + Date.now();
csv_link.download = "{os.path.basename(CSV_PATH)}";

// Forzar refresco imágenes de gráficos para evitar cache
document.querySelectorAll('img').forEach(img => {{
    img.src = img.src.split('?')[0] + "?v=" + Date.now();
}});
"""

with open(os.path.join(JS_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js_code)

print("JS actualizado con gasolina, luz y gas, evitando 'Cargando...' 🚀")