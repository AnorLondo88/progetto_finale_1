import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#Parte 1 – Dataset di base-------------------------------------------------------------------------

# seed per avere sempre gli stessi numeri (così non cambia tutto ogni volta)
np.random.seed(42)

negozi = ["Milano", "Roma", "Napoli", "Torino", "Bologna"]
prodotti = ["Smartphone", "Laptop", "TV", "Tablet", "Cuffie", "Console"]

prezzi_base = {
    "Smartphone": 499.99,
    "Laptop": 999.99,
    "TV": 699.99,
    "Tablet": 399.99,
    "Cuffie": 79.99,
    "Console": 449.99
}

# creo liste vuote, poi le riempio riga per riga (stile excel)
lista_date = []
lista_negozi = []
lista_prodotti = []
lista_quantita = []
lista_prezzi = []

# genero 30 righe
for i in range(30):

    # scelgo una data tra 10 giorni
    giorno = np.random.randint(1, 11)  # 1..10
    data = f"2023-09-{giorno:02d}"     # formatto tipo 2023-09-01

    # scelgo negozio e prodotto a caso
    negozio = np.random.choice(negozi)
    prodotto = np.random.choice(prodotti)

    # quantita tra 1 e 10
    quantita = np.random.randint(1, 11)

    # prezzo con piccola variazione (tipo sconti)
    prezzo_unit = prezzi_base[prodotto]
    prezzo_unit = prezzo_unit * np.random.uniform(0.9, 1.1)
    prezzo_unit = round(prezzo_unit, 2)

    # aggiungo alle liste
    lista_date.append(data)
    lista_negozi.append(negozio)
    lista_prodotti.append(prodotto)
    lista_quantita.append(quantita)
    lista_prezzi.append(prezzo_unit)

# creo il dizionario (colonne)
dati = {
    "Data": lista_date,
    "Negozio": lista_negozi,
    "Prodotto": lista_prodotti,
    "Quantità": lista_quantita,
    "Prezzo_unitario": lista_prezzi
}

# creo il dataframe
df_creato = pd.DataFrame(dati)

# salvo il csv
df_creato.to_csv("vendite.csv", index=False)
print("Ho creato vendite.csv")    

print(os.getcwd())

#Parte 2 – Importazione con Pandas----------------------------------------------------------------

df = pd.read_csv("vendite.csv")

print("\nPrime 5 righe:")
print(df.head())

print("\nShape (righe, colonne):")
print(df.shape)

print("\nInfo:")
print(df.info())

# converto data in datetime per fare groupby giornaliero bene
df["Data"] = pd.to_datetime(df["Data"])

#Parte 3 – Elaborazioni con Pandas-------------------------------------------------------------------

# colonna incasso
df["Incasso"] = df["Quantità"] * df["Prezzo_unitario"]

# incasso totale catena
incasso_totale = df["Incasso"].sum()
print("\nIncasso totale catena:", round(incasso_totale, 2))

# incasso medio per negozio
incasso_medio_negozio = df.groupby("Negozio")["Incasso"].mean()
print("\nIncasso medio per negozio:")
print(incasso_medio_negozio.round(2))

# top 3 prodotti più venduti per quantità totale
quantita_per_prodotto = df.groupby("Prodotto")["Quantità"].sum()
top3 = quantita_per_prodotto.sort_values(ascending=False).head(3)
print("\nTop 3 prodotti più venduti (quantità):")
print(top3)

# incasso medio per negozio e prodotto
incasso_medio_np = df.groupby(["Negozio", "Prodotto"])["Incasso"].mean()
print("\nIncasso medio per Negozio + Prodotto:")
print(incasso_medio_np.round(2))

#Parte 4 – Uso di NumPy

q = df["Quantità"].to_numpy()

media = np.mean(q)
minimo = np.min(q)
massimo = np.max(q)
dev_std = np.std(q)

percentuale_sopra_media = np.mean(q > media) * 100

print("\nNUMPY Quantità:")
print("media:", round(media, 2))
print("min:", minimo)
print("max:", massimo)
print("dev std:", round(dev_std, 2))
print("% sopra media:", round(percentuale_sopra_media, 2))

# array 2D (Quantità, Prezzo_unitario) e calcolo incasso
arr = df[["Quantità", "Prezzo_unitario"]].to_numpy()
incasso_numpy = arr[:, 0] * arr[:, 1]

# confronto con incasso del dataframe
incasso_df = df["Incasso"].to_numpy()
differenza = np.abs(incasso_numpy - incasso_df)

print("\nConfronto incasso NumPy vs df:")
print("max differenza:", differenza.max())

#Parte 5 – Visualizzazioni con Matplotlib


# barre: incasso totale per negozio
incasso_negozio = df.groupby("Negozio")["Incasso"].sum()

plt.figure()
plt.bar(incasso_negozio.index, incasso_negozio.values)
plt.title("Incasso totale per negozio")
plt.xlabel("Negozio")
plt.ylabel("Incasso (€)")
plt.show()

# torta: percentuale incassi per prodotto (non quantità)
incasso_prodotto = df.groupby("Prodotto")["Incasso"].sum()

plt.figure()
plt.pie(incasso_prodotto.values, labels=incasso_prodotto.index, autopct="%1.1f%%")
plt.title("Percentuale incassi per prodotto")
plt.show()

# linea: andamento giornaliero incassi (totale catena)
incasso_giorno = df.groupby("Data")["Incasso"].sum().sort_index()

plt.figure()
plt.plot(incasso_giorno.index, incasso_giorno.values, marker="o")
plt.title("Andamento giornaliero incassi (catena)")
plt.xlabel("Data")
plt.ylabel("Incasso (€)")
plt.xticks(rotation=45)
plt.show()

#Parte 6 – Analisi Avanzata

categoria = {
    "Smartphone": "Informatica",
    "Laptop": "Informatica",
    "Tablet": "Informatica",
    "TV": "Elettrodomestici",
    "Cuffie": "Accessori",
    "Console": "Gaming"
}

df["Categoria"] = df["Prodotto"].map(categoria)

incasso_categoria = df.groupby("Categoria")["Incasso"].sum()
quantita_media_categoria = df.groupby("Categoria")["Quantità"].mean()

print("\nIncasso totale per categoria:")
print(incasso_categoria.round(2))

print("\nQuantità media per categoria:")
print(quantita_media_categoria.round(2))

df.to_csv("vendite_analizzate.csv", index=False)
print("\nSalvato vendite_analizzate.csv")

#Parte 7 – Estensioni (per i più bravi)------------------------------------------------------------

# grafico combinato: barre (incasso medio) + linea (quantità media)
incasso_medio_cat = df.groupby("Categoria")["Incasso"].mean()
quantita_media_cat = df.groupby("Categoria")["Quantità"].mean()

categorie = incasso_medio_cat.index

fig, ax1 = plt.subplots()
ax1.bar(categorie, incasso_medio_cat.values)
ax1.set_xlabel("Categoria")
ax1.set_ylabel("Incasso medio (€)")
ax1.set_title("Incasso medio + Quantità media per categoria")

ax2 = ax1.twinx()
ax2.plot(categorie, quantita_media_cat.loc[categorie].values, marker="o")
ax2.set_ylabel("Quantità media")

plt.show()

# funzione top_n_prodotti(n) per incasso totale
def top_n_prodotti(n):
    incasso_tot_prodotto = df.groupby("Prodotto")["Incasso"].sum()
    incasso_tot_prodotto = incasso_tot_prodotto.sort_values(ascending=False)
    return incasso_tot_prodotto.head(n)

print("\nTop prodotti per incasso:")
print(top_n_prodotti(3).round(2))