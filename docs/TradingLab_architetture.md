# Trading Lab

## Software Requirements Specification (SRS)

Versione: 0.1
Stato: Draft

---

# 1. Obiettivo

Trading Lab è un'applicazione della piattaforma **Quantica** destinata allo studio, all'analisi e alla simulazione dei mercati finanziari.

L'applicazione non nasce per eseguire automaticamente ordini di acquisto o vendita, ma come laboratorio di analisi, backtesting e sviluppo di strategie.

L'obiettivo è costruire una piattaforma modulare che possa crescere nel tempo senza richiedere modifiche all'infrastruttura Quantica.

---

# 2. Architettura

Trading Lab viene eseguita come applicazione indipendente all'interno della piattaforma Quantica.

L'applicazione utilizza:

* Docker
* Python
* FastAPI
* PostgreSQL
* REST API
* HTML/CSS/Javascript
* Modulo finnhub-python  https://github.com/Finnhub-Stock-API/finnhub-python

L'applicazione utilizza il database PostgreSQL condiviso della piattaforma Quantica ma possiede:

* database dedicato
* utente dedicato
* schema dedicato

---

# 3. Obiettivi funzionali

L'applicazione dovrà permettere di:

* consultare dati finanziari
* scaricare serie storiche
* memorizzare i dati localmente
* evitare chiamate duplicate verso i provider esterni
* confrontare strumenti finanziari
* costruire indicatori tecnici
* effettuare backtest
* simulare portafogli
* generare grafici
* esportare dati

---

# 4. Data Provider

Provider iniziale:

* Finnhub

In futuro sarà possibile aggiungere:

* Alpha Vantage
* Yahoo Finance
* Polygon
* TwelveData
* Interactive Brokers
* altri provider

Il sistema dovrà permettere di utilizzare più provider senza modificare il codice dell'applicazione.

---

# 5. Interfaccia Web

La prima interfaccia dovrà essere volutamente semplice.

Funzioni iniziali:

* ricerca ticker
* inserimento ticker manuale
* elenco ticker monitorati
* download dati
* visualizzazione dati
* stato database
* log operazioni

Successivamente saranno aggiunti:

* grafici
* dashboard
* indicatori
* watchlist multiple
* preferiti

---

# 6. Database

Ogni applicazione possiede il proprio database.

Database iniziale:

trading_db

Utente:

trading_app_usr

Il database conterrà inizialmente:

* titoli monitorati
* serie storiche
* log aggiornamenti
* configurazione applicazione

Successivamente saranno aggiunte nuove tabelle.

---

# 7. Raccolta dati

L'applicazione dovrà poter scaricare:

* dati giornalieri
* dati intraday
* dati realtime (se disponibili)
* informazioni societarie
* dividendi
* split
* fondamentali
* news

Ogni richiesta dovrà essere memorizzata nel database.

---

# 8. Cache

Per ridurre il numero di chiamate ai provider esterni, i dati verranno mantenuti nel database.

L'applicazione dovrà verificare se i dati richiesti sono già disponibili prima di effettuare nuove richieste.

---

# 9. API interne

L'applicazione esporrà API REST.

Esempi:

GET /health

GET /symbols

POST /symbols

GET /history/{ticker}

POST /download/{ticker}

GET /status

---

# 10. Configurazione

Le impostazioni saranno memorizzate tramite variabili d'ambiente.

Esempio:

FINNHUB_API_KEY

DB_HOST

DB_NAME

DB_USER

DB_PASSWORD

LOG_LEVEL

---

# 11. Logging

Tutte le operazioni principali dovranno essere registrate.

In particolare:

* avvio
* arresto
* errori
* download dati
* tempo risposta API
* errori provider

---

# 12. Sicurezza

Le API Key non dovranno mai essere salvate nel repository Git.

Le credenziali saranno conservate esclusivamente nei file .env della piattaforma Quantica.

---

# 13. Modularità

L'applicazione dovrà essere progettata per moduli.

Struttura prevista:

* API REST
* servizi
* provider finanziari
* database
* modelli
* frontend
* configurazione

Ogni componente dovrà poter essere sostituito senza modificare gli altri.

---

# 14. Evoluzioni future

Le funzionalità previste includono:

* analisi tecnica
* strategie automatiche
* AI per suggerimenti
* analisi fondamentali
* portafogli multipli
* simulazioni
* alert
* notifiche Telegram
* notifiche email
* scheduler
* dashboard statistiche
* importazione dati da broker
* esportazione CSV
* esportazione Excel
* gestione utenti
* autenticazione

---

# 15. Requisiti Software

Sistema operativo

* Rocky Linux

Container

* Docker Engine
* Docker Compose

Backend

* Python 3.13+
* FastAPI
* SQLAlchemy
* psycopg
* Uvicorn

Frontend

* HTML5
* CSS3
* Javascript

Database

* PostgreSQL 16+

Versionamento

* Git
* GitHub

IDE

* Visual Studio Code

---

# 16. Filosofia del progetto

Trading Lab è un laboratorio software.

Ogni nuova funzionalità dovrà rispettare i principi della piattaforma Quantica:

* modularità
* riutilizzabilità
* semplicità
* sicurezza
* indipendenza tra applicazioni
* documentazione completa
* infrastruttura separata dalla logica applicativa
