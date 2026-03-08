// script.js final con fecha de última actualización
document.addEventListener("DOMContentLoaded", () => {
    const output = document.getElementById('barata');
    const csvPath = './docs/precios_gasolina.csv?t=' + Date.now(); // evita cache

    async function actualizarGasolinera() {
        try {
            const response = await fetch('./docs/precios_gasolina.csv?t=' + Date.now());
            if (!response.ok) throw new Error("CSV no encontrado");
            const text = await response.text();

            const lines = text.trim().split('\n').slice(1); // quitar encabezado
            if (lines.length === 0) {
                output.textContent = "No hay datos disponibles";
                output.style.backgroundColor = "#f8d7da"; // rojo suave para alertar
                return;
            }

            let minPrecio = Infinity;
            let minEstacion = '';
            let fechaActualizacion = '';

            for (let line of lines) {
                if(!line) continue;
                const [fecha, estacion, direccion, precio] = line.split(';');
                const p = parseFloat(precio);
                if (!isNaN(p) && p < minPrecio) {
                    minPrecio = p;
                    minEstacion = `${estacion} - ${direccion}`;
                    fechaActualizacion = fecha;
                }
            }

            if (minPrecio === Infinity) {
                output.textContent = "No hay precios válidos";
                output.style.backgroundColor = "#f8d7da"; // rojo suave
            } else {
                output.innerHTML = `💰 <strong>${minEstacion}</strong>: ${minPrecio.toFixed(2)} €<br><small>Última actualización: ${fechaActualizacion}</small>`;
                output.style.backgroundColor = "#d4edda"; // verde suave
                setTimeout(() => {
                    output.style.backgroundColor = "";
                }, 2000);
            }

        } catch (error) {
            console.error(error);
            output.textContent = "No se pudo cargar el CSV";
            output.style.backgroundColor = "#f8d7da"; // rojo suave
        }
    }

    // Ejecutar al cargar y luego cada 5 minutos
    actualizarGasolinera();
    setInterval(actualizarGasolinera, 5 * 60 * 1000);
});