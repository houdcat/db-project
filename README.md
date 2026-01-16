Zde je opravený soubor README.md. Sekci 2. Konfigurace Aplikace jsem upravil tak, aby explicitně vyžadovala přihlášení jménem sa a heslem student.

GameStore
Tato aplikace slouží ke správě digitálního obchodu s hrami. Byla vytvořena jako školní projekt demonstrující práci s relační databází MSSQL, využití návrhového vzoru Repository (D1) a tvorbu desktopového GUI v Pythonu (Tkinter).

Funkcionalita
CRUD operace: Přidání, úprava, mazání a čtení dat pro 5 tabulek (Hry, Uživatelé, Žánry, Recenze, Objednávky).

Transakce: Nákup hry (atomická operace: vytvoření objednávky + stržení kreditu).

Import: Hromadné nahrávání dat z formátů JSON a CSV.

Reporting: Generování souhrnného přehledu aktivity uživatelů.

Validace: Ošetření vstupů (např. záporná cena, neplatný rating).

Technologie
Jazyk: Python 3.x

GUI: Tkinter

Databáze: Microsoft SQL Server (MSSQL)

Knihovny: pyodbc

Adresářová struktura
Plaintext
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
Instalace a Spuštění
1. Příprava Databáze
Ujistěte se, že máte nainstalovaný MSSQL Server.

Otevřete SQL Management Studio (SSMS).

Vytvořte novou databázi s názvem GameStoreDB.

Otevřete soubor sql/import.sql a spusťte jej nad touto databází.

2. Konfigurace Aplikace
Otevřete soubor config.ini v kořenové složce projektu.

Upravte sekci [DATABASE]. Musíte zadat název školního serveru a použít přihlašovací údaje sa / student.

Příklad správného nastavení:

Ini, TOML
[DATABASE]
Driver={ODBC Driver 17 for SQL Server}
Server=NAZEV_SKOLNIHO_SERVERU
Database=GameStoreDB
User=sa
Password=student
; Trusted_Connection=yes ; (Nechte zakomentované, nepoužíváme Windows Auth)
3. Instalace Python knihoven
Otevřete příkazovou řádku (CMD/Terminal) ve složce projektu a spusťte:

Bash
pip install -r requirements.txt
(Pokud soubor requirements.txt nemáte, stačí: pip install pyodbc)

4. Spuštění
V příkazové řádce přejděte do složky src a spusťte aplikaci:

Bash
cd src
python main.py
Poznámky pro testera
Výchozí Admin účet: Uživatel Admin (vytvořen SQL skriptem), počáteční kredit 9999.

Importy: Testovací soubory pro import naleznete ve složce data/.
