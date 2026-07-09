trading_lab_architecture.md
1. Visione del progetto
2. Obiettivi
3. Casi d'uso
4. Architettura logica
5. Architettura fisica
6. Componenti software
7. Database
8. API REST
9. Frontend
10. Scheduler
11. Provider finanziari
12. Sicurezza
13. Logging
14. Deployment
15. Roadmap
16. Convenzioni di sviluppo
17. Test
18. Possibili evoluzioni
1 Visione
                Quantica Platform

                     Docker

     +--------------------------------------+

           PostgreSQL
                │
     +----------+-----------+

 Trading Lab   Gmail   NAS Tools   AI


Trading Lab è soltanto una delle applicazioni della piattaforma.

2 Architettura
Browser
    │
    ▼
FastAPI
    │
    ▼
Application Services
    │
    ├──────────────┐
    ▼              ▼
Database       Finnhub
3 Componenti
backend/

    apps/

        trading_lab/

            api/
            services/
            providers/
            models/
            repositories/
            schemas/
            jobs/
            utils/
            config/
            tests/

Questa suddivisione è molto più scalabile della classica struttura app/.

4 Database
PostgreSQL

quantica
│
├── trading_db
│
├── gmail_db
│
├── nas_db
│
└── ai_db

Ogni applicazione possiede:

database
utente
permessi

indipendenti.

5 Tabelle iniziali
symbols
--------

id
ticker
market
exchange
currency
active
created_at


history_daily
-------------

symbol_id
date
open
high
low
close
volume


history_intraday

news

fundamentals

jobs

logs

configuration
6 API
GET /health

GET /symbols

POST /symbols

DELETE /symbols/{id}

GET /history/{ticker}

POST /download/{ticker}

GET /news/{ticker}

GET /status
7 Provider Layer

Questa parte è fondamentale.

Trading Service

        │

        ▼

Provider Interface

        │

 ┌──────┴─────────┐

Finnhub     AlphaVantage

Yahoo       Polygon

IBKR        TwelveData

L'applicazione non deve sapere chi fornisce i dati.

Chiama solamente un'interfaccia.

Questo permetterà un giorno di cambiare provider con pochissimo codice.

8 Scheduler

Componenti previsti

Download Scheduler

Market Open Scheduler

News Scheduler

Portfolio Scheduler

Cleanup Scheduler
9 Cache
Browser

↓

FastAPI

↓

Cache PostgreSQL

↓

Finnhub

Se il dato è già presente nel database non viene effettuata alcuna chiamata esterna.

10 Frontend

Prima versione

Dashboard

Watchlist

Ticker Search

Download

History

Logs

Seconda versione

Candlestick

Indicatori

Portafoglio

Backtest

News

Alert
11 Logging
Application Log

API Log

Scheduler Log

Provider Log

Security Log
12 Sicurezza
API Key nel .env
password nel .env
nessuna credenziale su Git
utenti PostgreSQL separati
ogni app vede soltanto il proprio database
13 Roadmap
Fase 1

✔ Infrastruttura Quantica

Fase 2

✔ Docker

✔ PostgreSQL

✔ FastAPI

Fase 3

Ticker Search

Fase 4

Download storico

Fase 5

Grafici

Fase 6

Indicatori

Fase 7

Backtesting

Fase 8

Portfolio

Fase 9

AI Assistant

Fase 10

Trading Simulator