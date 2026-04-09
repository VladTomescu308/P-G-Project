// Prindem butonul și lista din HTML
const buton = document.getElementById('btnIncarca');
const lista = document.getElementById('listaProduse');

// Adăugăm un eveniment de click pe buton
buton.addEventListener('click', async () => {
    lista.innerHTML = "<li>Se încarcă... ⏳</li>";
    
    try {
        // Chemăm ruta din fastAPI.py
        const response = await fetch('/identifiers/');
        const data = await response.json();
        
        // Curățăm lista și adăugăm datele primite
        lista.innerHTML = "";
        
        if(data.length === 0) {
            lista.innerHTML = "<li>Nu s-a găsit niciun produs în baza de date.</li>";
        } else {
            data.forEach(produs => {
                const li = document.createElement('li');
                // Afișăm numele și descrierea din SQL Server
                li.textContent = `📦 ${produs.identifier_name} - ${produs.description || "Fără descriere"}`;
                lista.appendChild(li);
            });
        }
    } catch (error) {
        console.error("Eroare la preluarea datelor:", error);
        lista.innerHTML = "<li>❌ A apărut o eroare la conectarea cu API-ul.</li>";
    }
});