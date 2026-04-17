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

    function formatPrice(value) {
        return `${value.toFixed(3).replace('.', ',')}€`;
    }

    function formatMoney(value) {
        return `${value.toFixed(2).replace('.', ',')}€`;
    }

    function formatarFecha(iso) {
        const fecha = new Date(iso);
        return fecha.toLocaleString('es-ES');
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

            // Actualizar metadata
            setElement('timestamp', formatarFecha(data.timestamp));
            setElement('api-status', '✅ Conectado');
            setElement('data-status', '✅ Datos disponibles');

            setStatus('Sistema funcionando correctamente', 'ok');

        } catch (error) {
            console.error('Error cargando datos:', error);
            setStatus(`Error: ${error.message}`, 'error');
        }
    }

    // =========================
    // PROCESAR ELECTRICIDAD
    // =========================
    
    function procesarElectricidad(data) {
        if (!data) return;

        // Precios
        setElement('elec-cheap', formatPrice(data.precio_minimo));
        setElement('elec-avg', formatPrice(data.precio_promedio));
        setElement('elec-expensive', formatPrice(data.precio_maximo));

        // Mejor ventana
        setElement('elec-best-hours', `${data.mejor_ventana.inicio} - ${data.mejor_ventana.fin}`);
        setElement('elec-best-price', formatPrice(data.mejor_ventana.promedio));

        // Costes
        setElement('elec-daily-cost', formatMoney(data.coste_diario_estimado));
        setElement('elec-monthly-cost', formatMoney(data.coste_mensual_estimado));

        // Tabla horaria
        generarTablaHoraria(data.horas);

        // Gráfico
        generarGraficoElectricidad(data.horas);
    }

    function generarTablaHoraria(horas) {
        const container = document.getElementById('hourly-prices');
        container.innerHTML = '';

        horas.forEach((hora, idx) => {
            const cell = document.createElement('div');
            cell.className = `hour-cell ${hora.categoria}`;
            cell.textContent = `${idx}:00\n${hora.precio.toFixed(3)}€`;
            cell.title = `${hora.estado}`;
            container.appendChild(cell);
        });
    }

    function generarGraficoElectricidad(horas) {
        const ctx = document.getElementById('hourly-chart');
        if (!ctx) return;

        const colores = horas.map(h => {
            if (h.categoria === 'cheap') return 'rgba(16, 185, 129, 0.6)';
            if (h.categoria === 'expensive') return 'rgba(239, 68, 68, 0.6)';
            return 'rgba(245, 158, 11, 0.6)';
        });

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: horas.map(h => h.hora),
                datasets: [{
                    label: 'Precio (€/kWh)',
                    data: horas.map(h => h.precio),
                    backgroundColor: colores,
                    borderColor: colores,
                    borderWidth: 2,
                    borderRadius: 8,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return formatPrice(context.parsed.y);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatPrice(value);
                            }
                        }
                    }
                }
            }
        });
    }

    // =========================
    // PROCESAR GAS
    // =========================
    
    function procesarGas(data) {
        if (!data) return;

        setElement('gas-price', formatPrice(data.precio_kwh));
        setElement('gas-fixed', formatMoney(data.termino_fijo_diario));
        setElement('gas-type', data.tarifa_type);

        setElement('gas-daily', formatMoney(data.coste_diario_total));
        setElement('gas-monthly', formatMoney(data.coste_mensual_total));

        setElement('gas-daily-consumption', `${data.consumo_estimado_diario} kWh`);
        setElement('gas-monthly-consumption', `${data.consumo_estimado_mensual} kWh`);

        const alertEl = document.getElementById('gas-alert');
        alertEl.textContent = data.alerta;
        alertEl.className = 'badge ' + (data.alerta.includes('✅') ? 'ok' : 'warn');
    }

    // =========================
    // PROCESAR GASOLINA
    // =========================
    
    function procesarGasolina(data) {
        if (!data) return;

        const mejor = data.mejor;
        
        setElement('fuel-best-price', formatPrice(mejor.precio));
        setElement('fuel-best-station', `📍 ${mejor.estacion}`);
        
        const alertBadge = document.getElementById('fuel-alert');
        alertBadge.textContent = mejor.alerta;
        alertBadge.className = `badge ${mejor.estado}`;

        if (data.promedio) {
            setElement('fuel-avg', formatPrice(data.promedio));
        }

        setElement('total-stations', `${data.total} estaciones`);

        if (data.peor) {
            setElement('fuel-worst', formatPrice(data.peor.precio));
        }

        // Top 3 gasolineras
        if (data.top3 && data.top3.length > 0) {
            const top3List = document.getElementById('fuel-top3');
            top3List.innerHTML = '';

            data.top3.forEach(station => {
                const li = document.createElement('li');
                li.className = 'top-item';
                li.innerHTML = `
                    <div class="top-position">${station.posicion}🥇</div>
                    <div class="top-content">
                        <div class="top-name">${station.estacion}</div>
                        <div class="top-price">${formatPrice(station.precio)}</div>
                    </div>
                `;
                top3List.appendChild(li);
            });
        }
    }

    // =========================
    // PROCESAR PRESUPUESTO
    // =========================
    
    function procesarPresupuesto(presupuesto) {
        if (!presupuesto) return;

        const gastado = presupuesto.gasto_acumulado;
        const saldo = presupuesto.saldo_restante;
        const mensual = presupuesto.mensual;
        const dias = presupuesto.dias_restantes;

        setElement('budget-spent', formatMoney(gastado));
        setElement('budget-remaining', formatMoney(saldo));
        
        const porcentaje = (gastado / mensual * 100).toFixed(1);
        setElement('budget-percentage', `${porcentaje}%`);

        const bar = document.getElementById('budget-bar');
        if (bar) {
            bar.style.width = `${Math.min(porcentaje, 100)}%`;
        }

        setElement('budget-days', `${dias} días`);
        
        const gastoDiarioMedio = dias > 0 ? (saldo / dias).toFixed(2) : '0.00';
        setElement('budget-daily', formatMoney(parseFloat(gastoDiarioMedio)));

        const alertEl = document.getElementById('budget-alert');
        alertEl.textContent = presupuesto.alerta;
        
        if (presupuesto.alerta.includes('⚠️')) {
            alertEl.className = 'badge warn';
        } else if (presupuesto.alerta.includes('✅')) {
            alertEl.className = 'badge ok';
        }
    }

    // =========================
    // PROCESAR RECOMENDACIONES
    // =========================
    
    function procesarRecomendaciones(recomendaciones) {
        if (!recomendaciones || recomendaciones.length === 0) return;

        const container = document.getElementById('recommendations');
        container.innerHTML = '';

        recomendaciones.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'recommendation-card';
            card.innerHTML = `
                <div class="rec-icon">${rec.icono}</div>
                <div class="rec-title">${rec.titulo}</div>
                <div class="rec-detail">${rec.detalle}</div>
                <div class="rec-saving">+${formatMoney(rec.ahorro_estimado)} de ahorro</div>
            `;
            container.appendChild(card);
        });
    }

    // =========================
    // PROCESAR RESUMEN FINANCIERO
    // =========================
    
    function procesarResumenFinanciero(resumen) {
        if (!resumen) return;

        setElement('fin-electricity', formatMoney(resumen.electricidad));
        setElement('fin-gas', formatMoney(resumen.gas));
        setElement('fin-fuel', formatMoney(resumen.gasolina));
        setElement('fin-total', formatMoney(resumen.total_mensual));
    }

    // =========================
    // INICIAR CARGA
    // =========================
    
    await cargarDatos();

    // Recargar datos cada 10 minutos
    setInterval(cargarDatos, 600000);

});
