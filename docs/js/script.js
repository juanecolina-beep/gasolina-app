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
    if (el) el.textContent = content;
}

// ===== SISTEMA DE ALERTAS =====
function mostrarAlerta(tipo, titulo, mensaje) {
    const container = document.getElementById('alerts-container');
    if (!container) return;
    
    const alert = document.createElement('div');
    alert.className = `alert-toast ${tipo}`;
    alert.innerHTML = `<div class="alert-toast-title">${titulo}</div><div class="alert-toast-message">${mensaje}</div>`;
    container.appendChild(alert);
    
    setTimeout(() => {
        alert.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => alert.remove(), 300);
    }, 4000);
}

// ===== PROCESADOR DE ELECTRICIDAD =====
function procesarElectricidad(data) {
    if (!data || !data.electricidad) return;
    const elec = data.electricidad;
    
    setElement('elec-mejor-hora', elec.mejor_ventana.inicio);
    setElement('elec-promedio', formatPrice(elec.precio_promedio));
    setElement('elec-coste', formatMoney(elec.coste_mensual_estimado));
    setElement('fin-electricity', formatMoney(elec.coste_mensual_estimado));
    
    mostrarAlerta('success', '⚡ Electricidad', `Mejor hora: ${elec.mejor_ventana.inicio}`);
}

// ===== PROCESADOR DE GAS =====
function procesarGas(data) {
    if (!data || !data.gas) return;
    const gas = data.gas;
    
    setElement('gas-precio', formatPrice(gas.precio_kwh));
    setElement('gas-tendencia', gas.tendencia.toUpperCase());
    setElement('gas-coste', formatMoney(gas.coste_mensual_total));
    setElement('fin-gas', formatMoney(gas.coste_mensual_total));
    
    mostrarAlerta('warning', '🔥 Gas', gas.alerta);
}

// ===== PROCESADOR DE GASOLINA =====
function procesarGasolina(data) {
    if (!data || !data.gasolina) return;
    const gasolina = data.gasolina;
    
    setElement('gas-mejor', formatPrice(gasolina.mejor.precio));
    setElement('gas-estacion', gasolina.mejor.estacion);
    setElement('gas-presupuesto', formatMoney(gasolina.presupuesto.total));
    setElement('fin-fuel', formatMoney(gasolina.presupuesto.total));
}

// ===== MAPA CON LEAFLET =====
let mapInstance = null;

function crearMapa(gasolineras) {
    if (!gasolineras || gasolineras.length === 0) return;
    
    const container = document.getElementById('map');
    if (!container) return;
    
    if (mapInstance) mapInstance.remove();
    
    mapInstance = L.map(container).setView([40.08, -3.57], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(mapInstance);
    
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

// ===== CARGA DE DATOS =====
async function cargarDatos() {
    try {
        const response = await fetch('./datos.json');
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Procesar todos los datos
        procesarElectricidad(data);
        procesarGas(data);
        procesarGasolina(data);
        
        // Crear mapa
        if (data.gasolina && data.gasolina.estaciones) {
            crearMapa(data.gasolina.estaciones);
        }
        
        // Mostrar timestamp
        setElement('timestamp', formatarFecha(data.timestamp));
        
        // Total mensual
        const total = (data.electricidad?.coste_mensual_estimado || 0) + 
                     (data.gas?.coste_mensual_total || 0) + 
                     (data.gasolina?.presupuesto?.total || 0);
        setElement('fin-total', formatMoney(total));
        
        console.log('✅ Datos cargados correctamente');
        
    } catch (error) {
        console.error('Error cargando datos:', error);
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
        if (window.mapInstance) mapInstance.invalidateSize();
    };
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