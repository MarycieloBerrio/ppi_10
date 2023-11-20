"""
Este modulo contiene las funciones para calcular la similitud entre
usuarios y entre juegos con la distancia del coseno.
Además, la función generar recomendaciones para juegos, donde se
utiliza la similitud entre juegos para obtener los 
datos de los juegos más parecidos entre si.

Ejemplo de uso del módulo:

df_ratings = cargar_datos_google_sheets()
user_id = 0  ID de usuario para el ejemplo

sim_users = calcular_similitud_usuarios(df_ratings, user_id)
sim_games = calcular_similitud_juegos(df_ratings, user_id)
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

    df = pd.DataFrame(data)
    return df

def calcular_similitud_usuarios(df, user_id):
    """
    Calcula la similitud entre el usuario dado (user_id)
    y otros usuarios en el DataFrame.

    Args:
    df (pd.DataFrame): DataFrame que contiene los datos de los usuarios
                       y sus ratings.
    user_id (int): El ID del usuario para el cual se calculará la similitud.

    Returns:
    list: Lista de IDs de los 10 usuarios más
          similares al usuario dado (user_id).
    """
    # Filtra las filas del DataFrame donde el
    # ID_USUARIO es igual al ID proporcionado
    user_ratings = df[df['ID_USUARIO'] == user_id].iloc[:, 1:].values

    # Filtra las filas del DataFrame donde el
    # ID_USUARIO no es igual al ID proporcionado
    all_user_ratings = df[df['ID_USUARIO'] != user_id].iloc[:, 1:].values

    # Inicializa una lista para almacenar las puntuaciones de similitud
    similarity_scores = []

    # Calcula la similitud del coseno entre el usuario dado y otros usuarios
    for other_user_ratings in all_user_ratings:
        # Calcula la similitud del coseno entre las puntuaciones
        # del usuario y otros usuarios
        score = 1 - cosine(user_ratings, other_user_ratings)
        similarity_scores.append(score)

    # Obtiene los índices de los usuarios más
    #  similares al usuario dado (user_id)
    top_similar_users_indices = np.argsort(similarity_scores)[-10:][::-1]
    return list(df[df['ID_USUARIO'] != user_id].\
           iloc[top_similar_users_indices]['ID_USUARIO'])

def calcular_similitud_juegos(df, user_id):
    """
    Calcula los juegos más similares a las preferencias de un
    usuario en función de la similitud del coseno.

    Args:
    df (pd.DataFrame): DataFrame que contiene los datos de calificaciones
                       de los usuarios por juego.
    user_id (int): ID del usuario para el cual se buscan juegos similares.

    Returns:
    list: Lista de los nombres de los 10 juegos más similares a las
          preferencias del usuario dado.
    """
    # Extrae las puntuaciones de un usuario en particular
    user_ratings = df[df['ID_USUARIO'] == user_id].iloc[:, 1:].values[0]

    # Obtiene todas las puntuaciones de los juegos para todos los usuarios,
    # excluyendo la columna de ID_USUARIO
    all_game_ratings = df.drop(columns=['ID_USUARIO']).values

    # Inicializa una lista para almacenar las puntuaciones de similitud
    similarity_scores = []

    # Calcula la similitud del coseno entre las puntuaciones de un usuario y
    #  todas las puntuaciones de juegos
    for game_ratings in all_game_ratings:
        # Calcula la similitud del coseno entre las puntuaciones del usuario
        #  y las puntuaciones de cada juego
        score = 1 - cosine(user_ratings, game_ratings)
        similarity_scores.append(score)

    # Obtiene los índices de los juegos más similares a
    # las preferencias del usuario dado (user_id)
    top_similar_games_indices = np.argsort(similarity_scores)[-10:][::-1]

    # Obtiene los nombres de los juegos más similares
    # a las preferencias del usuario
    return list(df.drop(columns=['ID_USUARIO']).\
                columns[top_similar_games_indices])
