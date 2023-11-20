import streamlit as st
import requests
from streamlit import session_state
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Realizar la conexión a google sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive.file"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de Google Sheets
hoja = client.open("Usuarios_bd").get_worksheet(1)


# Configura el título y el favicon de la página
st.set_page_config(
    page_title="Gamer's Companion",
    page_icon="https://i.imgur.com/HaQOhdz.png",
)

# Título de la aplicación
url_title = "https://i.imgur.com/kpJuEpB.png"
st.markdown(f'<img src="{url_title}" alt="Encabezado" style="width: 100%;">',
            unsafe_allow_html=True)

data = hoja.get_all_values()
comentarios = pd.DataFrame(data[1:], columns=data[0])

if st.session_state['logged_in']:

    game_name = st.text_input("Ingresa el nombre del juego")

    if game_name:

        comentarios_2 = comentarios[comentarios['Juego'] == game_name][['Comentario', 'Correo']]
        st.table(comentarios_2)
else:
     st.error("Para buscar comentarios debes iniciar sesión")
