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

function setElement(id, content) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = content;
        console.log(`✓ ${id} = ${content}`);
    } else {
        console.warn(`⚠ No encontrado: #${id}`);
    }
}

// ===== SISTEMA DE ALERTAS =====
function mostrarAlerta(tipo, titulo, mensaje) {
    const container = document.getElementById('alerts-container');
    if (!container) {
        console.warn('⚠ No encontrado: alerts-container');
        return;
    }
    
    const alert = document.createElement('div');
    alert.className = `alert-toast ${tipo}`;
    alert.innerHTML = `<strong>${titulo}:</strong> ${mensaje}`;
    container.appendChild(alert);
    
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.3s ease-out';
        setTimeout(() => alert.remove(), 300);
    }, 4000);
}

// ===== PROCESADOR DE ELECTRICIDAD =====
function procesarElectricidad(data) {
    if (!data || !data.electricidad) {
        console.error('❌ No hay datos de electricidad');
        return;
    }
    const elec = data.electricidad;
    
    console.log('⚡ Procesando electricidad...', elec);
    
    // Mejor hora
    setElement('elec-mejor-hora', elec.mejor_ventana.inicio || '--:--');
    
    // Precio promedio
    setElement('elec-promedio', formatPrice(elec.precio_promedio));
    
    // Crear grid de horas
    const grid = document.getElementById('hours-grid');
    if (grid && elec.horas) {
        grid.innerHTML = elec.horas.map(h => `
            <div class="hour-cell ${h.categoria}" title="${h.hora}: ${formatPrice(h.precio)}">
                ${h.hora.split(':')[0]}h
            </div>
        `).join('');
    }
    
    mostrarAlerta('success', '⚡ Electricidad', `Mejor hora: ${elec.mejor_ventana.inicio}`);
}

// ===== PROCESADOR DE GAS =====
function procesarGas(data) {
    if (!data || !data.gas) {
        console.error('❌ No hay datos de gas');
        return;
    }
    const gas = data.gas;
    
    console.log('🔥 Procesando gas...', gas);
    
    setElement('gas-precio', formatPrice(gas.precio_kwh));
    setElement('gas-precio-kwh', formatPrice(gas.precio_kwh));
    setElement('gas-coste-mes', formatMoney(gas.coste_mensual_total));
    setElement('gas-tendencia', gas.tendencia ? gas.tendencia.toUpperCase() : 'N/A');
    
    mostrarAlerta('warning', '🔥 Gas', `Precio: ${formatPrice(gas.precio_kwh)}/kWh`);
}

// ===== PROCESADOR DE GASOLINA =====
function procesarGasolina(data) {
    if (!data || !data.gasolina) {
        console.error('❌ No hay datos de gasolina');
        return;
    }
    const gasolina = data.gasolina;
    
    console.log('⛽ Procesando gasolina...', gasolina);
    
    // Encontrar las más baratas de Aranjuez y Seseña
    const lista = document.getElementById('fuel-list');
    if (!lista) return;
    
    const estaciones = gasolina.estaciones || [];
    
    // Filtrar Aranjuez y Seseña y ordenar por precio
    const filtered = estaciones.filter(e => {
        const localidad = (e.localidad || '').toLowerCase();
        return localidad.includes('aranjuez') || localidad.includes('seseña');
    }).sort((a, b) => a.precio - b.precio);
    
    console.log('🔍 Estaciones filtradas:', filtered);
    
    if (filtered.length === 0) {
        lista.innerHTML = '<li class="fuel-item">No hay datos de gasolineras</li>';
        return;
    }
    
    lista.innerHTML = filtered.slice(0, 3).map((g, idx) => `
        <li class="fuel-item ${idx === 0 ? 'best' : ''}">
            <span class="fuel-name">${g.nombre} (${g.localidad})</span>
            <span class="fuel-price">${formatPrice(g.precio)}</span>
        </li>
    `).join('');
    
    mostrarAlerta('success', '⛽ Gasolina', `Más barata: ${filtered[0].nombre} @ ${formatPrice(filtered[0].precio)}`);
}

// ===== PROCESADOR DE RESUMEN MENSUAL =====
function procesarResumenMensual(data) {
    if (!data) {
        console.error('❌ No hay datos para resumen');
        return;
    }
    
    console.log('📊 Procesando resumen mensual...');
    
    // Electricidad
    const elec = data.electricidad?.coste_mensual_estimado || 0;
    setElement('mes-electricidad', formatMoney(elec));
    
    // Gas
    const gas = data.gas?.coste_mensual_total || 0;
    setElement('mes-gas', formatMoney(gas));
    
    // Gasolina (presupuesto mensual)
    const gasolina = data.gasolina?.presupuesto?.total || 0;
    setElement('mes-gasolina', formatMoney(gasolina));
    
    // Total
    const total = elec + gas + gasolina;
    setElement('mes-total', formatMoney(total));
    
    console.log('✓ Resumen mensual:', { elec, gas, gasolina, total });
}

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Inicializando dashboard...');
    initTemaOscuro();
    await cargarDatos();
    
    // Recargar datos cada 30 minutos
    setInterval(cargarDatos, 30 * 60 * 1000);
    
    console.log('✅ Dashboard listo');
});
async function cargarDatos() {
    try {
        console.log('🔄 Iniciando carga de datos...');
        
        const response = await fetch('./datos.json');
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('📊 Datos recibidos:', data);
        
        // Procesar resumen mensual
        procesarResumenMensual(data);
        
        // Procesar todos los datos
        procesarElectricidad(data);
        procesarGas(data);
        procesarGasolina(data);
        
        // Mostrar timestamp
        setElement('timestamp', formatarFecha(data.timestamp));
        
        console.log('✅ Datos cargados correctamente');
        
    } catch (error) {
        console.error('❌ Error cargando datos:', error);
        mostrarAlerta('danger', '❌ Error', 'No se pudieron cargar los datos: ' + error.message);
    }
}

// ===== TEMA OSCURO =====
function initTemaOscuro() {
    const html = document.documentElement;
    const toggle = document.getElementById('theme-toggle');
    
    if (!toggle) return;
    
    const isDark = localStorage.getItem('theme') === 'dark';
    if (isDark) html.classList.add('dark-mode');
    
    toggle.onclick = () => {
        const newDark = !html.classList.toggle('dark-mode');
        localStorage.setItem('theme', newDark ? 'dark' : 'light');
    };
}