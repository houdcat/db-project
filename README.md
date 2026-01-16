# GameStore

Tato aplikace slouží ke správě digitálního obchodu s hrami. Byla vytvořena jako školní projekt demonstrující práci s relační databází MSSQL, využití návrhového vzoru Repository (D1) a tvorbu desktopového GUI v Pythonu (Tkinter).

## Funkcionalita
- **CRUD operace:** Přidání, úprava, mazání a čtení dat pro 5 tabulek (Hry, Uživatelé, Žánry, Recenze, Objednávky).
- **Transakce:** Nákup hry (atomická operace: vytvoření objednávky + stržení kreditu).
- **Import:** Hromadné nahrávání dat z formátů JSON a CSV.
- **Reporting:** Generování souhrnného přehledu aktivity uživatelů.
- **Validace:** Ošetření vstupů (např. záporná cena, neplatný rating).

## Technologie
- **Jazyk:** Python 3.x
- **GUI:** Tkinter
- **Databáze:** Microsoft SQL Server (MSSQL)
- **Knihovny:** `pyodbc`

## Adresářová struktura
```text
GameStore/
│
├── config.ini           # Konfigurace připojení k DB
├── requirements.txt     # Seznam závislostí
├── README.md            # Tento soubor
│
├── src/                 # Zdrojové kódy
│   ├── main.py          # Hlavní spouštěcí soubor (GUI)
│   ├── database.py      # Database connection singleton
│   ├── repositories.py  # D1 Pattern (SQL logika)
│   ├── services.py      # Logika importů
│   └── models.py        # (Volitelné) Datové třídy
│
├── sql/                 # SQL skripty
│   └── import.sql       # Skript pro vytvoření tabulek a dat
│
├── data/                # Testovací data pro import (CSV, JSON)
├── doc/                 # Dokumentace projektu
└── test/                # Testovací scénáře
