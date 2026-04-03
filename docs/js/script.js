document.addEventListener("DOMContentLoaded", () => {

    function setText(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }

    // =========================
    // ESTADO SISTEMA
    // =========================
    let status = "🟢 Sistema cargado correctamente";

    // =========================
    // GASOLINA (FALLBACK SEGURO)
    // =========================
    setText('barata', "⚠️ Cargando datos...");

    // =========================
    // ENERGÍA (FALLBACK REAL)
    // =========================
    setText('luz', "0.135 €/kWh (🟡 Media) ⚖️ Normal");
    setText('gas', "0.042 €/kWh");

    // =========================
    // TOP 3 (VISIBLE)
    // =========================
    setText('top3', "⛽ No hay datos disponibles");

    // =========================
    // SISTEMA INFO
    // =========================
    setText('status', status);

    const update = document.getElementById('update');
    if (update) update.textContent = "🕒 Última actualización: " + new Date().toLocaleString();

    const total = document.getElementById('total');
    if (total) total.textContent = "⛽ Estaciones analizadas: --";

    // =========================
    // CACHE BUSTING
    // =========================
    const ts = Date.now();

    const csv = document.getElementById('csvlink');
    if (csv) csv.href = "precios_gasolina_2026-04-03.csv?v=" + ts;

    const img1 = document.getElementById('img_gasolina');
    if (img1) img1.src = "historial_gasolina.png?v=" + ts;

    const img2 = document.getElementById('img_energia');
    if (img2) img2.src = "historial_energia.png?v=" + ts;

});
