
fetch('precios_gasolina.csv')
.then(response => {
    if (!response.ok) throw new Error("CSV no encontrado");
    return response.text();
})
.then(text => {
    const lines = text.split('\n').slice(1);
    if (lines.length === 0) {
        document.getElementById('barata').textContent = "No hay datos disponibles";
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
        document.getElementById('barata').textContent = "No hay precios válidos";
    } else {
        document.getElementById('barata').textContent = `${minEstacion}: ${minPrecio} €`;
    }
})
.catch(error => {
    console.error(error);
    document.getElementById('barata').textContent = "No se pudo cargar el CSV";
});
