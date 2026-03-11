
document.getElementById("barata").textContent = "💰 REPSOL - AUTOVIA A-4 KM. 36,5: 1.759 € ¡Mejor precio!";
const csv_link = document.getElementById("csvlink");
csv_link.href = "precios_gasolina_2026-03-11.csv?v=" + Date.now();
csv_link.download = "precios_gasolina_2026-03-11.csv";
