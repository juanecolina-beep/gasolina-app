
document.getElementById('barata').textContent = "💰 REPSOL - CR A-4, 32: 1.835 € ¡Mejor precio!";
document.getElementById('luz').textContent = "0.146 €/kWh (🟡 Media)";
document.getElementById('gas').textContent = "0.042 €/kWh";

const ts = Date.now();
document.getElementById('csvlink').href = "precios_gasolina_2026-03-20.csv?v=" + ts;
document.getElementById('csvlink').download = "precios_gasolina_2026-03-20.csv";
document.getElementById('img_gasolina').src = "historial_gasolina.png?v=" + ts;
document.getElementById('img_energia').src = "historial_energia.png?v=" + ts;
