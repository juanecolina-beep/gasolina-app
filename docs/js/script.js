
document.getElementById("barata").textContent = "💰 REPSOL - CR A-4, 32: 1.799 € ¡Mejor precio!";
const csv_link = document.getElementById("csvlink");
csv_link.href = "precios_gasolina_2026-03-17.csv?v=" + Date.now();
csv_link.download = "precios_gasolina_2026-03-17.csv";
