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

// 3. Functia care aduce datele pentru Tabelul Ownership
async function incarcaOwnership() {
    const corpTabel = document.getElementById('corpTabelOwnership');
    corpTabel.innerHTML = "<tr><td colspan='5' style='text-align: center;'>Se incarca datele...</td></tr>";
    
    try {
        const response = await fetch('/ownership/');
        const data = await response.json();
        
        corpTabel.innerHTML = "";
        
        if(data.length === 0) {
            corpTabel.innerHTML = "<tr><td colspan='5' style='text-align: center;'>Nu exista inregistrari in Ownership.</td></tr>";
        } else {
            data.forEach(rand => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${rand.identifier_name || "-"}</strong></td>
                    <td>${rand.originator_first_name || "-"}</td>
                    <td>${rand.originator_last_name || "-"}</td>
                    <td><a href="mailto:${rand.email}">${rand.email || "-"}</a></td>
                    <td>${rand.owner_last_name || "-"}</td>
                `;
                corpTabel.appendChild(tr);
            });
        }
    } catch (error) {
        corpTabel.innerHTML = "<tr><td colspan='5' style='text-align: center; color: red;'>Eroare la incarcarea tabelului.</td></tr>";
    }
}

// Apelam functia ca sa se incarce automat cand deschidem pagina
incarcaOwnership();