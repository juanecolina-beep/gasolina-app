# 📌 HOJA DE REFERENCIA RÁPIDA

**Tu proyecto**: Energy & Fuel Control Center  
**Stack actual**: Python + HTML/CSS/JS vanilla  
**Stack mejorado**: Next.js 14 + TypeScript + Tailwind  
**Duración**: 8 semanas | **Usuarios finales**: Hogares España

---

## 🎯 LOS 3 MÓDULOS PRINCIPALES

### ⚡ ELECTRICIDAD
**Qué**: Precios horarios OMIE (€/kWh cada hora)  
**Fuente**: API OMIE/PVPC (datos reales)  
**Cálculos**: Min, máx, promedio, mejor ventana 4h  
**UI**: Gráfico línea + 3 cards + recomendación  
**Ubicación en dashboard**: Card superior izquierda

### 🔥 GAS
**Qué**: Tarifa TUR Naturgy (€/kWh + término fijo)  
**Fuente**: Tarifa TUR (actualización diaria)  
**Cálculos**: Coste diario, mensual, tendencia  
**UI**: Donut chart + tabla desglose + indicador tendencia  
**Ubicación en dashboard**: Card superior central

### ⛽ GASOLINA
**Qué**: Precios 95 Seseña (Repsol) vs Aranjuez (todos)  
**Fuente**: MITMA Geoportal  
**Cálculos**: Mejor opción, comparador, ahorro mensual  
**UI**: Mapa + tabla comparador + presupuesto tracker  
**Ubicación en dashboard**: Card superior derecha + mapa grande

---

## 📊 ESTRUCTURA DE DATOS JSON

```json
{
  "timestamp": "2026-04-17T14:30:00",
  "status": "ok",
  
  "electricidad": {
    "horas": [
      {"hora": "00:00", "precio": 0.065, "estado": "🟢 Barata"},
      {"hora": "01:00", "precio": 0.058, "estado": "🟢 Barata"},
      ...
    ],
    "precio_minimo": 0.048,
    "precio_maximo": 0.245,
    "precio_promedio": 0.128,
    "mejor_ventana": {
      "inicio": "02:00",
      "fin": "06:00",
      "promedio": 0.055
    },
    "coste_diario_estimado": 3.20,
    "coste_mensual_estimado": 96.00
  },
  
  "gas": {
    "precio_kwh": 0.045,
    "termino_fijo_diario": 0.35,
    "consumo_estimado_diario": 8,
    "coste_variable_diario": 0.36,
    "coste_fijo_diario": 0.35,
    "coste_diario_total": 0.71,
    "coste_mensual_total": 21.30,
    "tendencia": "estable",
    "tarifa_type": "T1 - Residencial"
  },
  
  "gasolina": {
    "mejor": {
      "estacion": "E.Leclerc Aranjuez",
      "precio": 1.729,
      "localidad": "Aranjuez",
      "distancia": 0.5
    },
    "peor": {
      "estacion": "Shell Aranjuez",
      "precio": 1.799,
      "localidad": "Aranjuez"
    },
    "promedio": 1.759,
    "total": 24,
    "top3": [...],
    "presupuesto": {
      "mensual": 100,
      "gasto_acumulado": 65,
      "saldo_restante": 35,
      "dias_restantes": 13,
      "alerta": "warning"
    }
  },
  
  "resumen_financiero": {
    "electricidad": 96.00,
    "gas": 21.30,
    "gasolina": 100.00,
    "total_mensual": 217.30,
    "moneda": "EUR"
  },
  
  "recomendaciones": [
    {
      "tipo": "electricidad",
      "titulo": "Ahorro en horas valle",
      "descripcion": "Usa lavadora entre 02:00-06:00",
      "ahorro_estimado": 25.50,
      "urgencia": "media"
    },
    ...
  ]
}
```

---

## 🔴 3 OPCIONES ESTRATÉGICAS

| Aspecto | Opción A (Mejora Rápida) | Opción B (Migración) | Opción C (Reescritura) |
|---------|------------------------|----------------------|----------------------|
| **Tiempo** | 2 sem | 4 sem | 8 sem |
| **Riesgo** | 🟢 Bajo | 🟡 Medio | 🔴 Alto |
| **APIs reales** | ✅ Sí | ✅ Sí | ✅ Sí |
| **Mapas** | ✅ Sí | ✅ Sí | ✅ Sí |
| **Stack moderno** | ❌ No | ✅ Sí | ✅ Sí |
| **Escalabilidad** | ⚠️ Limitada | ✅ Buena | ✅ Excelente |
| **Costo** | 💰 Bajo | 💰💰 Medio | 💰💰💰 Alto |

**👉 RECOMENDACIÓN**: Opción A ahora + Opción B en 2-3 semanas

---

## ⚡ LOS 8 CAMBIOS MÁS CRÍTICOS

### 1️⃣ Conectar API OMIE Real
```python
# main.py - Reemplazar mock
import requests

precios = requests.get('https://api.esios.ree.es/archives/70').json()
# Extraer valores reales
```

### 2️⃣ Integrar Leaflet.js
```html
<!-- docs/index.html -->
<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.min.js"></script>
<div id="map" style="height: 400px;"></div>
```

### 3️⃣ Selector Ciudad
```html
<select id="ciudad-selector">
  <option value="seseña">🔴 Seseña (Repsol)</option>
  <option value="aranjuez">🟦 Aranjuez (Todos)</option>
</select>
```

### 4️⃣ Modo Oscuro Toggle
```javascript
// Toggle tema con localStorage
document.getElementById('theme-toggle').onclick = () => {
  document.body.style.filter = 
    document.body.style.filter === 'invert(1)' ? 'none' : 'invert(1)';
};
```

### 5️⃣ Comparador Inteligente
```javascript
// Mostrar lado a lado
diferencia = mejorSeseña.precio - mejorAranjuez.precio;
ahorroMes = diferencia * 50 * 8;
```

### 6️⃣ Sistema de Alertas
```javascript
function mostrarAlerta(tipo, titulo, mensaje) {
  const alert = document.createElement('div');
  alert.style.background = tipo === 'warning' ? '#f59e0b' : '#10b981';
  alert.innerHTML = `<strong>${titulo}:</strong> ${mensaje}`;
  document.body.appendChild(alert);
  setTimeout(() => alert.remove(), 4000);
}
```

### 7️⃣ Refactorizar Python
```
modules/
  ├── electricity.py
  ├── gas.py
  ├── fuel.py
  └── recommendations.py
```

### 8️⃣ Setup Next.js (para semana 5)
```bash
npx create-next-app@latest --typescript --tailwind --app
```

---

## 📅 SEMANA POR SEMANA

```
SEMANA 1-2 (7-10 días)
  ├─ Día 1-2: API OMIE real
  ├─ Día 2-3: Selector ciudades
  ├─ Día 3-4: Mapa Leaflet
  ├─ Día 4-5: Modo oscuro
  ├─ Día 5-6: Comparador
  ├─ Día 6-7: Alertas
  ├─ Día 7-8: Modular Python
  └─ Día 8: Testing

SEMANA 3-4 (7-10 días)
  ├─ API MITMA geolocalización real
  ├─ Testing con usuarios reales (5+)
  ├─ Ajustes basados en feedback
  └─ Documentar insights

SEMANA 5-6 (8-10 días)
  ├─ Setup Next.js + TypeScript + Tailwind
  ├─ Migrar componentes principales
  ├─ Implementar Zustand store
  └─ Conectar APIs backend

SEMANA 7-8 (8-10 días)
  ├─ Frontend moderno completo
  ├─ Deploy Vercel
  ├─ Testing Lighthouse >85
  └─ 🚀 LANZAMIENTO V2
```

---

## 🎨 PALETA DE COLORES

- 🟢 **Verde (Ahorro)**: `#10b981` - Bien, ahorrar
- 🟡 **Amarillo (Alerta)**: `#f59e0b` - Atención, revisar
- 🔴 **Rojo (Crítico)**: `#ef4444` - Problema, actuar YA
- ⚫ **Oscuro**: `#1f2937` - Fondo modo noche
- ⚪ **Claro**: `#f9fafb` - Fondo modo día

---

## 🗺️ ARCHIVOS A MODIFICAR (Semana 1-2)

| Archivo | Cambio | Prioridad |
|---------|--------|-----------|
| `main.py` | Conectar API OMIE | 🔴 Crítico |
| `docs/index.html` | Agregar mapa + selector | 🔴 Crítico |
| `docs/js/script.js` | Modo oscuro + alertas | 🟡 Alta |
| `precios_gasolina.csv` | Geolocalización real | 🟡 Alta |
| (nuevo) `modules/*.py` | Refactorizar | 🟢 Media |

---

## 💻 COMANDOS ÚTILES

```bash
# Generar datos actualizados
python main.py

# Ver datos en JSON
cat docs/datos.json | python -m json.tool

# Abrir dashboard en navegador
python -m http.server 8000 --directory docs

# Setup Next.js (Semana 5)
npx create-next-app@latest --typescript --tailwind --app

# Deploy a Vercel (Semana 8)
vercel deploy

# Build para producción
npm run build && npm start
```

---

## ✅ CHECKLIST RÁPIDO (PRINT & STICK)

### Semana 1-2
- [ ] API OMIE conectada
- [ ] Selector ciudades funciona
- [ ] Mapa muestra gasolineras
- [ ] Modo oscuro toggle funciona
- [ ] Tabla comparador visible
- [ ] Alertas salen en pantalla
- [ ] Python modularizado
- [ ] Sin errores en consola

### Semana 3-4
- [ ] API MITMA activa
- [ ] 5+ usuarios testeados
- [ ] Feedback documentado
- [ ] Ajustes aplicados

### Semana 5-6
- [ ] Proyecto Next.js creado
- [ ] Estructura lista
- [ ] Store Zustand funciona
- [ ] Primeros componentes migrados

### Semana 7-8
- [ ] Frontend 100% moderno
- [ ] Deploy en Vercel
- [ ] Lighthouse >85
- [ ] 🎉 GO LIVE

---

## 🔗 LINKS RÁPIDOS

**APIs**
- [OMIE Datos](https://www.omie.es/)
- [MITMA Carburantes](https://geoportal.transportes.gob.es/)
- [Tarifa TUR](https://www.naturgy.es/)

**Código**
- [Next.js App Router](https://nextjs.org/docs/app)
- [Tailwind CSS](https://tailwindcss.com/)
- [Zustand State](https://github.com/pmndrs/zustand)
- [Recharts Gráficos](https://recharts.org/)
- [Leaflet.js Mapas](https://leafletjs.com/)

**Deploy**
- [Vercel Deploy](https://vercel.com/docs)
- [GitHub Actions CI/CD](https://github.com/features/actions)

---

## 🎯 DEFINICIÓN DE ÉXITO

✅ Usuario abre dashboard y en **<2 segundos** ve:
1. "¿Cuál es la mejor hora para lavar ropa hoy?"
2. "¿Dónde reposto más barato?"
3. "¿Cuánto me cuesta vivir hoy?"
4. "¿Cuánto ahorro si sigo recomendaciones?"

✅ Interfaz es hermosa, intuitiva y rápida (Lighthouse >85)

✅ Código es modular y escalable (fácil agregar más servicios)

✅ Usuarios están contentos y lo usan regularmente

---

## 📞 SOPORTE RÁPIDO

**Q: ¿Por dónde empiezo?**  
A: Semana 1 - Opción A (2 semanas)

**Q: ¿Cuándo veo resultados?**  
A: Semana 2 - Dashboard mejorado con mapas

**Q: ¿Es obligatorio Next.js?**  
A: No, pero recomendado en semana 5+

**Q: ¿Necesito dinero para las APIs?**  
A: No, todas son gratuitas (OMIE, MITMA, etc)

**Q: ¿Qué si una API cae?**  
A: Sistema fallback automático a datos estáticos

---

**🚀 ¿LISTO PARA EMPEZAR? Escribe: Comenzar con Semana 1**
