document.addEventListener("DOMContentLoaded", async () => {
    
    // =========================
    // FUNCIONES AUXILIARES
    // =========================
    
    function setElement(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }

    function setStatus(text, type = 'loading') {
        const icons = {
            'loading': '🔄',
            'ok': '🟢',
            'warn': '🟡',
            'error': '🔴'
        };
        const colors = {
            'loading': '#667eea',
            'ok': '#10b981',
            'warn': '#f59e0b',
            'error': '#ef4444'
        };

        const bar = document.getElementById('status-bar');
        if (bar) bar.style.borderColor = colors[type] || '#667eea';

        document.getElementById('status-icon').textContent = icons[type] || '❓';
        document.getElementById('status-text').textContent = ' ' + text;
    }

    // =========================
    // CARGAR DATOS DEL JSON
    // =========================
    
    async function cargarDatos() {
        try {
            setStatus('Obteniendo datos...', 'loading');

            const response = await fetch('datos.json');
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }

            const data = await response.json();

            if (data.status !== 'ok' || !data.gasolina) {
                throw new Error('Sin datos disponibles');
            }

            // Procesar gasolina
            procesarGasolina(data.gasolina);

            // Procesar energía
            if (data.energia) {
                procesarEnergia(data.energia);
            }

            // Actualizar metadata
            setElement('timestamp', formatearFecha(data.timestamp));
            setElement('api-status', '✅ Conectado');
            setElement('data-status', '✅ Datos disponibles');

            setStatus('Sistema funcionando correctamente', 'ok');

        } catch (error) {
            console.error('Error cargando datos:', error);
            mostrarError(error.message);
            setStatus(`Error: ${error.message}`, 'error');
        }
    }

    // =========================
    // PROCESAR GASOLINA
    // =========================
    
    function procesarGasolina(data) {
        if (!data.mejor) return;

        const mejor = data.mejor;
        
        setElement('better-price', `${mejor.precio.toFixed(3).replace('.', ',')} €/L`);
        setElement('better-station', `📍 ${mejor.estacion}`);
        
        const alertBadge = document.getElementById('better-alert');
        alertBadge.textContent = mejor.alerta;
        alertBadge.className = `badge ${mejor.estado}`;

        if (data.promedio) {
            setElement('avg-price', `${data.promedio.toFixed(3).replace('.', ',')}€`);
        }

        setElement('total-stations', data.total || 0);

        if (data.peor) {
            setElement('worst-price', `${data.peor.precio.toFixed(3).replace('.', ',')} €/L`);
            setElement('worst-station', `📍 ${data.peor.estacion}`);
        }

        // Procesar Top 3
        if (data.top3 && data.top3.length > 0) {
            procesarTop3(data.top3);
        }
    }

    // =========================
    // PROCESAR TOP 3
    // =========================
    
    function procesarTop3(top3) {
        if (!top3 || top3.length === 0) {
            setElement('top3-list', '<li style="text-align: center; color: #999; padding: 30px;">Sin datos disponibles</li>');
            return;
        }

        let html = '';
        for (const item of top3) {
            html += `
                <li class="top3-item">
                    <div class="top3-position">
                        ${item.posicion === 1 ? '🥇' : item.posicion === 2 ? '🥈' : '🥉'}
                    </div>
                    <div class="top3-content">
                        <div class="top3-station">${item.estacion}</div>
                        <div class="top3-price">${item.precio.toFixed(3).replace('.', ',')} €/L</div>
                    </div>
                </li>
            `;
        }

        const list = document.getElementById('top3-list');
        list.innerHTML = html;
    }

    // =========================
    // PROCESAR ENERGÍA
    // =========================
    
    function procesarEnergia(data) {
        if (data.luz) {
            setElement('light-price', `${data.luz.precio.toFixed(3).replace('.', ',')} €`);
            setElement('light-status', data.luz.estado);
        }

        if (data.gas) {
            setElement('gas-price', `${data.gas.precio.toFixed(3).replace('.', ',')} €`);
        }
    }

    // =========================
    // MOSTRAR ERROR
    // =========================
    
    function mostrarError(mensaje) {
        setElement('better-price', '❌ Error');
        setElement('better-station', mensaje || 'No se pudieron cargar los datos');
        setElement('light-price', '--');
        setElement('gas-price', '--');
        setElement('api-status', '❌ Desconectado');
    }

    // =========================
    // FORMATEAR FECHA
    // =========================

    function formatearFecha(isoString) {
        try {
            const date = new Date(isoString);
            return date.toLocaleString('es-ES', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (e) {
            return '--';
        }
    }

    // =========================
    // INICIALIZACIÓN
    // =========================
    
    // Cargar datos al iniciar
    await cargarDatos();

});
