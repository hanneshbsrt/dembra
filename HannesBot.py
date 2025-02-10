import pandas as pd
import streamlit as st
from fpdf import FPDF

def csv_to_pdf(df, output_file):
    # Auftragsmenge in numerischen Wert umwandeln
    df["Auftragsmenge"] = df["Auftragsmenge"].astype(str).str.replace(",", ".").astype(float)
    
    # Artikel zusammenfassen inkl. Einheit
    summary = df.groupby(["Pos-Bezeichnung", "Einheit"], as_index=False)["Auftragsmenge"].sum()
    
    # PDF erstellen
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Kommissionierübersicht", ln=True, align="C")
    pdf.ln(10)
    
    # Tabellenkopf
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(100, 10, "Artikel", border=1)
    pdf.cell(40, 10, "Menge", border=1)
    pdf.cell(40, 10, "Einheit", border=1, ln=True)
    
    # Tabellendaten
    pdf.set_font("Arial", size=10)
    for index, row in summary.iterrows():
        pdf.cell(100, 10, row["Pos-Bezeichnung"], border=1)
        pdf.cell(40, 10, str(row["Auftragsmenge"]), border=1)
        pdf.cell(40, 10, row["Einheit"], border=1, ln=True)
    
    # PDF speichern
    pdf.output(output_file)
    return output_file

# Streamlit App
st.title("Offene Belege zu Kommissionierschein")
uploaded_file = st.file_uploader("Lade eine CSV-Datei hoch", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";", encoding="utf-16", skiprows=1)
    pdf_file = "Kommissionierübersicht.pdf"
    csv_to_pdf(df, pdf_file)
    
    with open(pdf_file, "rb") as file:
        st.download_button("Download PDF", file, file_name=pdf_file, mime="application/pdf")
