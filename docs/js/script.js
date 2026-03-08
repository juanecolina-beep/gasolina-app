
fetch('precios_gasolina.csv?t=' + Date.now())
.then(response => response.text())
.then(text => {
    const lines = text.split('\n').slice(1);
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
    document.getElementById('barata').textContent = minPrecio === Infinity ? "No hay precios válidos" : `💰 ${minEstacion}: ${minPrecio} € ¡Mejor precio!`;
})
.catch(() => {
    document.getElementById('barata').textContent = "No se pudo cargar el CSV";
});
