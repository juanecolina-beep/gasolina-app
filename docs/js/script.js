
document.getElementById("barata").textContent = "💰 No hay datos - No hay datos: 0 € ¡Mejor precio!";
const csv_link = document.getElementById("csvlink");
csv_link.href = "precios_gasolina_2026-03-20.csv?v=" + Date.now();
csv_link.download = "precios_gasolina_2026-03-20.csv";
