# 🛠️ Guía de Personalización y Desarrollo

## 📋 Tabla de Contenidos

1. [Ajustes Básicos](#ajustes-básicos)
2. [Modificar Datos](#modificar-datos)
3. [Personalizar Interfaz](#personalizar-interfaz)
4. [Conectar APIs Reales](#conectar-apis-reales)
5. [Agregar Nuevas Funcionalidades](#agregar-nuevas-funcionalidades)

---

## 🔧 Ajustes Básicos

### Cambiar Parámetros de Consumo

**Archivo**: `main.py` (líneas 20-22)

```python
# Electricidad
CONSUMO_DIARIO_KWH = 25        # ← Cambiar consumo diario
# Ejemplo: departamento = 15, casa grande = 35

# Gasolina
PRESUPUESTO_GASOLINA = 100     # ← Cambiar presupuesto
# Ejemplo: zona rural = 200, zona urbana = 80

# Referencia de precio (solo informativo)
PRECIO_LITRO_GASOLINA = 1.769  # ← Actualizar precio actual
```

### Resultado después de cambiar
```bash
python main.py
# Regenera datos.json con nuevos parámetros
# Recarga página en navegador para ver cambios
```

---

## 📊 Modificar Datos

### 1. Cambiar Precios Base de Electricidad

**Archivo**: `main.py` función `generar_precios_electricidad()` (líneas 40-42)

```python
precios_base = [
    0.065, 0.058, 0.052, 0.048, 0.055, 0.072,  # 00-05: Más barato
    # ...
]
# Multiplica todos por factor para simular subida/bajada de tarifa
# Ej: 0.065 * 1.10 = sube 10%
```

### 2. Cambiar Consumo de Gas

**Archivo**: `main.py` función `generar_tarifa_gas()` (línea 105)

```python
consumo_diario_gas = 8         # kWh/día
# Cambiar según tu consumo real (invierno más alto, verano más bajo)
```

### 3. Cargar Datos Reales de Gasolineras

**Opción 1**: Editar CSV directamente

```csv
estacion,precio
Gasolina Express,1.749
Shell Premium,1.789
```

**Opción 2**: Script para importar datos

```python
# Añadir en main.py
def cargar_datos_gasolina_desde_api():
    # Conectar a API Globalhub
    response = requests.get('https://api.globalhub.es/precios')
    return response.json()
```

---

## 🎨 Personalizar Interfaz

### 1. Cambiar Colores del Dashboard

**Archivo**: `docs/index.html` (líneas 20-28)

```css
:root {
    --primary: #667eea;        /* Púrpura - cambiar a #1f2937 */
    --secondary: #764ba2;      /* Secundario - cambiar a #3b82f6 */
    --success: #10b981;        /* Verde - OK */
    --warning: #f59e0b;        /* Amarillo - Atención */
    --danger: #ef4444;         /* Rojo - Crítico */
}
```

**Ejemplos de paletas**:
- Dark: `--primary: #1f2937`, `--secondary: #374151`
- Ocean: `--primary: #0369a1`, `--secondary: #06b6d4`
- Forest: `--primary: #15803d`, `--secondary: #059669`

### 2. Cambiar Logo/Título

**Archivo**: `docs/index.html` línea 6 y 91

```html
<!-- Cambiar en <head> -->
<title>Mi Dashboard Personal - Ahorro de Energía</title>

<!-- Cambiar en <header> -->
<h1>🏠 Mi Casa Inteligente</h1>
<p>Control de gastos mensuales</p>
```

### 3. Cambiar Fuentes

**Archivo**: `docs/index.html` línea 33

```css
font-family: 'Roboto', 'Ubuntu', sans-serif;  /* Cambiar aquí */
```

Opciones: `'Arial'`, `'Verdana'`, `'Times New Roman'`, `'Georgia'`

---

## 🔌 Conectar APIs Reales

### 1. API OMIE (Precios Electricidad)

```python
# En main.py, reemplazar generar_precios_electricidad()

def generar_precios_electricidad():
    try:
        # API OMIE
        url = "https://www.omie.es/api/publicador/instrumentos/precios"
        response = requests.get(url)
        datos = response.json()
        
        # Procesar datos...
        return {
            'horas': datos['precios'],
            # ...
        }
    except:
        # Fallback a datos simulados
        return simular_precios()
```

### 2. API Naturgy (Tarifa Gas)

```python
# Naturgy publica tarifas en:
# https://www.naturgy.es/hogar/tarifas

def generar_tarifa_gas():
    try:
        # Conexión manual a web o API
        response = requests.get('https://www.naturgy.es/hogar/tarifas')
        # Parsear HTML o conectar API
        
        return {
            'precio_kwh': 0.045,
            # ...
        }
    except:
        return simular_tarifa()
```

### 3. API Globalhub (Precios Gasolina)

```python
def cargar_datos_gasolina():
    try:
        # API publica de precios
        response = requests.get(
            'https://www.globalhub.es/api/gasolineras',
            params={'longitud': -3.7, 'latitud': 40.4}  # Madrid
        )
        df = pd.DataFrame(response.json())
        return df
    except:
        # Datos por defecto
        return pd.read_csv("precios_gasolina.csv")
```

---

## ✨ Agregar Nuevas Funcionalidades

### 1. Agregar Agua (3ª Utilidad)

**Paso 1**: Crear función en `main.py`

```python
def generar_tarifa_agua():
    """Simula tarifa de agua local"""
    m3_diarios = 0.2  # metros cúbicos
    precio_m3 = 1.50  # €
    
    coste_diario = m3_diarios * precio_m3
    
    return {
        'precio_m3': precio_m3,
        'consumo_diario': m3_diarios,
        'coste_diario': round(coste_diario, 2),
        'coste_mensual': round(coste_diario * 30, 2)
    }
```

**Paso 2**: Agregar a JSON en `generar_datos()`

```python
datos['agua'] = generar_tarifa_agua()
```

**Paso 3**: Procesar en `script.js`

```javascript
function procesarAgua(data) {
    setElement('water-daily', formatMoney(data.coste_diario));
    setElement('water-monthly', formatMoney(data.coste_mensual));
}
```

**Paso 4**: Agregar tarjeta en `index.html`

```html
<div class="card">
    <h2 data-icon="💧">Agua</h2>
    <!-- Contenido similar a gas -->
</div>
```

### 2. Agregar Histórico de Gastos

**Paso 1**: Crear almacenamiento en `script.js`

```javascript
const historial = JSON.parse(localStorage.getItem('historial')) || [];

// Guardar cada día
function guardarHistorial(datos) {
    historial.push({
        fecha: new Date().toISOString(),
        electricidad: datos.electricidad.coste_diario_estimado,
        gas: datos.gas.coste_diario_total,
        gasolina: datos.gasolina.presupuesto.gasto_acumulado
    });
    localStorage.setItem('historial', JSON.stringify(historial));
}
```

**Paso 2**: Crear gráfico histórico

```javascript
function graficoHistorico() {
    // Similar a graficoElectricidad pero con datos mensuales
    const ctx = document.getElementById('historic-chart');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: historial.map(h => new Date(h.fecha).toLocaleDateString()),
            datasets: [{
                label: 'Gasto diario',
                data: historial.map(h => h.total)
            }]
        }
    });
}
```

### 3. Agregar Notificaciones

```javascript
// En script.js cuando el precio cae

function notificar(titulo, opciones) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(titulo, opciones);
    }
}

// Uso
if (electricidad.precio_minimo < 0.06) {
    notificar('⚡ Precio muy bajo!', {
        body: '€0.058/kWh - Hora de usar lavadora'
    });
}
```

---

## 🔗 Integración con Otros Servicios

### Google Sheets
```python
# Enviar datos a Google Sheets
import gspread

gc = gspread.service_account('creds.json')
sh = gc.open("Mi Dashboard")
ws = sh.sheet1
ws.append_row([datetime.now(), datos['electricidad'], datos['gas']])
```

### Telegram Bot
```python
# Enviar alertas por Telegram
import requests

def enviar_alerta_telegram(mensaje):
    TOKEN = 'tu_token'
    CHAT_ID = 'tu_chat_id'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, json={'chat_id': CHAT_ID, 'text': mensaje})
```

### Home Assistant
```python
# Publicar MQTT para Home Assistant
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 1883)
client.publish('home/electricity/price', 0.058)
```

---

## 📱 Customización Avanzada

### Cambiar tipo de gráfico

**Archivo**: `docs/js/script.js` línea 200

```javascript
// Cambiar de:
type: 'bar',

// A:
type: 'line',      // Línea
type: 'area',      // Área
type: 'doughnut',  // Dona
type: 'radar',     // Radar
```

### Agregar más estadísticas

Editar `stats triple` en HTML:

```html
<div class="stats triple">
    <div class="stat-item">
        <div class="stat-label">Nueva métrica</div>
        <div class="stat-value" id="new-stat">--</div>
    </div>
</div>
```

Procesar en JavaScript:
```javascript
setElement('new-stat', formatMoney(valor));
```

---

## 🐛 Debugging

### Ver datos en consola

```javascript
// En script.js
console.log('Datos cargados:', data);
console.log('Electricidad:', data.electricidad);
console.log('Recomendaciones:', data.recomendaciones);
```

### Forzar error para probar

```javascript
// En script.js línea 40
// throw new Error('Test error');
```

### Monitorear actualización

```javascript
// Cada vez que se actualizan datos
console.log('Dashboard actualizado a:', new Date().toLocaleTimeString());
```

---

## 📚 Referencias

- [Chart.js Documentation](https://www.chartjs.org/)
- [MDN CSS Variables](https://developer.mozilla.org/es/docs/Web/CSS/--*)
- [OMIE API](https://www.omie.es/)
- [Globalhub Gasolineras](https://www.globalhub.es/)

---

**¿Preguntas?** Consulta la documentación principal en `README.md`
