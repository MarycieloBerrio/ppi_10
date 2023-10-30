"""
Módulo con todo lo pertinente al registro de usuarios.
Se utiliza la API de googlesheets como backend.
"""
# Importación de librería estándar de python
from datetime import datetime

# Importar las librerías necesarias
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Realizar la conexión a google sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive.file"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de Google Sheets
hoja = client.open("Usuarios_bd").sheet1

# Página de streamlit
st.title("Formulario de Registro")

# Establecer un mínimo para la fecha
MIN_FECHA_NAC = datetime(1940, 1, 1)
# Datos personales
nombre = st.text_input("Nombre")
apellido = st.text_input("Apellido")
fecha_nacimiento = st.date_input("Fecha de Nacimiento",
                                  min_value= MIN_FECHA_NAC)
genero = st.selectbox("Género", ["Femenino", "Masculino",
                                  "Prefiero no decirlo"])
videojuego_preferido = st.selectbox("Género de Videojuego Preferido",
                                     ["Estrategia", "Acción", "Sci-fi",
                                       "Misterio", "Horror", "Aventura"])

# Datos de acceso
correo = st.text_input("Correo")
contrasena = st.text_input("Contraseña", type="password")

# Agregar una variable de verificación
usuario_existente = False

if st.button("Registrar"):
    # Verificar si el correo ya existe en la hoja de Google Sheets
    valores = hoja.col_values(6)

    if correo in valores:
        usuario_existente = True
        st.error("El usuario ya se encuentra registrado.")
    else:
        # Crear un diccionario con los datos del usuario
        usuario = {
            "Nombre": nombre,
            "Apellido": apellido,
            "Fecha de Nacimiento": fecha_nacimiento.strftime("%Y-%m-%d"),
            "Género": genero,
            "Género de videojuego preferido": videojuego_preferido,
            "Correo": correo,
            "Contraseña": contrasena
        }

        # Añadir una fila a la hoja de Google Sheets y registrar al usuario
        nueva_fila = [usuario["Nombre"], usuario["Apellido"], usuario["Fecha de Nacimiento"],
                      usuario["Género"], usuario["Género de videojuego preferido"],
                      usuario["Correo"], usuario["Contraseña"]]
        hoja.append_row(nueva_fila)
        st.success("¡Registro exitoso!")