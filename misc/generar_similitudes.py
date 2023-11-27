"""
Este modulo contiene las funciones para calcular la similitud entre
usuarios y entre juegos con la distancia del coseno.
Además, la función generar recomendaciones para juegos, donde se
utiliza la similitud entre juegos para obtener los 
datos de los juegos más parecidos entre si.
"""

# Importar las liberías requeridas
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine

def cargar_datos_google_sheets():
    """
    Carga los datos desde Google Sheets.

    Lee la hoja "Usuarios_rating" de la base de datos "Usuarios_bd"
    en Google Sheets y devuelve los datos en un DataFrame de pandas.

    Returns:
    pd.DataFrame: Un DataFrame con los datos cargados desde Google Sheets.
    """
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Usuarios_bd").worksheet("Usuarios_rating")
    data = sheet.get_all_records()

    # Asumiendo que la primera fila contiene los encabezados y la primera columna contiene IDs de usuario
    headers = data[0]
    data = data[1:]  # Quitamos la primera fila con encabezados
    df = pd.DataFrame(data, columns=headers)

    # Identificar la columna de ID de usuario correctamente
    df.set_index(df.columns[0], inplace=True)  # Suponiendo que la primera columna es el ID de usuario
    df.index.name = None  # Eliminamos el nombre del índice

    # Eliminar fila y columna duplicadas si existen
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.loc[~df.index.duplicated(keep='first')]

    # Convertir los valores a números si es necesario
    df = df.apply(pd.to_numeric)
    # Convertir los valores de los índices en enteros
    df.index = df.index.astype(int)

    return df


def calcular_similitud_juegos(df):
    """
    Calcula la matriz de similitud entre juegos.

    Args:
    df (pd.DataFrame): DataFrame con los datos de juegos y sus votaciones.

    Returns:
    pd.DataFrame: Matriz de similitud entre los juegos.
    """
    # Duplicar el DataFrame original excluyendo la primera fila y la primera columna
    df_copy = df.iloc[1:, 1:].copy()

    # Convertir los valores a números si es necesario
    df_copy = df_copy.apply(pd.to_numeric)

    # Calcular la matriz de similitud del coseno manualmente
    num_juegos = df_copy.shape[1]
    similarity_matrix = np.zeros((num_juegos, num_juegos))

    for i in range(num_juegos):
        for j in range(num_juegos):
            similarity_matrix[i, j] = 1 - cosine(df_copy.iloc[:, i], df_copy.iloc[:, j])

    # Almacenar los valores de similitud en la copia del DataFrame
    df_similarities = pd.DataFrame(similarity_matrix, index=df_copy.columns, columns=df_copy.columns)
    
    return df_similarities


def encontrar_juegos_similares(matriz_similitud:np.array, id_juego:str) -> list:
    """
    Encuentra los juegos más similares a un juego dado.

    Args:
    matriz_similitud (pd.DataFrame): Matriz de similitud entre juegos.
    id_juego (int): ID del juego para encontrar los juegos similares.

    Returns:
    list or str: Lista de IDs de juegos similares o mensaje si el ID no se encuentra.
    """
    if id_juego in matriz_similitud.index:
        similar_games = matriz_similitud.loc[id_juego].nlargest(11)[1:]  # Excluye el juego original
        return similar_games.index.tolist()
    else:
        return "ID de juego no encontrado"


a = cargar_datos_google_sheets()

