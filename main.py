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