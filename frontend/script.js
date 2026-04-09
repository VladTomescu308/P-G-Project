const butonIncarca = document.getElementById('btnIncarca');
const lista = document.getElementById('listaProduse');
const formAdaugare = document.getElementById('formAdaugare');
const mesajFormular = document.getElementById('mesajFormular');

// 1. Funcția care aduce datele (GET)
async function incarcaProduse() {
    lista.innerHTML = "<li>Se încarcă... ⏳</li>";
    try {
        const response = await fetch('/identifiers/');
        const data = await response.json();
        
        lista.innerHTML = "";
        
        if(data.length === 0) {
            lista.innerHTML = "<li>Nu s-a găsit niciun produs.</li>";
        } else {
            data.forEach(produs => {
                const li = document.createElement('li');
                // Adăugăm și tipul produsului la afișare
                li.innerHTML = `📦 <strong>${produs.identifier_name}</strong> <br> 
                                <small>Descriere: ${produs.description || "N/A"} | Tip: ${produs.identifier_type || "N/A"}</small>`;
                lista.appendChild(li);
            });
        }
    } catch (error) {
        lista.innerHTML = "<li>❌ Eroare la preluarea datelor.</li>";
    }
}

// Atașăm funcția pe butonul de Reîncărcare
butonIncarca.addEventListener('click', incarcaProduse);

// Încărcăm lista automat când deschidem pagina prima dată
incarcaProduse();

// 2. Funcția care trimite datele (POST)
formAdaugare.addEventListener('submit', async (event) => {
    // PREVENIM reîncărcarea automată a paginii web (comportamentul clasic HTML)
    event.preventDefault(); 
    mesajFormular.textContent = "Se salvează... ⏳";
    mesajFormular.className = "";

    // Preluăm valorile introduse de utilizator
    const nume = document.getElementById('numeProdus').value;
    const descriere = document.getElementById('descriereProdus').value;
    const tip = document.getElementById('tipProdus').value;

    // Construim obiectul JSON cerut de FastAPI
    const produsNou = {
        identifier_name: nume,
        description: descriere,
        identifier_type: tip
    };

    try {
        const response = await fetch('/identifiers/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(produsNou) // Transformăm obiectul JS în string JSON
        });

        if (response.ok) {
            // Dacă salvarea a reușit:
            mesajFormular.textContent = "✅ Produs adăugat cu succes!";
            mesajFormular.className = "mesaj-succes";
            
            formAdaugare.reset(); // Curățăm câmpurile formularului automat
            incarcaProduse();     // Reîncărcăm lista ca să vedem noul produs direct
            
            // Facem mesajul de succes să dispară după 3 secunde
            setTimeout(() => { mesajFormular.textContent = ""; }, 3000);
        } else {
            // Dacă API-ul dă eroare (ex: ID-ul există deja, eroare 400)
            const errorData = await response.json();
            mesajFormular.textContent = `❌ Eroare: ${errorData.detail}`;
            mesajFormular.className = "mesaj-eroare";
        }
    } catch (error) {
        mesajFormular.textContent = "❌ Eroare de conexiune la server.";
        mesajFormular.className = "mesaj-eroare";
    }
});