import streamlit as st
import pandas as pd
import os
from pdf_generator import generate_quote_pdf
from datetime import datetime, timedelta  # <--- AGGIUNGI QUESTO

# Configurazione UI
st.set_page_config(page_title="EasyQuote", layout="wide", page_icon="📝")

# Inizializzazione cartelle di sistema
if not os.path.exists("quotes"):
    os.makedirs("quotes")

st.title("💼 EasyQuote")
st.markdown("Gestione preventivi con ricerca rapida e selezione multipla.")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configurazione")
    file = st.file_uploader("Carica Listino (CSV/XLSX)", type=['csv', 'xlsx'])
    st.info("Il file deve avere le colonne: 'Prodotto' e 'Prezzo'")

    if st.button("🔄 Reset Applicazione"):
        st.clear_cache()
        st.rerun()

if file:
    # Caricamento e pulizia dati
    try:
        df_listino = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        df_listino['Prezzo'] = pd.to_numeric(df_listino['Prezzo'], errors='coerce').fillna(0.0)
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {e}")
        st.stop()

    # --- 1. Selezione Prodotti (Filtri/Chip) ---
    st.subheader("🔍 Selezione Prodotti")
    prodotti_scelti = st.multiselect(
        "Cerca e seleziona i prodotti dal listino:",
        options=df_listino['Prodotto'].unique().tolist(),
        placeholder="Scrivi per filtrare..."
    )

    if prodotti_scelti:
        # Preparazione dati per la griglia
        subset = df_listino[df_listino['Prodotto'].isin(prodotti_scelti)].copy()
        if 'Quantità' not in subset.columns:
            subset['Quantità'] = 1

        # --- 2. Griglia Editabile ---
        st.write("### 🛒 Carrello")
        edited_df = st.data_editor(
            subset[['Prodotto', 'Prezzo', 'Quantità']],
            column_config={
                "Prodotto": st.column_config.TextColumn(disabled=True),
                "Prezzo": st.column_config.NumberColumn("Prezzo (€)", format="%.2f"),
                "Quantità": st.column_config.NumberColumn("Qtà", min_value=1, step=1)
            },
            hide_index=True,
            use_container_width=True,
            key="quote_editor"
        )

        # Calcoli in tempo reale
        edited_df['Subtotale'] = edited_df['Prezzo'] * edited_df['Quantità']
        totale_lordo = edited_df['Subtotale'].sum()

        # --- 3. Dati Cliente, Sconto e IVA ---
        st.divider()
        st.subheader("📋 Parametri Finali")

        c1, c2, c3 = st.columns([2, 1, 1])

        with c1:
            cliente_base = st.text_input("Ragione Sociale Breve (per nome file)", "Cliente_Finale")

        with c2:
            sconto = st.number_input("Sconto (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)

        with c3:
            opzioni_iva = {
                "IVA 22% (Ordinaria)": 22.0,
                "IVA 10% (Ridotta)": 10.0,
                "IVA 4% (Minima)": 4.0,
                "IVA 0% (Esente)": 0.0
            }
            iva_label = st.selectbox("Aliquota IVA", options=list(opzioni_iva.keys()))
            iva_selezionata = opzioni_iva[iva_label]

        with st.expander("📝 Dettagli Intestazione e Pagamento", expanded=True):
            col_mio, col_cli = st.columns(2)
            with col_mio:
                st.subheader("I Tuoi Dati")
                mia_azienda = st.text_area("Tua Azienda (Nome, Indirizzo, P.IVA)",
                                           "Mia Azienda Srl\nVia Roma 1, Milano\nP.IVA 123456789")
                iban = st.text_input("IBAN per pagamento", "IT 00 X 00000 00000 000000000000")

            with col_cli:
                st.subheader("Dati Cliente")
                cliente_full = st.text_area("Dettagli Cliente Completi",
                                            "Spett.le Cliente\nVia Torino 5, Roma\nP.IVA 987654321")
                validita = st.date_input("Valido fino a:", datetime.now() + timedelta(days=30))

        # Calcolo Totali per Anteprima
        valore_sconto = totale_lordo * (sconto / 100)
        imponibile_netto = totale_lordo - valore_sconto
        valore_iva = imponibile_netto * (iva_selezionata / 100)
        totale_finale = imponibile_netto + valore_iva

        # Box Totale Gigante
        st.markdown(
            f"""
                    <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; border-left: 10px solid #FF4B4B; text-align: center; margin-top: 20px;">
                        <p style="color: #FAFAFA; font-size: 20px; font-weight: bold; text-transform: uppercase;">Totale Documento</p>
                        <h1 style="color: #FF4B4B; font-size: 60px; margin: 0;">€ {totale_finale:,.2f}</h1>
                        <p style="color: #888;">Imponibile: € {imponibile_netto:,.2f} | IVA: € {valore_iva:,.2f}</p>
                    </div>
                    """,
            unsafe_allow_html=True
        )

        st.divider()

        # Pulsante Generazione Unico
        if st.button("📄 Genera e Scarica Preventivo PDF", use_container_width=True, type="primary"):
            file_path = f"quotes/Preventivo_{cliente_base.replace(' ', '_')}.pdf"
            try:
                generate_quote_pdf(
                    cliente_full,
                    mia_azienda,
                    iban,
                    validita.strftime('%d/%m/%Y'),
                    edited_df,
                    totale_lordo,
                    sconto,
                    iva_selezionata,
                    file_path
                )
                st.success("✅ PDF Generato con successo!")
                with open(file_path, "rb") as f:
                    st.download_button("📥 Clicca qui per scaricare", f, file_name=os.path.basename(file_path))
            except Exception as e:
                st.error(f"Errore generazione: {e}")