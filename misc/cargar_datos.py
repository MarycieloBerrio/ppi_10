"""
Este módulo genera votos aleatorios por parte de usuarios falsos. Además
carga datos aleatorios desde el local, usando un Dataframe de pandas que 
contiene información sobre videojuegos, hasta la base de datos
en googlesheets.
"""
# Importar las librerías necesarias
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pandas as pd

# Se establece la URL con los datos de los videojuegos
RUTA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjgWQ8jWpgtMLjkxOfOfRN\
DrHzTNS-dSINU5zcfWZTvkYnU07ezFGlBdkJoWjp805NbecrQmSQrjfR/pub?output=xlsx"

# Se carga los datos
dataset = pd.read_excel(RUTA)

# Obtenemos la columna de interés
dataset = dataset["Nombre"]

# Crear una lista de videojuegos
videojuegos = dataset.shape[0]

# TODO: Hacer la generación con ID's númericos
# Generar usuarios aleatorios con IDs únicos
NUM_USUARIOS = 13
usuarios = ["Usuario_" + str(i) for i in range(NUM_USUARIOS)]

# Crear un DataFrame para los votos de los usuarios
data = pd.DataFrame(index=dataset)

# Generar votos aleatorios para los usuarios y agregarlos directamente al DataFrame de data
for usuario in usuarios:
    if usuario == "Usuario_0":
        # Generar un usuario que vote 1 en todos los videojuegos
        data[usuario] = np.random.randint(1, 2, size=videojuegos)
    elif usuario == "Usuario_1":
        # Generar un usuario que vote 2 en todos los videojuegos
        data[usuario] = np.random.randint(2, 3, size=videojuegos)
    elif usuario == "Usuario_2":
        # Generar un usuario que vote 3 en todos los videojuegos
        data[usuario] = np.random.randint(3, 4, size=videojuegos)
    elif usuario == "Usuario_3":
        # Generar un usuario que vote 4 en todos los videojuegos
        data[usuario] = np.random.randint(4, 5, size=videojuegos)
    elif usuario == "Usuario_4":
        # Generar un usuario que vote 5 en todos los videojuegos
        data[usuario] = np.random.randint(5, 6, size=videojuegos)
    elif usuario == "Usuario_5":
        # Generar un usuario que vote entre 1 y 2
        data[usuario] = np.random.randint(1, 3, size=videojuegos)
    elif usuario == "Usuario_6":
        # Generar un usuario que vote entre 2 y 3
        data[usuario] = np.random.randint(2, 4, size=videojuegos)
    elif usuario == "Usuario_7":
        # Generar un usuario que vote entre 3 y 4
        data[usuario] = np.random.randint(3, 5, size=videojuegos)
    elif usuario == "Usuario_8":
        # Generar un usuario que vote entre 4 y 5
        data[usuario] = np.random.randint(4, 6, size=videojuegos)
    else:
        # Generar usuarios que voten en un rango entre 1 y 5
        data[usuario] = np.random.randint(1, 6, size=videojuegos)

# Realizar la conexión a google sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive.file"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de Google Sheets
hoja_google = client.open("Usuarios_bd")

# Nombre de la nueva hoja
NUEVA_HOJA_NOMBRE = "Usuarios_rating"

# Crear una nueva hoja en la hoja de Google Sheets
nueva_hoja = hoja_google.add_worksheet(title=NUEVA_HOJA_NOMBRE, rows=1, cols=1)

# Actualizar la hoja con los datos del Dataframe
nueva_hoja.update([data.columns.values.tolist()] + data.values.tolist())

print(f"DataFrame guardado en la nueva hoja de Google Sheets: {NUEVA_HOJA_NOMBRE}")
