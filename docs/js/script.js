
document.getElementById('barata').textContent = "💰 REPSOL - 1.579€ 🚨 MUY BARATA";
document.getElementById('luz').textContent = "0.135 €/kWh (🟡 Media) ⚖️ Normal";
document.getElementById('gas').textContent = "0.042 €/kWh";

// TOP 3
console.log("TOP 3 GASOLINERAS:\nREPSOL - 1.579€\nREPSOL - 1.589€\nREPSOL - 1.589€");

const ts = Date.now();
document.getElementById('csvlink').href = "precios_gasolina_2026-04-03.csv?v=" + ts;
document.getElementById('img_gasolina').src = "historial_gasolina.png?v=" + ts;
document.getElementById('img_energia').src = "historial_energia.png?v=" + ts;
