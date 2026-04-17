# 🧠 PROMPT OPTIMIZADO PARA ENERGY & FUEL CONTROL CENTER

> **Versión**: 2.0 Mejorada | **Tipo**: Full-Stack Moderno | **Alcance**: MVP + Escalable

---

## 🎯 DESCRIPCIÓN EJECUTIVA

Construir **Energy & Fuel Control Center**: un dashboard web inteligente que **optimiza automáticamente gastos diarios** en:
- ⚡ Electricidad (PVPC España)
- 🔥 Gas (Naturgy TUR)
- ⛽ Gasolina (Repsol + gasolineras baratas)
- 📊 Panel de control unificado
- 💡 Recomendaciones IA personalizadas

**Objetivo**: Responder automáticamente:
1. ¿Cuándo consumo más barato?
2. ¿Dónde reposto más barato?
3. ¿Cuánto me cuesta vivir hoy?
4. ¿Cómo ahorró con decisiones inteligentes?

**Ubicaciones priorizadas**: Seseña (Repsol) + Aranjuez (comparativa general)

---

## 🏗️ STACK TECNOLÓGICO (MANDATORIO)

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Lenguaje**: TypeScript
- **Estilos**: Tailwind CSS
- **Gráficos**: Recharts (barras, líneas, áreas)
- **Mapas**: Leaflet.js (OpenStreetMap) - o Google Maps con API key
- **Estado Global**: Zustand (ligero, sin boilerplate)
- **UI/UX**: Componentes reutilizables, sistema de diseño coherente
- **Temas**: Modo oscuro/claro con persistencia

### Backend
- **Runtime**: Node.js + Next.js API Routes
- **Lenguaje**: TypeScript
- **Validación**: Zod o io-ts
- **Cache**: Redis (opcional, fase 2)
- **Base de datos**: SQLite/PostgreSQL (fase 2, ahora mock)

### DevOps
- **Version Control**: Git + GitHub
- **Deploy**: Vercel (Next.js) + Backend en Railway/Render
- **Testing**: Jest + React Testing Library (fase 2)
- **CI/CD**: GitHub Actions

### Datos
- **APIs Externas**: OMIE/PVPC, MITMA Carburantes, OpenWeatherMap
- **Almacenamiento**: Caché local + base de datos histórica

---

## ⚡ MÓDULO 1: ELECTRICIDAD (PVPC / OMIE)

### 1.1 Fuente de Datos
- **API Real**: [OMIE](https://www.omie.es/) o [PVPC IDAE](https://www.idae.es/)
- **Fallback**: Mock con estructura realista
- **Actualización**: Cada hora automática

### 1.2 Datos a Mostrar

| Métrica | Tipo | Ejemplo |
|---------|------|---------|
| Precio €/kWh por hora | Tabla 24h | 0.048€ - 0.245€ |
| Mejor hora | Hora + precio | 03:00 (0.048€) |
| Peor hora | Hora + precio | 19:00 (0.245€) |
| Precio promedio | Número | 0.128€ |
| Mejor ventana 4h | Rango horario | 02:00 - 06:00 |
| Consumo diario | Configurable (kWh) | 25 kWh/día |
| Coste diario | Calculado | 3.20€/día |
| Coste mensual | Estimado | 96€/mes |

### 1.3 Visualización

**Gráfico Principal**: Línea con área (Recharts)
```
Eje Y: Precio €/kWh (0.00 - 0.30)
Eje X: Horas (00:00 - 23:00)
Colores:
  - Zona verde (barato): ≤ mín + 10%
  - Zona amarilla (medio): promedio ±15%
  - Zona roja (caro): ≥ máx - 15%
```

**Cards Secundarias**:
- Card: "Mejor hora" (verde)
- Card: "Peor hora" (rojo)
- Card: "Promedio" (neutral)
- Card: "Mejor ventana" (destacada)

### 1.4 Recomendaciones IA

```
Ejemplo: "💚 AHORRO: Usa lavadora entre 02:00-06:00
Diferencia: 2,50€/ciclo (15% barato)
Ahorro mensual: ~30€"
```

**Lógica**:
- Si hay valle claro (>20% diferencia): recomendar
- Calcular ahorro basado en consumo estimado
- Mostrar horario específico en español

---

## 🔥 MÓDULO 2: GAS (NATURGY TUR)

### 2.1 Fuente de Datos
- **API Real**: Naturgy/IDAE (si disponible)
- **Fallback**: Tarifa TUR estructurada realista
- **Tipo Tarifa**: T1 - Residencial
- **Actualización**: Diaria a medianoche

### 2.2 Datos a Mostrar

| Métrica | Tipo | Ejemplo |
|---------|------|---------|
| Precio €/kWh | Número | 0.045€ |
| Término fijo diario | Número | 0.35€/día |
| Consumo estimado | Configurable | 8 kWh/día |
| Coste variable diario | Calculado | 0.36€/día |
| Coste fijo diario | Fijo | 0.35€/día |
| Coste total diario | Sumado | 0.71€/día |
| Coste mensual | Proyectado | 21.30€/mes |
| Tendencia | Indicador | ↑ Sube / ↓ Baja / → Estable |
| Alerta de cambio | Booleano | ✅ Sin cambios / ⚠️ Cambio detectado |

### 2.3 Visualización

**Gráfico Circular (Donut)**:
- Segmento azul: Coste variable
- Segmento gris: Coste fijo
- Centro: Total €/día

**Tabla de Desglose**:
```
┌─────────────────────────────┐
│ Concepto        │   Importe │
├─────────────────────────────┤
│ Parte variable  │ 0,36€/día │
│ Parte fija      │ 0,35€/día │
├─────────────────────────────┤
│ TOTAL           │ 0,71€/día │
│ MES (30 días)   │  21,30€   │
└─────────────────────────────┘
```

### 2.4 Indicador de Tendencia
```
Precio: 0.045€/kWh
Tendencia: ↑ SUBE (↑5.2% vs semana anterior)
Estado: 🟡 ALERTA - Máximo del trimestre
```

---

## ⛽ MÓDULO 3: GASOLINA (REPSOL + COMPARADOR)

### 3.1 Fuente de Datos
- **API Real**: [MITMA Geoportal](https://geoportal.transportes.gob.es/)
- **Fallback**: Mock de gasolineras reales
- **Actualización**: Cada 30 minutos
- **Tipo de gasolina**: Gasolina 95 (por defecto)

### 3.2 Ubicaciones Priorizadas

#### A) SESEÑA (Prioridad Repsol)
**Objetivo**: Gasolineras Repsol cercanas

**Datos por estación**:
- Nombre (ej: REPSOL Seseña)
- Precio gasolina 95 (€/L)
- Distancia desde centro (km)
- Teléfono / Dirección
- Horario (24h sí/no)

**Tabla de resultados**:
```
┌────┬──────────────────────┬────────┬──────────┐
│ # │ Gasolinera           │ Precio │ Distancia│
├────┼──────────────────────┼────────┼──────────┤
│🥇 │ REPSOL Centro        │ 1,749€ │ 0,3 km   │
│🥈 │ REPSOL Polígono      │ 1,759€ │ 1,2 km   │
│🥉 │ REPSOL Carretera     │ 1,769€ │ 2,5 km   │
└────┴──────────────────────┴────────┴──────────┘

💡 MEJOR: REPSOL Centro por 1,749€
```

**Recomendación automática**:
> "🥇 Mejor opción Repsol: Centro a 1,749€/L (0,3 km)"

#### B) ARANJUEZ (Mercado Abierto - Todos)
**Objetivo**: Comparativa con todas las marcas

**Marcas incluidas**:
- Repsol
- Cepsa
- BP
- Shell
- Ballenoil
- Carrefour
- E.Leclerc
- Independientes

**Datos**:
- Top 5 más baratas (ordenadas asc)
- Nombre + marca + precio
- Distancia
- Tipo de estación (gasolinera, hipermercado, etc)

**Tabla comparativa**:
```
┌────┬──────────────────────────┬────────┬──────────┐
│ # │ Gasolinera               │ Precio │ Distancia│
├────┼──────────────────────────┼────────┼──────────┤
│🥇 │ E.Leclerc Aranjuez       │ 1,729€ │ 0,5 km   │
│🥈 │ Carrefour Centro         │ 1,739€ │ 1,1 km   │
│🥉 │ BP Polígono              │ 1,749€ │ 2,2 km   │
│4️⃣ │ REPSOL Ronda Sur         │ 1,759€ │ 1,8 km   │
│5️⃣ │ Shell Centro             │ 1,769€ │ 0,9 km   │
└────┴──────────────────────────┴────────┴──────────┘

💡 MEJORA: E.Leclerc es 2 céntimos más barata
```

#### C) COMPARADOR INTELIGENTE (Seseña vs Aranjuez)

**Mostrar lado a lado**:
```
┌───────────────────────────────────────────┐
│ SESEÑA (Repsol)    vs    ARANJUEZ (Todos) │
├───────────────────────────────────────────┤
│ 🔴 REPSOL Centro      🟢 E.Leclerc        │
│    1,749€/L            1,729€/L           │
│    0,3 km              0,5 km             │
│                                           │
│ DIFERENCIA: 2 céntimos/L                 │
│ AHORRO: 8€ por depósito (50L)            │
│ AHORRO MENSUAL: ~64€ (8 depósitos)       │
│                                           │
│ ✅ RECOMENDACIÓN: Aranjuez - E.Leclerc   │
└───────────────────────────────────────────┘
```

#### D) Mapa Interactivo
- **Tecn**: Leaflet.js + OpenStreetMap (o Google Maps)
- **Pines por estación**: color según precio
  - 🟢 Verde: <1,75€
  - 🟡 Amarillo: 1,75€-1,79€
  - 🔴 Rojo: >1,79€
- **Click en pin**: mostrar detalles + navegar (Google Maps/Waze)
- **Filtros**: marcar/desmarcar por ciudad
- **Zoom**: auto-centrado en mejor opción

### 3.3 Control de Tarjeta Combustible

```
┌────────────────────────────────┐
│ 💳 PRESUPUESTO COMBUSTIBLE     │
├────────────────────────────────┤
│ Presupuesto: 100€/mes          │
│ Gasto acumulado: 65€           │
│ Saldo restante: 35€            │
│                                │
│ [=========>        ] 65%       │
│                                │
│ Días restantes: 13 días        │
│ Gasto recomendado: 2,69€/día   │
│ Gasto real promedio: 5,00€/día │
│                                │
│ ⚠️ ALERTA: Ritmo insostenible  │
│    (Ahorrar 2,31€ diarios)     │
└────────────────────────────────┘
```

**Estados**:
- 🟢 ✅ Presupuesto saludable: >70% saldo
- 🟡 ⚠️ Atención: 30-70% saldo
- 🔴 🚨 CRÍTICO: <30% saldo

---

## 📊 MÓDULO 4: DASHBOARD CENTRAL (Main View)

### 4.1 Layout Grid Responsivo
```
[Desktop - 1400px]
┌────────────────────────────────────────────────────────┐
│  HEADER + STATUS BAR + CONTROLES                       │
├──────────────────────┬──────────────────────────────────┤
│ ⚡ ELECTRICIDAD     │ 🔥 GAS          │ ⛽ GASOLINA    │
│ (Card principal)    │ (Card medio)    │ (Card medio)   │
├──────────────────────┼──────────────────────────────────┤
│ 💰 RESUMEN MENSUAL (Tarjeta ancha - Full width)        │
│ Electricidad: 750€ | Gas: 240€ | Gasolina: 100€       │
│ TOTAL: 1.090€                                          │
├──────────────────────┴──────────────────────────────────┤
│ 💡 RECOMENDACIONES (Carousel o lista)                  │
├──────────────────────────────────────────────────────────┤
│ 📍 COMPARADOR SESEÑA vs ARANJUEZ (Tabla + Mapa)        │
├──────────────────────────────────────────────────────────┤
│ 📋 DETALLES TÉCNICOS (API status, último sync, etc)   │
└──────────────────────────────────────────────────────────┘

[Móvil - Stack vertical]
```

### 4.2 Cards Principales (8 totales)

1. **Card: Mejor Hora Electricidad** 🟢
   - Hora + precio
   - Botón: "Ver gráfico 24h"

2. **Card: Peor Hora Electricidad** 🔴
   - Hora + precio
   - Aviso: "Evita este horario"

3. **Card: Presupuesto Gas** 🟡
   - Porcentaje visual
   - Coste mes estimado

4. **Card: Mejor Gasolinera** 🥇
   - Nombre + precio
   - Distancia
   - "Ver en mapa"

5. **Card: Mejor Repsol** 🏆
   - Solo Seseña
   - Comparativa vs mejor general

6. **Card: Presupuesto Gasolina** 💳
   - Barra de progreso
   - Estado (ok/warn/critical)

7. **Card: Ahorro Mensual Potencial** 💚
   - Cantidad en €
   - % de reducción posible
   - Acciones recomendadas

8. **Card: Alerts & Recomendaciones** 📢
   - Lista de alertas activas
   - Badge rojo/amarillo/verde

### 4.3 Resumen Financiero Unificado (Tarjeta Principal)

```
┌─────────────────────────────────────────────────┐
│ 💰 RESUMEN MENSUAL ESTIMADO                     │
├─────────────────────────────────────────────────┤
│ ⚡ Electricidad      750€  [25 kWh/día]         │
│ 🔥 Gas              240€  [8 kWh/día]          │
│ ⛽ Gasolina          100€  [100€ presupuesto]   │
│ ─────────────────────────                       │
│ 💰 TOTAL          1.090€/mes                    │
│                                                 │
│ Ahorro potencial: +120€/mes (optimizado)        │
│ Tu consumo optimizado: 970€/mes                 │
│ % Ahorro: 11%                                   │
└─────────────────────────────────────────────────┘
```

---

## 🧠 MOTOR DE RECOMENDACIONES (IA)

### Lógica de Recomendaciones

**Input**: Datos OMIE + Tarifa TUR + Precios gasolineras + Consumo

**Output**: Array de objetos:
```typescript
interface Recomendacion {
  id: string;
  tipo: 'electricidad' | 'gas' | 'gasolina' | 'general';
  icono: string;
  titulo: string;
  descripcion: string;
  accion: string;
  ahorro_estimado: number;
  urgencia: 'baja' | 'media' | 'alta';
  timestamp: Date;
}
```

### Ejemplos

#### Recomendación 1: Horario Electricidad
```json
{
  "tipo": "electricidad",
  "icono": "⚡",
  "titulo": "Ahorro en horas valle",
  "descripcion": "Usa lavadora, lavavajillas y carga móvil entre 02:00-06:00",
  "accion": "Establecer alarmas para 02:00",
  "ahorro_estimado": 25.50,
  "urgencia": "media"
}
```

#### Recomendación 2: Gasolinera Barata
```json
{
  "tipo": "gasolina",
  "icono": "⛽",
  "titulo": "Gasolinera más barata detectada",
  "descripcion": "E.Leclerc Aranjuez a 1,729€/L (2¢ menos que Repsol)",
  "accion": "Ver en mapa",
  "ahorro_estimado": 64,
  "urgencia": "alta"
}
```

#### Recomendación 3: Presupuesto Crítico
```json
{
  "tipo": "gasolina",
  "icono": "🚨",
  "titulo": "Presupuesto de gasolina crítico",
  "descripcion": "Te quedan 35€ para 13 días. Gasto recomendado: 2,69€/día",
  "accion": "Buscar ruta eficiente",
  "ahorro_estimado": 0,
  "urgencia": "alta"
}
```

### Algoritmo de Generación

```python
def generar_recomendaciones(electricidad, gas, gasolina, consumo_usuario):
    recomendaciones = []
    
    # 1. Electricidad: si hay valle claro (>20% diferencia)
    if (max_price - min_price) / promedio > 0.20:
        recomendaciones.append({
            titulo: "Ahorro en horas valle",
            ahorro: consumo_kWh * (max_price - min_price_en_valle)
        })
    
    # 2. Gas: si hay tendencia al alza
    if tendencia == 'alza' and precio > precio_promedio_3_meses:
        recomendaciones.append({
            titulo: "Gas en máximos",
            accion: "Considerar otros proveedores"
        })
    
    # 3. Gasolina: si mejor opción es 2%+ más barata
    ahorro_posible = (mejor_repsol - mejor_general) * 50 * 8  # 50L * 8 depósitos/mes
    if ahorro_posible > consumo_presupuesto * 0.06:  # >6% presupuesto
        recomendaciones.append({
            titulo: "Mejor gasolinera detectada",
            ahorro: ahorro_posible
        })
    
    return recomendaciones
```

---

## 📱 UX / UI

### Temas
- **Modo Oscuro**: Por defecto (Tesla dashboard style)
- **Modo Claro**: Disponible, cambio con toggle
- **Persistencia**: localStorage

### Paleta de Colores
- 🟢 **Verde (Ahorro)**: #10b981
- 🟡 **Amarillo (Alerta)**: #f59e0b
- 🔴 **Rojo (Crítico)**: #ef4444
- ⚪ **Neutro**: #6b7280
- 🔵 **Primario**: #667eea
- ⚫ **Dark**: #1f2937 (fondo modo oscuro)

### Componentes Reutilizables

```typescript
// Card genérico
<Card icon={icon} title={title} value={value} unit={unit} status={status} />

// Gráfico dinámico
<ChartContainer data={data} type="line" height={300} />

// Tabla filtrable
<DataTable columns={columns} data={data} sortable={true} />

// Map con pines
<MapComponent pins={pins} zoom={13} center={center} />

// Indicador de estado
<StatusBadge status="warning" text="Alerta activa" />

// Toggle tema
<ThemeToggle currentTheme={theme} onChange={setTheme} />

// Barra de progreso
<ProgressBar value={65} max={100} color="warning" />
```

---

## 🔌 ARQUITECTURA DE DATOS

### Estructura de Carpetas

```
energy-fuel-control/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── page.tsx (main dashboard)
│   │   │   │   └── layout.tsx
│   │   │   ├── (modules)/
│   │   │   │   ├── electricity/
│   │   │   │   ├── gas/
│   │   │   │   ├── fuel/
│   │   │   │   └── comparator/
│   │   │   ├── api/
│   │   │   │   ├── electricity.ts
│   │   │   │   ├── gas.ts
│   │   │   │   ├── fuel.ts
│   │   │   │   └── recommendations.ts
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── charts/
│   │   │   │   ├── LineChart.tsx
│   │   │   │   ├── DonutChart.tsx
│   │   │   │   └── BarChart.tsx
│   │   │   ├── cards/
│   │   │   │   ├── ElectricityCard.tsx
│   │   │   │   ├── GasCard.tsx
│   │   │   │   ├── FuelCard.tsx
│   │   │   │   └── SummaryCard.tsx
│   │   │   ├── maps/
│   │   │   │   └── GasolineraMap.tsx
│   │   │   ├── shared/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── ThemeToggle.tsx
│   │   │   │   └── LoadingSpinner.tsx
│   │   │   └── layout/
│   │   │       ├── SidebarNav.tsx
│   │   │       └── ResponsiveGrid.tsx
│   │   ├── store/
│   │   │   ├── useEnergyStore.ts (Zustand)
│   │   │   └── useSettingsStore.ts
│   │   ├── services/
│   │   │   ├── api/
│   │   │   │   ├── electricityApi.ts
│   │   │   │   ├── gasApi.ts
│   │   │   │   ├── fuelApi.ts
│   │   │   │   └── recommendationsApi.ts
│   │   │   └── formatters.ts
│   │   ├── types/
│   │   │   ├── electricity.ts
│   │   │   ├── gas.ts
│   │   │   ├── fuel.ts
│   │   │   └── common.ts
│   │   ├── styles/
│   │   │   └── globals.css (Tailwind)
│   │   └── hooks/
│   │       ├── useElectricity.ts
│   │       ├── useGas.ts
│   │       ├── useFuel.ts
│   │       └── useTheme.ts
│   ├── public/
│   │   ├── icons/
│   │   └── images/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── .env.local
│
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── electricity.ts
│   │   │   │   ├── gas.ts
│   │   │   │   ├── fuel.ts
│   │   │   │   └── recommendations.ts
│   │   │   └── middleware/
│   │   │       └── errorHandler.ts
│   │   ├── services/
│   │   │   ├── electricityService.ts
│   │   │   ├── gasService.ts
│   │   │   ├── fuelService.ts
│   │   │   └── recommendationsService.ts
│   │   ├── data/
│   │   │   ├── omieClient.ts
│   │   │   ├── mitmaClient.ts
│   │   │   └── naturgyClient.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── utils/
│   │   │   └── cache.ts
│   │   └── index.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── .env
│
├── docs/
│   ├── API.md
│   ├── SETUP.md
│   └── DEPLOYMENT.md
│
├── README.md
├── .gitignore
└── package.json (monorepo)
```

### Tipos TypeScript Clave

```typescript
// Electricidad
interface Hora {
  hora: string;
  precio: number;
  estado: 'barata' | 'media' | 'cara';
}

interface Electricidad {
  horas: Hora[];
  precio_minimo: number;
  precio_maximo: number;
  precio_promedio: number;
  mejor_ventana: { inicio: string; fin: string; promedio: number };
  coste_diario_estimado: number;
  coste_mensual_estimado: number;
}

// Gas
interface Gas {
  precio_kwh: number;
  termino_fijo_diario: number;
  consumo_estimado_diario: number;
  coste_variable_diario: number;
  coste_fijo_diario: number;
  coste_diario_total: number;
  coste_mensual_total: number;
  tendencia: 'sube' | 'baja' | 'estable';
  tarifa_type: 'T1 - Residencial' | 'T2' | 'T3';
}

// Gasolina
interface Gasolinera {
  id: string;
  nombre: string;
  marca: 'REPSOL' | 'CEPSA' | 'BP' | 'SHELL' | 'BALLENOIL' | 'CARREFOUR' | 'E.LECLERC' | 'INDEPENDIENTE';
  precio: number;
  localidad: 'Seseña' | 'Aranjuez';
  distancia: number;
  coordenadas: { lat: number; lng: number };
  horario: string;
  telefono?: string;
}

interface Gasolina {
  mejor: Gasolinera;
  peor: Gasolinera;
  promedio: number;
  total: number;
  top3: Gasolinera[];
  presupuesto: {
    mensual: number;
    gasto_acumulado: number;
    saldo_restante: number;
    dias_restantes: number;
    alerta: 'ok' | 'warning' | 'critical';
  };
}

// Recomendación
interface Recomendacion {
  id: string;
  tipo: 'electricidad' | 'gas' | 'gasolina' | 'general';
  icono: string;
  titulo: string;
  descripcion: string;
  accion: string;
  ahorro_estimado: number;
  urgencia: 'baja' | 'media' | 'alta';
  timestamp: Date;
}
```

---

## 🔗 APIS EXTERNAS

### 1. OMIE / PVPC (Electricidad)
```
GET https://api.esios.ree.es/archives/70
Response: Precios horarios €/kWh últimas 24h
```

### 2. MITMA Geoportal (Gasolina)
```
GET https://geoportal.transportes.gob.es/api/gasolineras
Params: localidad, tipo_gasolina, orden
Response: JSON con lista de gasolineras
```

### 3. Naturgy / IDAE (Gas)
```
GET https://www.naturgy.es/ (web scraping o API privada)
Response: Tarifa TUR actual
```

### 4. OpenWeatherMap (Bonus)
```
GET https://api.openweathermap.org/data/2.5/weather
Params: Seseña/Aranjuez coords
Response: Clima (para predicción consumo)
```

---

## ⚠️ REQUISITOS NO FUNCIONALES

### Performance
- [ ] First Contentful Paint (FCP) < 1.5s
- [ ] Largest Contentful Paint (LCP) < 2.5s
- [ ] Time to Interactive (TTI) < 3.5s
- [ ] Lighthouse Score > 85

### Escalabilidad
- [ ] Código modular y reutilizable
- [ ] Servicios separados por dominio
- [ ] Preparado para agregar Telecomunicaciones, Seguros, etc.
- [ ] API RESTful versioning (/v1/, /v2/)

### Mantenibilidad
- [ ] TypeScript en 100% del código
- [ ] Tests unitarios + e2e (fase 2)
- [ ] Documentación OpenAPI (Swagger)
- [ ] CI/CD con GitHub Actions

### Seguridad
- [ ] Variables de entorno para API keys
- [ ] HTTPS obligatorio en producción
- [ ] Rate limiting en APIs
- [ ] Validación con Zod en todas las entradas

---

## 📋 CHECKLIST DE ENTREGA

### Fase 1 (MVP - Semanas 1-2)
- [ ] Setup Next.js + TypeScript + Tailwind
- [ ] Estructura carpetas según arquitectura
- [ ] Componentes base (Card, Chart, Map, etc)
- [ ] Mock de datos OMIE/TUR/Gasolineras
- [ ] Dashboard principal funcional
- [ ] Tema oscuro/claro con toggle
- [ ] Responsive design (móvil/tablet/desktop)

### Fase 2 (APIs Reales - Semanas 3-4)
- [ ] Conectar API OMIE electricidad
- [ ] Conectar API MITMA gasolineras
- [ ] Conectar tarifa TUR gas
- [ ] Implementar caché local
- [ ] Refresco automático cada 30min

### Fase 3 (Inteligencia - Semanas 5-6)
- [ ] Sistema de recomendaciones
- [ ] Comparador Seseña vs Aranjuez
- [ ] Alertas personalizadas
- [ ] Historial de precios
- [ ] Predicción básica

### Fase 4 (Optimización - Semanas 7-8)
- [ ] Tests unitarios (Jest)
- [ ] Tests e2e (Playwright/Cypress)
- [ ] Optimización de performance
- [ ] SEO básico
- [ ] Deploy en Vercel

---

## 🎯 ÉXITO

El proyecto es exitoso cuando:

✅ Usuario abre dashboard y ve en **<2s**:
- ¿Cuál es la mejor hora para consumir electricidad hoy?
- ¿Dónde debo repostar gasolina más barata?
- ¿Cuánto me cuesta vivir hoy?
- ¿Cuánto puedo ahorrar si sigo recomendaciones?

✅ Sistema recomienda acciones automáticas

✅ Interfaz es intuitiva, rápida y hermosa

✅ Escalable a más servicios (seguros, telecomunicaciones, etc)

---

**¿Listo para comenzar? 🚀**
