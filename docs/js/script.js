// script.js: gasolinera más barata con auto-refresh, resaltado y etiqueta visual
document.addEventListener("DOMContentLoaded", () => {
  const output = document.getElementById('barata');
  const csvPath = 'docs/precios_gasolina.csv'; // Ajusta según tu estructura
  let lastCSV = '';

  async function actualizarGasolinera() {
    try {
      const response = await fetch(csvPath + '?t=' + Date.now()); // evitar cache
      if (!response.ok) throw new Error("CSV no encontrado");
      const text = await response.text();

      if (text === lastCSV) return; // no hay cambios
      lastCSV = text;

      const lines = text.trim().split('\n');
      if (lines.length <= 1) {
        output.innerHTML = "No hay datos disponibles";
        output.style.backgroundColor = "";
        return;
      }

      const dataLines = lines.slice(1).filter(line => line.trim() !== '');
      let minPrecio = Infinity;
      let minEstacion = '';

      for (let line of dataLines) {
        const cols = line.split(',');
        if (cols.length < 4) continue;
        const [fecha, estacion, direccion, precio] = cols;
        const p = parseFloat(precio);
        if (!isNaN(p) && p < minPrecio) {
          minPrecio = p;
          minEstacion = `${estacion} - ${direccion}`;
        }
      }

      if (minPrecio === Infinity) {
        output.innerHTML = "No hay precios válidos";
        output.style.backgroundColor = "";
      } else {
        // Mostrar con icono y etiqueta
        output.innerHTML = `💰 <strong>${minEstacion}</strong> - ${minPrecio.toFixed(2)} € <span style="color: green; font-weight: bold;">¡Mejor precio!</span>`;

        // Resaltado visual temporal
        output.style.transition = "background-color 0.8s ease";
        output.style.backgroundColor = "#d4edda"; // verde suave
        setTimeout(() => {
          output.style.backgroundColor = "";
        }, 2000);
      }

    } catch (error) {
      console.error(error);
      output.innerHTML = "No se pudo cargar el CSV";
      output.style.backgroundColor = "#f8d7da"; // rojo suave para error
      setTimeout(() => {
        output.style.backgroundColor = "";
      }, 2000);
    }
  }

  // Actualiza al cargar y luego cada 5 minutos
  actualizarGasolinera();
  setInterval(actualizarGasolinera, 5 * 60 * 1000);
});