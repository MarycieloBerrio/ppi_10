# Importar las librerías necesarias
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

# Autenticación y acceso a Google Sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Leer los datos de Sheet1 (usuarios)
sheet_users = client.open("Usuarios_bd").worksheet("Sheet1")
users_data = pd.DataFrame(sheet_users.get_all_records())

# Leer los datos de Info_Juegos (juegos)
sheet_games = client.open("Usuarios_bd").worksheet("Info_Juegos")
games_data = pd.DataFrame(sheet_games.get_all_records())

# Obtener los IDs de usuario y juego
user_ids = users_data['ID_Usuario']
game_ids = games_data['ID_JUEGO']

# Crear un DataFrame para las calificaciones de los usuarios a los juegos
ratings_data = pd.DataFrame(index=game_ids, columns=user_ids)

# Generar calificaciones aleatorias para los usuarios a los juegos
for user_id in user_ids:
    if user_id == 0:
        # Generar un usuario que califique con 1 todos los juegos
        ratings_data[user_id] = np.random.randint(1, 2, size=len(game_ids))
    elif user_id == 1:
        # Generar un usuario que califique con 2 todos los juegos
        ratings_data[user_id] = np.random.randint(2, 3, size=len(game_ids))

    elif user_id == 2:
        # Generar un usuario que califique con 3 todos los juegos
        ratings_data[user_id] = np.random.randint(3, 4, size=len(game_ids))
    elif user_id == 3:
        # Generar un usuario que califique con 4 todos los juegos
        ratings_data[user_id] = np.random.randint(4, 5, size=len(game_ids))
    elif user_id == 4:
        # Generar un usuario que califique con 5 todos los juegos
        ratings_data[user_id] = np.random.randint(5, 6, size=len(game_ids))
    elif user_id == 5:
        # Generar un usuario que califique entre 1 y 2 todos los juegos
        ratings_data[user_id] = np.random.randint(1, 3, size=len(game_ids))
    elif user_id == 6:
        # Generar un usuario que califique entre 2 y 3 todos los juegos
        ratings_data[user_id] = np.random.randint(2, 4, size=len(game_ids))
    elif user_id == 7:
        # Generar un usuario que califique entre 3 y 4 todos los juegos
        ratings_data[user_id] = np.random.randint(3, 5, size=len(game_ids))
    elif user_id == 8:
        # Generar un usuario que califique entre 4 y 5 todos los juegos
        ratings_data[user_id] = np.random.randint(4, 6, size=len(game_ids))
    else:
        # Generar usuarios que califiquen entre 1 y 5 todos los juegos
        ratings_data[user_id] = np.random.randint(1, 6, size=len(game_ids))

# Subir los datos a una nueva hoja de Google Sheets con los ID de usuario como columnas y ID de juego como índices
new_worksheet = client.open("Usuarios_bd").add_worksheet("Usuarios_rating",
                                                          rows=len(ratings_data.index) + 1,
                                                          cols=len(ratings_data.columns))

# Actualizar la hoja con los datos del DataFrame transpuesto
new_worksheet.update([ratings_data.index.values.tolist()] + ratings_data.values.T.tolist())
