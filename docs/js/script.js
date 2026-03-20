
// ==========================
// Script dinámico para web
// ==========================

// Gasolinera más barata
document.getElementById("barata").textContent = "💰 REPSOL - CR A-4, 32: 1.835 € ¡Mejor precio!";

// Valores de energía
document.getElementById("luz").textContent = "0.105 €/kWh (🟡 Media)";
document.getElementById("gas").textContent = "0.042 €/kWh";

// Refrescar CSV
const csv_link = document.getElementById("csvlink");
csv_link.href = "precios_gasolina_2026-03-20.csv?v=" + Date.now();
csv_link.download = "precios_gasolina_2026-03-20.csv";

// Refrescar gráficos para evitar cache
document.getElementById("img_gasolina").src = "historial_gasolina.png?v=" + Date.now();
document.getElementById("img_energia").src = "historial_energia.png?v=" + Date.now();