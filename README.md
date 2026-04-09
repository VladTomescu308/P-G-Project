# P&G Manufacturing Dashboard

Acest proiect este o aplicatie web Full-Stack dezvoltata pentru gestionarea si vizualizarea datelor de productie. Ofera o interfata intuitiva pentru administrarea inventarului (produse/identificatori) si afiseaza statistici detaliate privind consumatorii si proprietatea datelor.

## Tehnologii Utilizate

* **Backend:** Python, FastAPI, Uvicorn
* **Baza de Date:** SQL Server (conectare via SQLAlchemy si PyODBC)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
* **Data Science / Analiza:** Pandas, Matplotlib (pentru generarea graficelor direct din backend)

## Functionalitati Principale

1.  **Gestiunea Inventarului (CRUD):** * Vizualizarea in timp real a produselor din baza de date.
    * Adaugarea de noi produse prin intermediul unui formular validat pe frontend si backend.
2.  **Statistici Consumatori:** * Generarea dinamica a unui grafic de tip bar-chart cu numarul de consumatori pe tari (colorat specific fiecarui steag).
    * Graficul este procesat de Pandas si Matplotlib in memorie si servit ca fisier PNG catre frontend.
3.  **Tabel Ownership:** * Afisarea detaliata a informatiilor despre originatorii si proprietarii datelor.
    * Integrare directa a adreselor de email pentru contact rapid.

## Structura Proiectului

```text
├── frontend/
│   ├── index.html       # Structura paginii web
│   ├── style.css        # Design-ul si formatarea vizuala
│   └── script.js        # Logica aplicatiei si apelurile HTTP (GET, POST)
├── database.py          # Configurarea conexiunii SQL Server si modelele SQLAlchemy
├── authdb.py            # Schemele Pydantic pentru validarea datelor
├── fastAPI.py           # Rutele API-ului si logica de server
├── requirements.txt     # Librariile Python necesare
└── README.md            # Documentatia proiectului