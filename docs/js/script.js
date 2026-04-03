function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

// =========================
// ESTADO INICIAL
// =========================
let hasData = false;

// =========================
// GASOLINA (FALLBACK SEGURO)
// =========================
const mejorPrecio = "⚠️ Sin datos disponibles";
setText('barata', mejorPrecio);

// =========================
// ENERGÍA (FALLBACK REALISTA)
// =========================
const precioLuz = 0.135;
const estadoLuz = "🟡 Media";
const recomendacionLuz = "⚖️ Normal";

setText('luz', `${precioLuz} €/kWh (${estadoLuz}) ${recomendacionLuz}`);
setText('gas', "0.042 €/kWh");

// =========================
// TOP 3 (VISIBLE, NO CONSOLE)
// =========================
const top3 = "No hay datos disponibles";

const top3El = document.getElementById('top3');
if (top3El) {
    top3El.textContent = top3;
}

// =========================
// STATUS SISTEMA
// =========================
const statusEl = document.getElementById('status');
if (statusEl) {
    statusEl.textContent = "🟡 Modo fallback activo (datos simulados)";
    statusEl.className = "status warn";
}

// =========================
// TIMESTAMP + CACHE BUSTING
// =========================
const ts = Date.now();

const csv = document.getElementById('csvlink');
if (csv) csv.href = `precios_gasolina_2026-04-03.csv?v=${ts}`;

const img1 = document.getElementById('img_gasolina');
if (img1) img1.src = `historial_gasolina.png?v=${ts}`;

const img2 = document.getElementById('img_energia');
if (img2) img2.src = `historial_energia.png?v=${ts}`;
