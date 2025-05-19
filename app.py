import streamlit as st
import pandas as pd
from utils import lade_daten, berechne_sieger_und_zahlungen, neues_spiel_hinzufuegen, speichere_daten, berechne_statistik, loesche_spiel, SPIELER

DATEIPFAD = "daten.csv"
st.set_page_config("Catan Ergebnis", layout="wide")

# Daten laden
df = lade_daten(DATEIPFAD)
df = berechne_sieger_und_zahlungen(df)

# Statistik anzeigen
st.title("📊 Catan Ergebnisdokumentation")
st.subheader("📈 Statistik")
statistik = berechne_statistik(df)
st.dataframe(statistik, use_container_width=True)
st.markdown(f"💰 Gesamtpott: **{df['€ Summe'].sum():.2f} €**")

# Neues Spiel
st.subheader("➕ Neues Spiel")
with st.form("spiel"):
    datum = st.date_input("Datum")
    punkte = {s: st.number_input(f"Punkte {s}", 0, 20, step=1) for s in SPIELER}
    speichern = st.form_submit_button("💾 Speichern")
    if speichern:
        df = neues_spiel_hinzufuegen(df, datum, punkte)
        df = berechne_sieger_und_zahlungen(df)
        speichere_daten(DATEIPFAD, df)
        st.success("Spiel gespeichert.")
        st.rerun()

# Historie mit Löschfunktion
st.subheader("📜 Spiele-Historie")
for i, row in df[::-1].iterrows():
    with st.expander(f"Spiel am {row['Datum']} – Sieger: {row['Sieger']}"):
        st.write({k: row[k] for k in SPIELER})
        st.write({f"€ {k}": row[f"€ {k}"] for k in SPIELER})
        if st.button("❌ Löschen", key=f"del_{i}"):
            df = loesche_spiel(df, i)
            speichere_daten(DATEIPFAD, df)
            st.rerun()
