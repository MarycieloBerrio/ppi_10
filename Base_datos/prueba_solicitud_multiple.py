import requests
import pandas as pd

# URL de la API de IGDB

URL = "https://api.igdb.com/v4/games"

# Headers de la solicitud

HEADERS = {
    "Client-ID": "ju1vfy05jqstzoclqv1cs2hsomw1au",
    "Authorization": "Bearer 8h1ymcezojqdpcvmz5fvwxal2myoxp",
    
}


BODY = 'fields id,name,summary,cover.url,involved_companies.company.name,total_rating;\
      limit 150; sort total_rating desc; where total_rating > 50 & total_rating_count > 500;'

response = requests.post(URL, headers=HEADERS, data=BODY)
data = response.json()

# Procesamiento de los datos obtenidos de la API IGDB
if data:
    # Crear un DataFrame con los datos obtenidos
    df = pd.DataFrame(data)

    # Eliminar juegos duplicados por nombre
    df.drop_duplicates(subset='name', inplace=True)

    # Filtrar juegos sin URL de imagen
    df = df[df['cover'].notnull()]

    # Seleccionar las columnas necesarias
    selected_columns = ['id', 'name', 'summary', 'involved_companies', 'total_rating', 'cover']
    df = df[selected_columns]

    # Convertir la columna 'involved_companies' a una lista de nombres de empresas
    df['involved_companies'] = df['involved_companies'].apply(lambda x: x[0]['company']['name'] if x else None)

    # Guardar los datos en un archivo CSV
    df.to_csv('juegos.csv', index=False)

