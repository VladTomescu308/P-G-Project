const butonIncarca = document.getElementById('btnIncarca');
const lista = document.getElementById('listaProduse');
const formAdaugare = document.getElementById('formAdaugare');
const mesajFormular = document.getElementById('mesajFormular');

// 1. Functia care aduce datele (GET)
async function incarcaProduse() {
    lista.innerHTML = "<li>Se incarca...</li>";
    try {
        const response = await fetch('/identifiers/');
        const data = await response.json();
        
        lista.innerHTML = "";
        
        if(data.length === 0) {
            lista.innerHTML = "<li>Nu s-a gasit niciun produs.</li>";
        } else {
            data.forEach(produs => {
                const li = document.createElement('li');
                // Adaugam si tipul produsului la afisare
                li.innerHTML = `<strong>${produs.identifier_name}</strong> <br> 
                                <small>Descriere: ${produs.description || "N/A"} | Tip: ${produs.identifier_type || "N/A"}</small>`;
                lista.appendChild(li);
            });
        }
    } catch (error) {
        lista.innerHTML = "<li>Eroare la preluarea datelor.</li>";
    }
}

// Atasam functia pe butonul de Reincarcare
butonIncarca.addEventListener('click', incarcaProduse);

// Incarcam lista automat cand deschidem pagina prima data
incarcaProduse();

// 2. Functia care trimite datele (POST)
formAdaugare.addEventListener('submit', async (event) => {
    // PREVENIM reincarcarea automata a paginii web (comportamentul clasic HTML)
    event.preventDefault(); 
    mesajFormular.textContent = "Se salveaza...";
    mesajFormular.className = "";

    // Preluam valorile introduse de utilizator
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
            body: JSON.stringify(produsNou) // Transformam obiectul JS in string JSON
        });

        if (response.ok) {
            // Daca salvarea a reusit:
            mesajFormular.textContent = "Produs adaugat cu succes!";
            mesajFormular.className = "mesaj-succes";
            
            formAdaugare.reset(); // Curatam campurile formularului automat
            incarcaProduse();     // Reincarcam lista ca sa vedem noul produs direct
            
            // Facem mesajul de succes sa dispara dupa 3 secunde
            setTimeout(() => { mesajFormular.textContent = ""; }, 3000);
        } else {
            // Daca API-ul da eroare (ex: ID-ul exista deja, eroare 400)
            const errorData = await response.json();
            mesajFormular.textContent = `Eroare: ${errorData.detail}`;
            mesajFormular.className = "mesaj-eroare";
        }
    } catch (error) {
        mesajFormular.textContent = "Eroare de conexiune la server.";
        mesajFormular.className = "mesaj-eroare";
    }
});