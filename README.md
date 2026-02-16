# 💼 EasyQuote - Generatore di Preventivi Intelligente

**EasyQuote** è un'applicazione web leggera e intuitiva realizzata in Python con **Streamlit**, progettata per aiutare freelance e piccole imprese a generare preventivi professionali in formato PDF in pochi secondi.



## ✨ Funzionalità principali

* **Caricamento Listino**: Supporta file Excel e CSV per importare rapidamente i propri prodotti e prezzi.
* **Selezione Rapida**: Sistema di ricerca e selezione multipla dei prodotti con gestione dinamica delle quantità.
* **Calcoli Automatici**: Gestione immediata di sconti percentuali e diverse aliquote IVA (4%, 10%, 22%).
* **PDF Professionale**: Generazione di documenti PDF pronti all'invio, completi di coordinate bancarie, dati aziendali e scadenze.
* **Anteprima Real-time**: Visualizzazione del totale del documento con impatto grafico elevato prima della generazione.

## 🛠️ Tecnologie utilizzate

* **Python 3.11+**
* **Streamlit**: Per l'interfaccia utente reattiva.
* **FPDF2**: Per la generazione avanzata di documenti PDF con supporto Unicode.
* **Pandas**: Per la manipolazione e il filtraggio dei dati del listino.

## 🚀 Come iniziare

### 1. Clona il repository
```bash
git clone [https://github.com/tuo-username/easyquote.git](https://github.com/tuo-username/easyquote.git)
cd easyquote
```
### 2. Installa le dipendenze
```bash
pip install -r requirements.txt
```
### 3. Avvia l'applicazione
```bash
streamlit run main.py
```

## 📋 Struttura del Listino
Il file CSV o Excel caricato deve contenere almeno le seguenti colonne:
* **Prodotto**: Nome del servizio o oggetto.
* **Prezzo**: Prezzo unitario (numerico).


## 📄 Esempio di Utilizzo
1. Carica il tuo file `.csv` o `.xlsx`.
2. Seleziona i prodotti dal menu a comparsa.
3. Modifica quantità o prezzi nella tabella interattiva se necessario.
4. Inserisci i dati del cliente e l'aliquota IVA desiderata.
5. Clicca su "Genera PDF" per ottenere il documento pronto al download.
