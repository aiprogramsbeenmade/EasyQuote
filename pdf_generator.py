from fpdf import FPDF
from datetime import datetime
import os

class PDFQuote(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        font_path = "assets/DejaVuSans.ttf"
        font_bold_path = "assets/DejaVuSans-Bold.ttf"

        if os.path.exists(font_path) and os.path.exists(font_bold_path):
            self.add_font("DejaVu", style="", fname=font_path)
            self.add_font("DejaVu", style="B", fname=font_bold_path)
            self.main_font = "DejaVu"
        else:
            self.main_font = "Helvetica"

    def header(self):
        logo = "assets/logo.png"
        if os.path.exists(logo):
            self.image(logo, 10, 8, 30)
            self.ln(10)
        self.set_font(self.main_font, "B", 16)
        self.cell(0, 10, "PREVENTIVO COMMERCIALE", ln=True, align="C")
        self.set_font(self.main_font, "", 9)
        self.cell(0, 5, f"Data emissione: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.main_font, "", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


def generate_quote_pdf(client_info, my_info, iban, valid_until, df_items, total_raw, discount_perc, iva_perc,
                       output_path):
    pdf = PDFQuote()
    pdf.add_page()
    f = pdf.main_font

    # --- INTESTAZIONE ALTA ---
    pdf.set_font(f, "B", 12)
    pdf.cell(100, 6, "DA:", ln=0)
    pdf.cell(0, 6, f"DATA: {datetime.now().strftime('%d/%m/%Y')}", ln=1, align="R")

    pdf.set_font(f, "", 10)
    # Usiamo multi_cell per gli indirizzi che hanno più righe
    pdf.multi_cell(100, 5, my_info)

    pdf.set_y(pdf.get_y() - 15)  # Torna su per allineare la scadenza
    pdf.cell(0, 5, f"VALIDO FINO A: {valid_until}", ln=1, align="R")
    pdf.ln(10)

    # --- BOX CLIENTE ---
    pdf.set_fill_color(230, 230, 250)  # Viola chiarissimo come esempio
    pdf.set_font(f, "B", 10)
    pdf.cell(0, 8, "CLIENTE:", ln=1, fill=True)
    pdf.set_font(f, "", 10)
    pdf.multi_cell(0, 5, client_info)
    pdf.ln(10)

    # --- TABELLA VOCI ---
    pdf.set_fill_color(240, 255, 240)  # Verde chiarissimo
    pdf.set_font(f, "B", 9)
    # Intestazioni come nel tuo esempio
    pdf.cell(70, 10, "VOCI/SERVIZI", 1, 0, "C", True)
    pdf.cell(25, 10, "QUANTITÀ", 1, 0, "C", True)
    pdf.cell(30, 10, "PREZZO", 1, 0, "C", True)
    pdf.cell(35, 10, "SUBTOTALE", 1, 0, "C", True)
    pdf.cell(30, 10, "IVA", 1, 1, "C", True)

    pdf.set_font(f, "", 9)
    for _, row in df_items.iterrows():
        pdf.cell(70, 8, str(row['Prodotto']), 1)
        pdf.cell(25, 8, str(int(row['Quantità'])), 1, 0, "C")
        pdf.cell(30, 8, f"{row['Prezzo']:.2f}", 1, 0, "R")
        pdf.cell(35, 8, f"{row['Subtotale']:.2f}", 1, 0, "R")
        pdf.cell(30, 8, f"{iva_perc}%", 1, 1, "C")

    # --- RIEPILOGO FINALE (Ottimizzato per grandi cifre) ---
    pdf.ln(10)
    sconto_v = total_raw * (discount_perc / 100)
    imp_netto = total_raw - sconto_v
    iva_v = imp_netto * (iva_perc / 100)
    totale_ivato = imp_netto + iva_v

    # Allarghiamo la colonna dei valori per evitare sovrapposizioni
    col_etichetta = 135
    col_valore = 55

    pdf.set_font(f, "", 10)

    # Subtotale
    pdf.cell(col_etichetta, 8, "SUBTOTALE:", 0, 0, "R")
    pdf.cell(col_valore, 8, f"{imp_netto:,.2f} €", 0, 1, "R")

    # IVA
    pdf.cell(col_etichetta, 8, f"IVA ({iva_perc}%):", 0, 0, "R")
    pdf.cell(col_valore, 8, f"{iva_v:,.2f} €", 0, 1, "R")

    pdf.ln(2)

    # Totale Finale - Aumentiamo il font e lo spazio
    pdf.set_font(f, "B", 14)
    pdf.set_text_color(46, 204, 113)  # Il verde professionale che ti piaceva

    pdf.cell(col_etichetta, 12, "TOTALE:", 0, 0, "R")
    pdf.cell(col_valore, 12, f"{totale_ivato:,.2f} €", 0, 1, "R")

    # Reset colore testo
    pdf.set_text_color(0, 0, 0)

    # --- PIÈ DI PAGINA (Banca) ---
    pdf.set_y(-40)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font(f, "B", 8)
    pdf.multi_cell(0, 4, f"Coordinate Bancarie:\nIBAN: {iban}")

    pdf.output(output_path)