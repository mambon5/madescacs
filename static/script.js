let origen = null;

function crearTauler(data) {
    const tauler = document.getElementById("tauler");
    tauler.innerHTML = "";

    data.tauler.forEach((fila, y) => {
        fila.forEach((pieza, x) => {
            const casella = document.createElement("div");
            casella.className = `casella ${(x + y) % 2 === 0 ? 'blanca' : 'negra'}`;
            casella.textContent = pieza;
            casella.dataset.x = x;
            casella.dataset.y = y;
            casella.addEventListener("click", onCasellaClick);
            tauler.appendChild(casella);
        });
    });
}

function onCasellaClick(e) {
    const x = parseInt(e.currentTarget.dataset.x);
    const y = parseInt(e.currentTarget.dataset.y);

    if (origen === null) {
        origen = { x, y };
        e.currentTarget.classList.add("seleccionada");
    } else {
        const desti = { x, y };
        fetch("/moviment", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ origen, desti })
        })
        .then(res => res.json())
        .then(data => {
            crearTauler(data);
        });
        origen = null;
    }
}

function carregarTauler() {
    fetch("/estat")
        .then(res => res.json())
        .then(data => crearTauler(data));
}

carregarTauler();
