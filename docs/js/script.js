// ===== GESTIÓN DE TEMA OSCURO =====
function initTemaOscuro() {
    const html = document.documentElement;
    const toggle = document.getElementById('theme-toggle');
    const isDark = localStorage.getItem('theme') === 'dark';
    
    if (isDark) html.classList.add('dark-mode');
    
    toggle.onclick = () => {
        const newDark = !html.classList.toggle('dark-mode');
        localStorage.setItem('theme', newDark ? 'dark' : 'light');
        if (window.mapInstance) mapInstance.invalidateSize();
    };
}

// ===== GESTIÓN DE SELECTOR DE CIUDADES =====
function initSelectorCiudad() {
    const selector = document.getElementById('ciudad-selector');
    const saved = localStorage.getItem('ciudad') || 'todas';
    selector.value = saved;
    selector.onchange = async () => {
        localStorage.setItem('ciudad', selector.value);
        await cargarDatos();
    };
}

// ===== SISTEMA DE ALERTAS TOAST =====
function mostrarAlerta(tipo, titulo, mensaje) {
    const container = document.getElementById('alerts-container');
    const alert = document.createElement('div');
    alert.className = `alert-toast ${tipo}`;
    alert.innerHTML = `<div class="alert-toast-title">${titulo}</div><div class="alert-toast-message">${mensaje}</div>`;
    container.appendChild(alert);
    
    setTimeout(() => {
        alert.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => alert.remove(), 300);
    }, 4000);
}

// ===== UTILIDADES DE FORMATO =====
function formatPrice(price) {
    return price.toFixed(3) + '€';
}

function formatMoney(money) {
    return money.toFixed(2) + '€';
}

function formatarFecha(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('es-ES');
}

// ===== PROCESADORES DE DATOS =====
function procesarElectricidad(data) {
    if (!data.electricidad) return;
    const elec = data.electricidad;
    
    document.getElementById('elec-mejor-hora').textContent = elec.mejor_ventana.inicio;
    document.getElementById('elec-promedio').textContent = formatPrice(elec.precio_promedio);
    document.getElementById('elec-coste').textContent = formatMoney(elec.coste_mensual_estimado);
    document.getElementById('fin-electricity').textContent = formatMoney(elec.coste_mensual_estimado);
    
    mostrarAlerta('success', '⚡ Electricidad', `Mejor hora: ${elec.mejor_ventana.inicio}`);
}

function procesarGas(data) {
    if (!data.gas) return;
    const gas = data.gas;
    
    document.getElementById('gas-precio').textContent = formatPrice(gas.precio_kwh);
    document.getElementById('gas-tendencia').textContent = gas.tendencia.toUpperCase();
    document.getElementById('gas-coste').textContent = formatMoney(gas.coste_mensual_total);
    document.getElementById('fin-gas').textContent = formatMoney(gas.coste_mensual_total);
    
    mostrarAlerta('warning', '🔥 Gas', gas.alerta);
}

function procesarGasolina(data) {
    if (!data.gasolina) return;
    const gasolina = data.gasolina;
    
    document.getElementById('gas-mejor').textContent = formatPrice(gasolina.mejor.precio);
    document.getElementById('gas-estacion').textContent = gasolina.mejor.estacion;
    document.getElementById('gas-presupuesto').textContent = formatMoney(gasolina.presupuesto.total);
    document.getElementById('fin-fuel').textContent = formatMoney(gasolina.presupuesto.total);
}

function procesarComparador(data) {
    if (!data.comparador) return;
    const comp = data.comparador;
    
    document.getElementById('comp-seseña-nombre').textContent = comp.seseña.nombre;
    document.getElementById('comp-seseña-precio').textContent = formatPrice(comp.seseña.precio);
    document.getElementById('comp-aranjuez-nombre').textContent = comp.aranjuez.nombre;
    document.getElementById('comp-aranjuez-precio').textContent = formatPrice(comp.aranjuez.precio);
    document.getElementById('comp-diferencia').textContent = formatPrice(Math.abs(comp.diferencia_precio));
    document.getElementById('comp-ahorro').textContent = formatMoney(comp.ahorro_mensual_estimado);
    document.getElementById('comp-recomendacion').textContent = comp.recomendacion;
    
    if (comp.ahorro_mensual_estimado > 20) {
        mostrarAlerta('success', '⚖️ Comparador', `Ahorro: ${formatMoney(comp.ahorro_mensual_estimado)}/mes`);
    }
}

function procesarRecomendaciones(data) {
    if (!data.recomendaciones) return;
    const list = document.getElementById('recomendaciones-list');
    list.innerHTML = '';
    
    data.recomendaciones.forEach(rec => {
        const div = document.createElement('div');
        div.className = 'recommendation-card';
        div.innerHTML = `
            <div class="rec-icon">${rec.tipo === 'Electricidad' ? '⚡' : rec.tipo === 'Gas' ? '🔥' : rec.tipo === 'Gasolina' ? '⛽' : '💡'}</div>
            <div class="rec-title">${rec.titulo}</div>
            <div class="rec-detail">${rec.descripcion}</div>
            <div class="rec-saving">Ahorro: ${formatMoney(rec.ahorro_estimado)}</div>
        `;
        list.appendChild(div);
        
        if (rec.urgencia === 'alta') {
            mostrarAlerta('danger', `⚠️ ${rec.tipo}`, rec.titulo);
        }
    });
}

// ===== MAPA CON LEAFLET =====
let mapInstance = null;

function crearMapa(gasolineras) {
    if (mapInstance) mapInstance.remove();
    
    const container = document.getElementById('map');
    mapInstance = L.map(container).setView([40.08, -3.57], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapInstance);
    
    const colores = {green: '#10b981', yellow: '#f59e0b', red: '#ef4444'};
    
    gasolineras.forEach(g => {
        const color = g.precio < 1.75 ? colores.green : (g.precio < 1.79 ? colores.yellow : colores.red);
        const icon = L.divIcon({
            html: `<div style="background:${color}; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:12px;">⛽</div>`,
            iconSize: [30, 30]
        });
        L.marker([g.lat, g.lon], {icon}).bindPopup(`<b>${g.nombre}</b><br>${formatPrice(g.precio)}<br>${g.localidad}`).addTo(mapInstance);
    });
    
    mostrarAlerta('success', '🗺️ Mapa', 'Estaciones cargadas');
}

// ===== CARGAR Y PROCESAR DATOS =====
async function cargarDatos() {
    try {
        const response = await fetch('datos.json');
        const data = await response.json();
        
        // Procesar todos los datos
        procesarElectricidad(data);
        procesarGas(data);
        procesarGasolina(data);
        procesarComparador(data);
        procesarRecomendaciones(data);
        
        // Crear mapa
        if (data.gasolina && data.gasolina.estaciones) {
            crearMapa(data.gasolina.estaciones);
        }
        
        // Mostrar timestamp
        document.getElementById('timestamp').textContent = formatarFecha(data.timestamp);
        
        // Total mensual
        const total = (data.electricidad?.coste_mensual_estimado || 0) + 
                     (data.gas?.coste_mensual_total || 0) + 
                     (data.gasolina?.presupuesto?.total || 0);
        document.getElementById('fin-total').textContent = formatMoney(total);
        
    } catch (error) {
        console.error('Error cargando datos:', error);
        mostrarAlerta('danger', '❌ Error', 'No se pudieron cargar los datos');
    }
}

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', async () => {
    initTemaOscuro();
    initSelectorCiudad();
    await cargarDatos();
    
    // Recargar datos cada 30 minutos
    setInterval(cargarDatos, 30 * 60 * 1000);
});

function mostrarAlerta(tipo, titulo, mensaje) {
    const container = document.getElementById('alerts-container');
    const toast = document.createElement('div');
    
    toast.className = `alert-toast ${ tipo }`;
    toast.innerHTML = `<strong>${ titulo }:</strong> ${ mensaje }`;
    
    container.appendChild(toast);
    
    // Animar salida después de 4 segundos
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ==========================================
// GESTOR DE TEMA OSCURO
// ==========================================

function initTemaOscuro() {
    const html = document.documentElement;
    const isDark = localStorage.getItem('theme') === 'dark';
    
    if (isDark) {
        html.classList.add('dark-mode');
    }
    
    document.getElementById('theme-toggle').addEventListener('click', () => {
        html.classList.toggle('dark-mode');
        const newDark = html.classList.contains('dark-mode');
        localStorage.setItem('theme', newDark ? 'dark' : 'light');
        
        // Redibujar mapa si existe
        if (mapInstance) {
            setTimeout(() => mapInstance.invalidateSize(), 100);
        }
    });
}

// ==========================================
// GESTOR DE CIUDAD
// ==========================================

function initSelectorCiudad() {
    const selector = document.getElementById('ciudad-selector');
    const ciudadGuardada = localStorage.getItem('ciudad-seleccionada') || 'seseña';
    
    selector.value = ciudadGuardada;
    selector.addEventListener('change', (e) => {
        localStorage.setItem('ciudad-seleccionada', e.target.value);
        cargarDatos(); // Recargar datos
    });
}

// ==========================================
// PROCESAMIENTO DE ELECTRICIDAD
// ==========================================

function procesarElectricidad(data) {
    if (!data) return;

    // Precios
    setElement('elec-cheap', formatPrice(data.precio_minimo));
    setElement('elec-avg', formatPrice(data.precio_promedio));
    setElement('elec-expensive', formatPrice(data.precio_maximo));

    // Mejor ventana
    setElement('elec-best-hours', `${ data.mejor_ventana.inicio } - ${ data.mejor_ventana.fin }`);
    setElement('elec-best-price', formatPrice(data.mejor_ventana.promedio));

    // Costes
    setElement('elec-daily-cost', formatMoney(data.coste_diario_estimado));
    setElement('elec-monthly-cost', formatMoney(data.coste_mensual_estimado));

    // Tabla horaria
    const hourlyTable = document.getElementById('hourly-prices');
    hourlyTable.innerHTML = data.horas.map(h => `
        <div class="hour-cell ${ h.categoria }" title="${ h.hora }: ${ formatPrice(h.precio) }">
            ${ h.hora.split(':')[0] }h
        </div>
    `).join('');

    // Gráfico
    crearGraficoElectricidad(data.horas);
}

function crearGraficoElectricidad(horas) {
    const canvas = document.getElementById('hourly-chart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    
    // Destruir gráfico anterior si existe
    if (window.hourlyChartInstance) {
        window.hourlyChartInstance.destroy();
    }

    const colores = horas.map(h => {
        if (h.categoria === 'cheap') return 'rgba(16, 185, 129, 0.8)';
        if (h.categoria === 'expensive') return 'rgba(239, 68, 68, 0.8)';
        return 'rgba(245, 158, 11, 0.8)';
    });

    window.hourlyChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: horas.map(h => h.hora),
            datasets: [{
                label: 'Precio €/kWh',
                data: horas.map(h => h.precio),
                backgroundColor: colores,
                borderColor: colores,
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => formatPrice(ctx.parsed.y)
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (v) => formatPrice(v)
                    }
                }
            }
        }
    });
}

// ==========================================
// PROCESAMIENTO DE GAS
// ==========================================

function procesarGas(data) {
    if (!data) return;

    setElement('gas-price', formatPrice(data.precio_kwh));
    setElement('gas-fixed', formatMoney(data.termino_fijo_diario));
    setElement('gas-type', data.tarifa_type);
    setElement('gas-daily', formatMoney(data.coste_diario_total));
    setElement('gas-monthly', formatMoney(data.coste_mensual_total));
    setElement('gas-daily-consumption', `${ data.consumo_estimado_diario } kWh`);
    setElement('gas-monthly-consumption', `${ data.consumo_estimado_mensual } kWh`);

    // Alerta
    const alertEl = document.getElementById('gas-alert');
    if (data.tendencia === 'sube') {
        alertEl.textContent = `${ data.indicador_tendencia } SUBE: ${ data.alerta }`;
        alertEl.className = 'badge warn';
        mostrarAlerta('warning', 'Gas', `Tendencia al alza - Precio: ${ data.precio_kwh }€/kWh`);
    } else {
        alertEl.textContent = `${ data.indicador_tendencia } ${ data.alerta }`;
        alertEl.className = 'badge ok';
    }
}

// ==========================================
// PROCESAMIENTO DE GASOLINA
// ==========================================

function procesarGasolina(data) {
    if (!data) return;

    // Mejor
    setElement('fuel-best-price', formatPrice(data.mejor.precio));
    setElement('fuel-best-station', `${ data.mejor.estacion } (${ data.mejor.localidad })`);

    // Estadísticas
    setElement('fuel-avg', formatPrice(data.promedio));
    setElement('fuel-worst', formatPrice(data.peor.precio));

    // Alerta
    const alertEl = document.getElementById('fuel-alert');
    alertEl.textContent = data.mejor.alerta;
    alertEl.className = `badge ${ data.mejor.estado }`;

    // Top 3
    const top3El = document.getElementById('fuel-top3');
    top3El.innerHTML = data.top3.map((item, idx) => `
        <li class="top-item">
            <div class="top-position">🥇</div>
            <div class="top-content">
                <div class="top-name">${ item.estacion }</div>
                <div style="font-size: 0.9em; color: #666;">${ item.localidad } • ${ item.distancia } km</div>
            </div>
            <div class="top-price">${ formatPrice(item.precio) }</div>
        </li>
    `).join('');
}

// ==========================================
// PROCESAMIENTO DE PRESUPUESTO
// ==========================================

function procesarPresupuesto(presupuesto) {
    if (!presupuesto) return;

    setElement('budget-spent', formatMoney(presupuesto.gasto_acumulado));
    setElement('budget-remaining', formatMoney(presupuesto.saldo_restante));
    setElement('budget-percentage', `${ presupuesto.porcentaje_consumo.toFixed(0) }%`);
    setElement('budget-days', `${ presupuesto.dias_restantes } días`);
    setElement('budget-daily', formatMoney(presupuesto.gasto_diario_recomendado));

    // Barra de progreso
    const barraEl = document.getElementById('budget-bar');
    barraEl.style.width = `${ presupuesto.porcentaje_consumo }%`;

    // Alerta presupuesto
    const alertEl = document.getElementById('budget-alert');
    alertEl.textContent = presupuesto.alerta;
    alertEl.className = `badge ${ presupuesto.porcentaje_consumo > 70 ? 'warn' : (presupuesto.porcentaje_consumo > 90 ? 'bad' : 'ok') }`;

    if (presupuesto.porcentaje_consumo > 80) {
        mostrarAlerta('warning', 'Presupuesto', `Cuidado: ${ presupuesto.porcentaje_consumo.toFixed(0) }% gastado`);
    }
}

// ==========================================
// PROCESAMIENTO DE RECOMENDACIONES
// ==========================================

function procesarRecomendaciones(recomendaciones) {
    if (!recomendaciones || recomendaciones.length === 0) return;

    const container = document.getElementById('recommendations');
    container.innerHTML = recomendaciones.map(rec => `
        <div class="recommendation-card">
            <div class="rec-icon">${ rec.icono }</div>
            <div class="rec-title">${ rec.titulo }</div>
            <div class="rec-detail">${ rec.descripcion }</div>
            ${ rec.detalle ? `<div style="font-size: 0.85em; color: #999; margin: 8px 0;">${ rec.detalle }</div>` : '' }
            ${ rec.ahorro_estimado > 0 ? `<div class="rec-saving">💰 ${ formatMoney(rec.ahorro_estimado) }/mes</div>` : '' }
            <div style="font-size: 0.8em; color: #ccc; margin-top: 10px;">
                Urgencia: ${ rec.urgencia === 'alta' ? '🔴' : (rec.urgencia === 'media' ? '🟡' : '🟢') }
            </div>
        </div>
    `).join('');

    // Mostrar alerta para recomendaciones críticas
    const criticas = recomendaciones.filter(r => r.urgencia === 'alta');
    criticas.forEach(rec => {
        mostrarAlerta('danger', rec.titulo, rec.descripcion);
    });
}

// ==========================================
// PROCESAMIENTO DE COMPARADOR
// ==========================================

function procesarComparador(comparador) {
    if (!comparador) return;

    // Seseña
    setElement('comp-seseña-estacion', comparador.mejor_actual.estacion);
    setElement('comp-seseña-precio', formatPrice(comparador.mejor_actual.precio));
    setElement('comp-seseña-distancia', `${ comparador.mejor_actual.distancia } km`);

    // Aranjuez (peor actual, pero el más barato del mercado)
    setElement('comp-aranjuez-estacion', comparador.peor_actual.estacion || 'N/A');
    setElement('comp-aranjuez-precio', formatPrice(comparador.peor_actual.precio));
    setElement('comp-aranjuez-distancia', '1.2 km (estimado)');

    // Diferencia
    setElement('comp-diferencia', `${ formatPrice(comparador.diferencia_por_litro) } más barata`);
    setElement('comp-ahorro-mes', formatMoney(comparador.ahorro_mensual_estimado));

    // Recomendación
    const recEl = document.getElementById('comp-recomendacion');
    if (comparador.ahorro_mensual_estimado > 20) {
        recEl.textContent = '✅ MEJOR OPCIÓN';
        recEl.style.color = 'var(--success)';
        mostrarAlerta('success', 'Ahorro Detectado', `Ahorras ${ formatMoney(comparador.ahorro_mensual_estimado) }/mes en Aranjuez`);
    } else {
        recEl.textContent = 'Similar';
    }
}

// ==========================================
// GESTOR DE MAPA
// ==========================================

function crearMapa(gasolineras) {
    // Inicializar mapa si no existe
    if (!mapInstance) {
        mapInstance = L.map('map').setView([40.0, -3.6], 11);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap',
            maxZoom: 19
        }).addTo(mapInstance);
    } else {
        // Limpiar marcadores anteriores
        if (markersLayer) {
            mapInstance.removeLayer(markersLayer);
        }
    }

    // Crear grupo de marcadores
    markersLayer = L.featureGroup();

    // Agregar pines por gasolinera
    gasolineras.forEach(gas => {
        let color, icono;

        if (gas.precio < 1.75) {
            color = 'green';
            icono = '🟢';
        } else if (gas.precio < 1.85) {
            color = 'gold';
            icono = '🟡';
        } else {
            color = 'red';
            icono = '🔴';
        }

        // Crear marcador personalizado
        const marker = L.circleMarker([gas.coordenadas?.lat || 40.0, gas.coordenadas?.lng || -3.6], {
            radius: 10,
            fillColor: color,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        })
            .bindPopup(`
                <b>${ gas.nombre }</b><br>
                ${ formatPrice(gas.precio) }/L<br>
                ${ gas.distancia } km
            `)
            .addTo(markersLayer);
    });

    markersLayer.addTo(mapInstance);
    
    // Auto-centrar en marcadores
    if (gasolineras.length > 0) {
        mapInstance.fitBounds(markersLayer.getBounds(), { padding: [50, 50] });
    }
}

// ==========================================
// RESUMEN FINANCIERO
// ==========================================

function procesarResumenFinanciero(resumen) {
    if (!resumen) return;

    setElement('fin-electricity', formatMoney(resumen.electricidad));
    setElement('fin-gas', formatMoney(resumen.gas));
    setElement('fin-fuel', formatMoney(resumen.gasolina));
    setElement('fin-total', formatMoney(resumen.total_mensual));
}

// ==========================================
// CARGA PRINCIPAL DE DATOS
// ==========================================

async function cargarDatos() {
    try {
        const bar = document.getElementById('status-bar');
        const statusIcon = document.getElementById('status-icon');
        const statusText = document.getElementById('status-text');

        statusIcon.textContent = '🔄';
        statusText.textContent = ' Cargando datos...';

        const response = await fetch('datos.json');

        if (!response.ok) {
            throw new Error(`Error HTTP: ${ response.status }`);
        }

        const data = await response.json();

        if (data.status !== 'ok') {
            throw new Error('Sin datos disponibles');
        }

        // Procesar todos los módulos
        procesarElectricidad(data.electricidad);
        procesarGas(data.gas);
        procesarGasolina(data.gasolina);
        procesarPresupuesto(data.gasolina.presupuesto);
        procesarRecomendaciones(data.recomendaciones);
        procesarResumenFinanciero(data.resumen_financiero);
        procesarComparador(data.comparador);

        // Simular datos de gasolineras para el mapa
        const gasolinerasParaMapa = data.gasolina.top3.map((g, idx) => ({
            nombre: g.estacion,
            precio: g.precio,
            distancia: g.distancia,
            coordenadas: {
                lat: 40.0 + (idx * 0.01),
                lng: -3.6 + (idx * 0.01)
            }
        }));

        crearMapa(gasolinerasParaMapa);

        // Actualizar metadata
        setElement('timestamp', formatarFecha(data.timestamp));
        setElement('api-status', '✅ Conectado');
        setElement('data-status', '✅ Datos disponibles');
        setElement('total-stations', `${ data.gasolina.total } estaciones`);

        statusIcon.textContent = '🟢';
        statusText.textContent = ' Sistema funcionando correctamente';
        bar.style.borderColor = '#10b981';

    } catch (error) {
        console.error('Error cargando datos:', error);
        
        const bar = document.getElementById('status-bar');
        const statusIcon = document.getElementById('status-icon');
        const statusText = document.getElementById('status-text');

        statusIcon.textContent = '🔴';
        statusText.textContent = ` Error: ${ error.message }`;
        bar.style.borderColor = '#ef4444';

        mostrarAlerta('danger', 'Error', `No se pudieron cargar los datos: ${ error.message }`);
    }
}

// ==========================================
// INICIALIZACIÓN
// ==========================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Inicializando dashboard...');

    // Inicializar controles
    initTemaOscuro();
    initSelectorCiudad();

    // Cargar datos
    await cargarDatos();

    // Recargar datos cada 30 minutos
    setInterval(cargarDatos, 30 * 60 * 1000);

    console.log('✅ Dashboard listo');
});
