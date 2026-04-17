# 💡⚡🔥⛽ Dashboard Integral de Energía y Combustible - España

## 🎯 Visión General

Dashboard personal unificado que permite controlar y optimizar **gastos mensuales de energía y combustible** en España en una única vista. Integra:

- ⚡ **Electricidad** (Precios horarios OMIE)
- 🔥 **Gas** (Tarifa TUR Naturgy)
- ⛽ **Gasolina** (Con control de presupuesto)
- 💰 **Resumen Financiero Unificado**
- 💡 **Recomendaciones Inteligentes de Ahorro**

---

## 📊 Características Principales

### 1. ⚡ CONTROL DE ELECTRICIDAD

#### Información mostrada:
- 🟢 Precio más barato del día (€/kWh)
- 🟡 Precio promedio
- 🔴 Precio más caro
- **Mejor ventana de consumo** (ej: 02:00-06:00)
- Consumo diario estimado: **25 kWh/día** (configurable)
- Coste diario y mensual proyectado
- **Gráfico de precios horarios** (24h) con código de colores

#### Recomendaciones automáticas:
> "Usa lavadora y lavavajillas entre 02:00-06:00 para ahorrar 15%"

---

### 2. 🔥 CONTROL DE GAS

#### Información mostrada:
- Precio actual TUR (€/kWh)
- Término fijo diario
- Tipo de tarifa: **T1 - Residencial**
- Consumo estimado: **8 kWh/día**
- Coste variable diario
- Coste total diario (variable + fijo)
- Coste mensual proyectado
- **Alerta de cambios de tarifa**

---

### 3. ⛽ CONTROL DE GASOLINA

#### Información mostrada:
- 🏆 Mejor precio actual (Gasolina 95)
- 📍 Gasolinera más económica
- Precio promedio
- Precio más alto
- **Top 3 gasolineras más baratas** (ranking con medallas)
- Total de estaciones analizadas

---

### 4. 💳 PRESUPUESTO MENSUAL DE COMBUSTIBLE

#### Control integrado:
- **Presupuesto**: 100€ mensuales (configurable)
- Gasto acumulado actual
- Saldo restante
- Porcentaje de consumo (barra de progreso visual)
- Días restantes del mes
- Gasto diario recomendado
- **Alertas inteligentes**:
  - ✅ "Presupuesto saludable"
  - ⚠️ "Te quedan pocos fondos"

---

### 5. 📊 PANEL FINANCIERO UNIFICADO

Resumen mensual estimado visible en la parte superior:

| Concepto | Costo |
|----------|-------|
| ⚡ Electricidad | 750€/mes |
| 🔥 Gas | 240€/mes |
| ⛽ Gasolina | 100€/mes |
| **💰 TOTAL** | **1.090€/mes** |

---

### 6. 💡 RECOMENDACIONES DE AHORRO

El dashboard genera automáticamente recomendaciones personalizadas:

- 💚 Consejos de horarios para consumo eléctrico
- 🔥 Alertas de cambios de tarifa de gas
- ⛽ Avisos de presupuesto de combustible
- 💡 Consejos generales diarios

Cada recomendación muestra el **ahorro estimado en euros**.

---

## 🏗️ Arquitectura Técnica

### Backend (Python)
**Archivo**: `main.py`

#### Funciones principales:

1. **`generar_precios_electricidad()`**
   - Simula precios OMIE horarios (0-24h)
   - Patrón realista: bajo en madrugada, alto en tarde
   - Calcula mejor ventana de 4h
   - Genera detalle por hora con categorías

2. **`generar_tarifa_gas()`**
   - Simula TUR Naturgy T1 (residencial)
   - Componentes: término fijo + variable
   - Alerta de cambios de tarifa

3. **`cargar_datos_gasolina()` y `analizar_gasolina()`**
   - Lee CSV con datos de gasolineras
   - Calcula presupuesto mensual
   - Genera top 3 estaciones

4. **`generar_recomendaciones()`**
   - Crea sugerencias personalizadas
   - Calcula ahorro estimado

5. **`generar_datos()`**
   - Orquesta todo
   - Genera `datos.json` completo

### Frontend (HTML/CSS/JavaScript)
**Archivos**: `docs/index.html`, `docs/js/script.js`

#### Características:

- ✨ Diseño moderno con gradientes
- 📱 Responsive 100% (móvil, tablet, desktop)
- 📊 Gráficos interactivos con Chart.js
- 🎨 Sistema de colores inteligente (verde/amarillo/rojo)
- ♿ Accesible y bien estructurado
- ⚡ Actualización dinámica cada 10 minutos

---

## 📈 Datos Generados (JSON)

La aplicación genera `docs/datos.json` con estructura:

```json
{
  "timestamp": "2026-04-17T17:45:21",
  "status": "ok",
  "resumen_financiero": {
    "electricidad": 750.00,
    "gas": 240.00,
    "gasolina": 100.00,
    "total_mensual": 1090.00,
    "moneda": "EUR"
  },
  "electricidad": { /* precios horarios */ },
  "gas": { /* tarifa TUR */ },
  "gasolina": { /* precios y presupuesto */ },
  "recomendaciones": [ /* consejos de ahorro */ ]
}
```

---

## 🚀 Cómo Usar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Generar datos
```bash
python main.py
```

Esto creará `docs/datos.json` con los datos simulados.

### 3. Ver dashboard
- Abre `docs/index.html` en navegador
- Los datos se cargan automáticamente desde `datos.json`
- Se actualiza cada 10 minutos (configurable)

---

## 📋 Configuración

Edita `main.py` líneas 20-22 para personalizar:

```python
CONSUMO_DIARIO_KWH = 25        # Cambiar consumo diario de electricidad
PRESUPUESTO_GASOLINA = 100     # Cambiar presupuesto mensual
PRECIO_LITRO_GASOLINA = 1.769  # Cambiar precio referencia
```

---

## 🎨 Paleta de Colores

| Color | Significado | Uso |
|-------|-------------|-----|
| 🟢 Verde | Ahorro / Bueno | Precios bajos, presupuesto saludable |
| 🟡 Amarillo | Atención | Precios medios, alerta suave |
| 🔴 Rojo | Gasto alto | Precios caros, presupuesto crítico |
| 🟣 Púrpura | Principal | Títulos, primaria |

---

## 📱 Responsive Design

- **Desktop**: Grid de 3-4 columnas, gráficos grandes
- **Tablet**: Grid de 2 columnas, proporción optimizada
- **Móvil**: Stack único, todo adaptado

---

## 🔄 Flujo de Datos

```
main.py (genera datos)
    ↓
docs/datos.json (almacena)
    ↓
script.js (carga JSON)
    ↓
index.html (renderiza)
    ↓
Usuario (ve dashboard)
```

---

## 🧠 Comportamiento Inteligente

1. **Análisis automático**: Detecta horas baratas, alertas tarifarias
2. **Recomendaciones personalizadas**: Basadas en patrones
3. **Control de presupuesto**: Con alertas en tiempo real
4. **Gráficos interactivos**: Hover para detalles
5. **Actualización periódica**: Cada 10 minutos (configurable)

---

## 📊 Datos de Ejemplo

### Gasolina
- **Mejor**: Gasolina Express @ 1.749€/L 🟢
- **Promedio**: 1.773€/L
- **Peor**: BP Energía @ 1.799€/L 🔴

### Electricidad (Horario hoy)
- **Mínima**: 0.048€/kWh (05:00) 🟢
- **Máxima**: 0.245€/kWh (19:00) 🔴
- **Mejor ventana**: 02:00-06:00 (0.058€/kWh)

### Gas (TUR T1)
- **Precio**: 0.042-0.052€/kWh
- **Término fijo**: 0.35€/día
- **Total diario**: 6.70€/día aprox.

---

## 🔧 Mantenimiento

### Actualizar precios reales
Para conectar APIs reales (OMIE, Naturgy, etc.):

1. Reemplazar funciones `generar_*` con llamadas HTTP
2. Usar APIs: 
   - OMIE: https://www.omie.es/
   - Globalhub Gasolineras: https://www.globalhub.es/

### Agregar más datos
- Modificar `resumen_financiero` en `generar_datos()`
- Extender `recomendaciones` con nuevo tipo

---

## 📝 Notas Importantes

- ✅ Datos **simulados** pero **realistas** (patrones España)
- ✅ Presupuesto de gasolina aleatorio (40-90% mes)
- ✅ Totalmente **funcional** como demo/prototipo
- ✅ Listo para integrar APIs reales

---

## 🚀 Próximas Mejoras

- [ ] Conectar API OMIE para precios reales
- [ ] Integrar API Naturgy para tarifa actual
- [ ] Histórico de gastos (gráficos mensuales)
- [ ] Notificaciones cuando hay precio bajo
- [ ] Exportar a PDF/CSV
- [ ] Dark mode
- [ ] Almacenamiento local (IndexedDB)
- [ ] Comparativa mes anterior

---

**Desarrollado con ❤️ para ahorrar dinero en España** 💚
