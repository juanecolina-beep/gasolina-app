# 🗺️ ROADMAP EJECUTIVO - Energy & Fuel Control Center

**Fecha**: 17 Abril 2026 | **Duración Total**: 8 semanas | **Estrategia**: Opción A + B

---

## 📊 VISIÓN GENERAL DEL PLAN

```
SEMANA 1-2: Mejoras Rápidas (Actual HTML/Python)
↓
SEMANA 3-4: APIs Reales + Mapas (Validación usuarios)
↓
SEMANA 5-6: Setup Next.js (Migración gradual)
↓
SEMANA 7-8: Frontend Moderno (Lanzamiento v2)
```

---

## ⚡ SEMANA 1-2: MEJORAS INMEDIATAS AL PROYECTO ACTUAL

### Objetivo
Potenciar el MVP actual con funcionalidades críticas y preparar para APIs reales

### Tareas (14 días)

#### Día 1-2: Conectar API OMIE Real
**Qué**: Reemplazar mock electricidad con datos reales  
**Archivo**: `main.py`

```python
# Antes: Mock con números hardcodeados
precios_base = [0.065, 0.058, ...] # Valores aleatorios

# Después: API real
import requests

def generar_precios_electricidad():
    try:
        # API OMIE: precios horarios últimas 24h
        url = 'https://api.esios.ree.es/archives/70'
        response = requests.get(url)
        datos_omie = response.json()
        
        # Extraer precios de la respuesta
        precios = [float(d['valor']) for d in datos_omie['datos']]
        
        # Continuar con lógica actual...
        return procesar_precios(precios)
    except:
        # Fallback a mock si API falla
        return generar_precios_mock()
```

**Tiempo**: 2 horas  
**Validación**: Verificar que los precios son diferentes cada vez que ejecutas `python main.py`

---

#### Día 2-3: Selector Dinámico de Ciudades
**Qué**: Agregar UI para elegir Seseña vs Aranjuez  
**Archivos**: `docs/index.html` + `docs/js/script.js`

```html
<!-- En header, antes del título -->
<div style="margin-bottom: 20px; text-align: center;">
    <label for="ciudad-selector" style="color: white; font-weight: bold; margin-right: 10px;">
        📍 Selecciona Ciudad:
    </label>
    <select id="ciudad-selector" style="padding: 8px 15px; border-radius: 8px; border: none;">
        <option value="seseña">🔴 Seseña (Repsol)</option>
        <option value="aranjuez">🟦 Aranjuez (Todos)</option>
    </select>
</div>
```

```javascript
// En script.js - Agregar evento
document.getElementById('ciudad-selector').addEventListener('change', async (e) => {
    const ciudad = e.target.value;
    localStorage.setItem('ciudad-seleccionada', ciudad);
    
    // Recargar datos filtrados
    cargarDatos();
});

// En cargarDatos():
const ciudadSeleccionada = localStorage.getItem('ciudad-seleccionada') || 'seseña';
// Filtrar gasolineras por ciudad
```

**Tiempo**: 3 horas  
**Validación**: Al cambiar ciudad, la tabla de gasolineras se actualiza

---

#### Día 3-4: Integración Leaflet.js (Mapa)
**Qué**: Mostrar gasolineras en mapa interactivo  
**Archivo**: `docs/index.html`

```html
<!-- Agregar en <head> -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.min.css" />
<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.min.js"></script>

<!-- Agregar en body (nueva sección) -->
<section class="card grid-full" style="height: 500px; padding: 0;">
    <div id="map" style="height: 100%; border-radius: 20px;"></div>
</section>
```

```javascript
// En script.js - Nueva función
function dibujarMapa(gasolineras) {
    // Inicializar mapa
    const map = L.map('map').setView([40.0, -3.4], 11); // Centrado en zona
    
    // Agregar base layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Agregar pines por gasolinera
    gasolineras.forEach(gas => {
        const color = gas.precio < 1.75 ? 'green' : (gas.precio < 1.85 ? 'yellow' : 'red');
        L.circleMarker([gas.lat, gas.lng], {
            radius: 8,
            fillColor: color,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        })
        .addTo(map)
        .bindPopup(`
            <b>${gas.nombre}</b><br>
            ${gas.precio}€/L<br>
            ${gas.distancia} km
        `);
    });
}
```

**Tiempo**: 4 horas  
**Validación**: El mapa aparece con pines verdes/rojos según precio

---

#### Día 4-5: Modo Oscuro Toggle
**Qué**: Agregar botón para cambiar tema  
**Archivos**: `docs/index.html` + CSS mejorado

```html
<!-- En header, botón -->
<button id="theme-toggle" 
        style="background: rgba(255,255,255,0.2); 
               border: none; 
               color: white; 
               padding: 8px 15px; 
               border-radius: 8px; 
               cursor: pointer; 
               font-size: 18px;">
    🌙
</button>
```

```javascript
// Gestionar tema
const html = document.documentElement;
const isDark = localStorage.getItem('theme') === 'dark';

if (isDark) {
    html.style.filter = 'invert(1)';
    document.body.style.background = '#1f2937';
}

document.getElementById('theme-toggle').addEventListener('click', () => {
    const newDark = html.style.filter !== 'invert(1)';
    html.style.filter = newDark ? 'invert(1)' : 'none';
    localStorage.setItem('theme', newDark ? 'dark' : 'light');
});
```

**Tiempo**: 2 horas  
**Validación**: Toggle funciona y persiste al recargar

---

#### Día 5-6: Comparador Inteligente (Tabla)
**Qué**: Mostrar lado a lado Seseña vs Aranjuez con ahorro calculado  
**Archivo**: `docs/index.html` + `script.js`

```html
<!-- Nueva card después del mapa -->
<div class="card grid-full">
    <h3>⚖️ COMPARADOR: SESEÑA vs ARANJUEZ</h3>
    <table style="width: 100%; margin-top: 20px;">
        <tr>
            <th>Ubicación</th>
            <th>Gasolinera</th>
            <th>Precio</th>
            <th>Distancia</th>
            <th>Recomendación</th>
        </tr>
        <tr id="comp-seseña"></tr>
        <tr id="comp-aranjuez"></tr>
        <tr style="border-top: 2px solid #ccc; font-weight: bold;">
            <td colspan="3">Diferencia: <span id="comp-diferencia">0.00</span>€/L</td>
            <td colspan="2">Ahorro mensual: <span id="comp-ahorro">0.00</span>€</td>
        </tr>
    </table>
</div>
```

```javascript
function mostrarComparador(mejorSeseña, mejorAranjuez) {
    const diferencia = mejorSeseña.precio - mejorAranjuez.precio;
    const ahorroMes = diferencia * 50 * 8; // 50L * 8 depósitos/mes
    
    document.getElementById('comp-seseña').innerHTML = `
        <td>Seseña</td>
        <td>${mejorSeseña.nombre}</td>
        <td><strong>${mejorSeseña.precio}€</strong></td>
        <td>${mejorSeseña.distancia} km</td>
        <td>Repsol oficial</td>
    `;
    
    document.getElementById('comp-aranjuez').innerHTML = `
        <td>Aranjuez</td>
        <td>${mejorAranjuez.nombre}</td>
        <td><strong style="color: green;">${mejorAranjuez.precio}€</strong></td>
        <td>${mejorAranjuez.distancia} km</td>
        <td>${ahorroMes > 5 ? '✅ MÁS BARATA' : 'Similar'}</td>
    `;
    
    document.getElementById('comp-diferencia').textContent = diferencia.toFixed(3);
    document.getElementById('comp-ahorro').textContent = ahorroMes.toFixed(2);
}
```

**Tiempo**: 3 horas  
**Validación**: Tabla muestra datos correctos y cálculo de ahorro

---

#### Día 6-7: Alertas Inteligentes
**Qué**: Sistema de alertas tipo notificación (toast)  
**Archivo**: `docs/js/script.js`

```javascript
function mostrarAlerta(tipo, titulo, mensaje) {
    const alert = document.createElement('div');
    alert.style.cssText = `
        position: fixed; top: 20px; right: 20px; 
        padding: 15px 20px; 
        border-radius: 8px; 
        color: white; 
        z-index: 9999;
        animation: slideInRight 0.3s ease;
        ${tipo === 'success' ? 'background: #10b981;' : ''}
        ${tipo === 'warning' ? 'background: #f59e0b;' : ''}
        ${tipo === 'error' ? 'background: #ef4444;' : ''}
    `;
    alert.innerHTML = `<strong>${titulo}:</strong> ${mensaje}`;
    document.body.appendChild(alert);
    
    setTimeout(() => alert.remove(), 4000);
}

// Usar en recomendaciones:
generar_recomendaciones(electricidad, gas, gasolina).forEach(rec => {
    if (rec.urgencia === 'alta') {
        mostrarAlerta('warning', rec.titulo, rec.descripcion);
    }
});
```

**Tiempo**: 2 horas  
**Validación**: Alertas aparecen y desaparecen automáticamente

---

#### Día 7-8: Refactorizar Python en Módulos
**Qué**: Separar lógica en archivos independientes  
**Estructura**:

```
gasolina-app/
├── main.py (orquestador)
├── modules/
│   ├── __init__.py
│   ├── electricity.py (funciones OMIE)
│   ├── gas.py (funciones TUR)
│   ├── fuel.py (funciones gasolineras)
│   └── recommendations.py (lógica IA)
└── ...
```

```python
# modules/electricity.py
def generar_precios_electricidad():
    """Obtiene datos reales OMIE"""
    pass

# modules/gas.py
def generar_tarifa_gas():
    """Obtiene tarifa TUR Naturgy"""
    pass

# main.py (nuevo)
from modules import electricity, gas, fuel, recommendations

def generar_datos():
    elec = electricity.generar_precios_electricidad()
    gas_data = gas.generar_tarifa_gas()
    fuel_data = fuel.cargar_gasolineras()
    recom = recommendations.generar_recomendaciones(elec, gas_data, fuel_data)
    return {...}
```

**Tiempo**: 4 horas  
**Validación**: `python main.py` funciona igual pero código es modular

---

#### Día 8: Testing y Documentación
**Qué**: Verificar todo funciona, documentar cambios  
**Archivo**: Crear `CAMBIOS_SEMANA1.md`

```markdown
# ✅ Cambios Semana 1-2

## Nuevas Funcionalidades
- [x] API OMIE integrada (datos reales electricidad)
- [x] Selector ciudades (Seseña/Aranjuez)
- [x] Mapa interactivo Leaflet.js
- [x] Modo oscuro toggle
- [x] Comparador inteligente
- [x] Sistema de alertas
- [x] Código modular Python

## Bugs Corregidos
- Electricidad siempre mostraba precios aleatorios
- No había forma de cambiar ciudad
- Faltaba visualización espacial

## Próximos: APIs MITMA + Geolocalización

```

**Tiempo**: 2 horas

---

### 📈 Resultado Esperado Semana 1-2

✅ Dashboard con:
- Precios electricidad reales OMIE
- Mapa interactivo de gasolineras
- Selector dinámico de ciudades
- Comparador Seseña vs Aranjuez
- Modo oscuro funcional
- Código más mantenible

📊 **Métrica de éxito**: Tiempo de carga <2s, sin errores en consola

---

## 🗓️ SEMANA 3-4: APIs REALES + VALIDACIÓN

### Objetivo
Conectar todas las APIs externas y validar con usuarios reales

### Tareas

#### API MITMA Carburantes Completa
```python
# modules/fuel.py - Mejorado
import requests

def cargar_gasolineras_real():
    """Conecta a MITMA Geoportal"""
    url = 'https://geoportal.transportes.gob.es/api/gasolineras'
    
    # Filtrar por localidad
    params = {
        'localidad': 'Aranjuez',
        'tipo_gasolina': '95',
        'sort': 'precio'
    }
    
    response = requests.get(url, params=params)
    return response.json()
```

#### Tarifa TUR Naturgy (Web Scraping)
```python
# modules/gas.py
from selenium import webdriver  # o BeautifulSoup

def obtener_tarifa_tur():
    """Scrapping tarifa actual TUR"""
    # Alternativa: mock + actualización manual
    pass
```

#### Geolocalización + Distancias Reales
```python
# modules/fuel.py
from geopy.distance import geodesic

def calcular_distancias(gasolineras, lat_usuario, lng_usuario):
    """Calcula distancia real a cada gasolinera"""
    for gas in gasolineras:
        dist = geodesic(
            (lat_usuario, lng_usuario),
            (gas['lat'], gas['lng'])
        ).km
        gas['distancia'] = round(dist, 1)
    return gasolineras
```

**Tiempo**: 6 horas  
**Validación**: Ejecutar `python main.py` y ver datos reales en `docs/datos.json`

---

### Testing con Usuarios
- [ ] Mostrar dashboard a 3-5 usuarios reales
- [ ] Recopilar feedback
- [ ] Ajustar según comentarios
- [ ] Documentar insights

**Tiempo**: 8 horas

---

## 📱 SEMANA 5-6: MIGRACIÓN A NEXT.JS

### Objetivo
Preparar infraestructura moderna sin perder funcionalidad

### Fase 1: Setup

```bash
# Terminal
npx create-next-app@latest energy-fuel-control \
  --typescript \
  --tailwind \
  --app \
  --eslint

cd energy-fuel-control
npm install zustand recharts leaflet zod
```

### Fase 2: Estructura Base

```
energy-fuel-control/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx (dashboard)
│   │   └── api/
│   │       ├── electricity.ts
│   │       ├── gas.ts
│   │       └── fuel.ts
│   ├── components/
│   │   ├── ElectricityCard.tsx
│   │   ├── GasCard.tsx
│   │   ├── FuelCard.tsx
│   │   └── ...
│   ├── store/
│   │   └── useEnergyStore.ts
│   └── types/
│       └── index.ts
└── package.json
```

### Fase 3: Componentes Principales (4 días)

```typescript
// src/components/ElectricityCard.tsx
import { Card } from './shared/Card';
import { LineChart } from 'recharts';

export function ElectricityCard() {
  const { electricity } = useEnergyStore();
  
  return (
    <Card icon="⚡" title="Electricidad">
      <LineChart data={electricity.horas} />
      <p>Mejor: {electricity.mejor_ventana.inicio}</p>
    </Card>
  );
}
```

### Fase 4: Store Zustand (1 día)

```typescript
// src/store/useEnergyStore.ts
import create from 'zustand';

interface EnergyStore {
  electricity: Electricity | null;
  gas: Gas | null;
  fuel: Gasolina | null;
  fetchData: () => Promise<void>;
}

export const useEnergyStore = create<EnergyStore>((set) => ({
  electricity: null,
  gas: null,
  fuel: null,
  
  fetchData: async () => {
    const data = await fetch('/api/data').then(r => r.json());
    set({
      electricity: data.electricity,
      gas: data.gas,
      fuel: data.fuel
    });
  }
}));
```

**Tiempo**: 6-8 horas

---

## 🚀 SEMANA 7-8: LANZAMIENTO V2

### Objetivo
Frontend moderno en producción

### Deploy
```bash
# Vercel
vercel deploy

# O manual:
npm run build
npm start
```

### Testing
- [ ] Pruebas en mobil (iOS + Android)
- [ ] Lighthouse score >85
- [ ] Todas las alertas funcionan
- [ ] APIs caen back a mock

**Tiempo**: 4 horas

---

## 📋 CHECKLIST FINAL

### Funcionalidades Críticas (MVP)
- [ ] Dashboard principal visible <2s
- [ ] Precios electricidad reales
- [ ] Mapa gasolineras interactivo
- [ ] Comparador Seseña vs Aranjuez
- [ ] Presupuesto combustible
- [ ] Alertas inteligentes
- [ ] Modo oscuro
- [ ] Responsive (móvil/desktop)

### Funcionalidades Futuras (Post-MVP)
- [ ] Histórico de precios
- [ ] Predicción con ML
- [ ] Notificaciones email
- [ ] Integración telecomunicaciones
- [ ] Integración seguros
- [ ] App móvil nativa

---

## 💡 NOTAS IMPORTANTES

### Problemas Posibles y Soluciones

**Problema**: API OMIE está caída  
**Solución**: Usar fallback con datos estáticos del día anterior

**Problema**: MITMA no tiene datos de Seseña  
**Solución**: Usar CSV local + actualización manual

**Problema**: Mapa es lento en móvil  
**Solución**: Limitar pines a top 10, usar lazy loading

---

## 🎯 MÉTRICAS DE ÉXITO

| Métrica | Objetivo | Semana |
|---------|----------|--------|
| **Tiempo carga** | <2s | 2 |
| **Usuarios testeados** | 5+ | 4 |
| **API uptime** | 99% | 6 |
| **Lighthouse** | >85 | 8 |
| **Modo oscuro** | 100% funcional | 2 |
| **Mapas** | Sin lag | 2 |

---

## 🔗 RECURSOS ÚTILES

- [OMIE API Docs](https://www.omie.es/)
- [MITMA Geoportal](https://geoportal.transportes.gob.es/)
- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Zustand](https://github.com/pmndrs/zustand)
- [Leaflet.js](https://leafletjs.com/reference.html)

---

**¿Empezamos con Semana 1? Escribe: `Sí, comenzar` 🚀**
