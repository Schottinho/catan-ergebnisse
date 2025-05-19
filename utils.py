import pandas as pd
import os

SPIELER = ["Sotirios", "Kosta", "Simon", "Michael"]

def lade_daten(pfad):
    if not os.path.exists(pfad):
        df = pd.DataFrame(columns=["Datum"] + SPIELER)
        df.to_csv(pfad, sep=";", index=False)
    df = pd.read_csv(pfad, sep=";", encoding="utf-8")
    df[SPIELER] = df[SPIELER].apply(pd.to_numeric, errors="coerce")
    return df

def berechne_sieger_und_zahlungen(df):
    df = df.copy()
    df["Sieger"] = df[SPIELER].idxmax(axis=1)
    for s in SPIELER:
        df[f"€ {s}"] = 0.0

    for idx, row in df.iterrows():
        teilnehmer = [s for s in SPIELER if row[s] > 0]
        sieger = row["Sieger"]
        for s in teilnehmer:
            if s == sieger:
                df.at[idx, f"€ {s}"] = 0.0
            elif row[s] < 9:
                df.at[idx, f"€ {s}"] = 2.0
            else:
                df.at[idx, f"€ {s}"] = 1.0

    df["€ Summe"] = df[[f"€ {s}" for s in SPIELER]].sum(axis=1)
    return df

def neues_spiel_hinzufuegen(df, datum, punkte):
    neuer_eintrag = {"Datum": datum.strftime("%Y-%m-%d"), **punkte}
    df = pd.concat([df, pd.DataFrame([neuer_eintrag])], ignore_index=True)
    return df

def speichere_daten(pfad, df):
    df.to_csv(pfad, sep=";", index=False)

def berechne_statistik(df):
    stats = []
    for s in SPIELER:
        spiele = df[df[s] > 0].shape[0]
        siege = df["Sieger"].eq(s).sum()
        euro = df[f"€ {s}"].sum()
        punkte = df[s].sum()
        stats.append({
            "Name": s, "Spiele": spiele, "Siege": siege,
            "Total €": round(euro, 2), "d-Punkte": punkte
        })
    return pd.DataFrame(stats)

def loesche_spiel(df, index):
    return df.drop(index=index).reset_index(drop=True)
