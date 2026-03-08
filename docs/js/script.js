document.addEventListener("DOMContentLoaded", () => {
    const output = document.getElementById('barata');
    const csvPath = './docs/precios_gasolina.csv?t=' + Date.now(); // ruta relativa correcta

    fetch(csvPath)
    .then(response => {
        if (!response.ok) throw new Error("CSV no encontrado");
        return response.text();
    })
    .then(text => {
        const lines = text.trim().split('\n').slice(1);
        if (lines.length === 0) {
            output.textContent = "No hay datos disponibles";
            return;
        }

        let minPrecio = Infinity;
        let minEstacion = '';
        for (let line of lines) {
            if(!line) continue;
            const [fecha, estacion, direccion, precio] = line.split(';');
            const p = parseFloat(precio);
            if (!isNaN(p) && p < minPrecio) {
                minPrecio = p;
                minEstacion = `${estacion} - ${direccion}`;
            }
        }

        if (minPrecio === Infinity) {
            output.textContent = "No hay precios válidos";
        } else {
            output.innerHTML = `💰 <strong>${minEstacion}</strong>: ${minPrecio} € ¡Mejor precio!`;
        }
    })
    .catch(error => {
        console.error(error);
        output.textContent = "No se pudo cargar el CSV";
    });
});