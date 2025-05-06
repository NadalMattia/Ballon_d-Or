#Importare il dataset
import pandas as pd

##Importa il CSV
# Leggi il file CSV in un DataFrame
df = pd.read_csv('ballon-d-or.csv', index_col=0)
# Mostra le prime righe del DataFrame

##Scraping primi 3 posti dal 2018 al 2024
from bs4 import BeautifulSoup
import requests
import time

# Definisco l'URL di base
base_url = "https://it.wikipedia.org/wiki/Pallone_d%27oro_{anno}"

# Lista degli anni
list_years = [2019, 2021, 2022, 2023, 2024]

# Genera gli URL per ogni anno
urls = [base_url.format(anno=anno) for anno in list_years]

# Creo un DataFrame vuoto con colonne specifiche per i giocatori mancanti
df_miss_player = pd.DataFrame(columns=['year', 'rank', 'player', 'team', 'points', 'percentages'])

# Funzione per fare scraping su un singolo URL
def scrape_url_wikipedia(url, year):
    try:
        # Fai una richiesta HTTP al sito web
        response = requests.get(url)
        response.raise_for_status()  # Controlla se la richiesta ha avuto successo
        
        # Analizza il contenuto HTML della pagina
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trova il primo tag tbody
        tbody = soup.find('tbody')
        trs = tbody.find_all('tr')
        
        # Leggi solo le prime 3 righe (escludendo l'intestazione)
        for tr in trs[1:4]:
            td_elements = tr.find_all('td')
            if len(td_elements) >= 5:
                rank = td_elements[0].text.replace('\n', ' ').strip()
                player = td_elements[2].find('a').get('title')
                team = td_elements[4].text.strip()
                points = td_elements[3].text.replace('\n', ' ').strip()
                percentages = 0.0
                # Aggiungi una nuova riga al DataFrame
                df_miss_player.loc[len(df_miss_player)] = [year, rank, player, team, int(points), percentages]
            else:
                print("Errore td_elements")
    
    except Exception as e:
        print(f"Errore con l'URL {url}: {e}")

# Esegui le richieste in sequenza con un ritardo tra le richieste
for year, url in zip(list_years, urls):
    scrape_url_wikipedia(url, year)
    time.sleep(3)  # Aggiungi un ritardo di 3 secondi tra le richieste

# Calcola la percentuale per ogni giocatore raggruppando per annata e arrotonda a due cifre significative
df_miss_player['percentages'] = df_miss_player.groupby('year')['points'].transform(lambda x: (x / x.sum()) * 100)
df_miss_player['percentages'] = df_miss_player['percentages'].round(2)

df_miss_player.at[5, 'player'] = "Jorginho"
df_miss_player.at[12, 'player'] = "Rodri"

# Concateno i dataframe
df = pd.concat([df.reset_index(drop=True), df_miss_player.reset_index(drop=True)], ignore_index=True)

#Creazione lista url per scraping nazionalotà
import unidecode

# Definisco l'URL di base
base_url = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={giocatore}"

# Funzione per sostituire gli spazi con %20
def format_name(name):
    return name.replace(" ", "+")

# Normalizzo i nomi dei giocatori nel DataFrame
df1 = df.copy()
df1['player'] = df1['player'].apply(lambda x: unidecode.unidecode(x).lower())

# Estrai i valori unici dalla colonna
list_player_unique = list(df1['player'].unique())

# Genera gli URL per ogni nome e cognome
urls = [base_url.format(giocatore=format_name(name)) for name in list_player_unique]


# Lista per memorizzare le nazionalità e i ruoli

###

#DA SISTEMARE CON  RUOLI DEI GIOCATORI

###
nationalities = []

# Headers HTTP per simulare un browser reale
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com'
}

# Funzione per fare scraping su un singolo URL
def scrape_url(url):
    try:
        # Fai una richiesta HTTP al sito web con gli headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Controlla se la richiesta ha avuto successo
        
        # Analizza il contenuto HTML della pagina
        soup = BeautifulSoup(response.content, 'html.parser')


        # Trova il primo <tr> con classe 'odd' (esempio di riga di dati)
        tr = soup.find('tr', class_='odd')
        if not tr:
            print("Errore: elemento <tr> con classe 'odd' non trovato")
            return

        # Estrai tutte le celle <td> dalla riga trovata
        tds = tr.find_all('td')
        td_class = tds.find_all('td', class_='zentriert')
        pritn(td_class)

        # Estrazione dei dati
        nationality = tds[4].find('img').get('title') if tds[4].find('img') else None
        position_td = tds[2].find('td', class_='zentriert')
        position = position_td.text.strip() if position_td else None

        # Aggiungi alla lista solo se almeno uno dei due dati è disponibile
        nationalities.append({'nationality': nationality, 'role': position})
        print("Trovato:", nationalities[-1])

    except Exception as e:
        print(f"Errore con l'URL {url}: {e}")
        
# Esegui le richieste in sequenza con un ritardo tra le richieste
for url in urls:
    scrape_url(url)
    time.sleep(2)  # Aggiungi un ritardo di 2 secondo tra le richieste
