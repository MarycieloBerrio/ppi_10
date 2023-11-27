# Importar las librerías requeridas
import sys
# Agrega la ruta a la carpeta que contiene el script
sys.path.append("misc")
# Importa el script
from generar_similitudes import cargar_datos_google_sheets, calcular_similitud_juegos, encontrar_juegos_similares
import pandas as pd
import streamlit as st
from streamlit import session_state
import gspread
from oauth2client.service_account import ServiceAccountCredentials

 # Configuración de autenticación y acceso a Google Sheets
scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.file"
    ]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
cliente = gspread.authorize(creds)

# Obtener el ID del usuario desde st.session_state
user_id = st.session_state.get('id')

# Verificar si el usuario está logueado
if user_id is not None:
    # Cargar los datos desde Google Sheets
    df = cargar_datos_google_sheets()

    # Crear una copia del DataFrame original
    df_copy = df.copy()

    # Obtener la fila correspondiente al usuario y convertirla en un DataFrame
    user_ratings = df.loc[user_id].astype(int)  # Aseguramos que las calificaciones sean enteros
    
    # Crear un DataFrame con un solo registro (la fila del usuario)
    user_ratings_df = pd.DataFrame([user_ratings.values], columns=user_ratings.index)
    
    # Obtener las calificaciones de los juegos mayores a 3 y dropear los NA
    rated_above_3 = user_ratings_df[user_ratings_df > 3].dropna(axis=1, how='all')

    if not rated_above_3.empty:
        # Obtener el ID del primer juego con calificación mayor a 3
        random_game_id = rated_above_3.columns[1]  # Obtener el primer juego con calificación mayor a 3
        # Generar recomendaciones basadas en ese juego
        matriz_similitud = calcular_similitud_juegos(df)
        recomendaciones = encontrar_juegos_similares(matriz_similitud, random_game_id)

        # Conectar con la hoja de Google Sheets que contiene la información de los juegos
        info_juegos_sheet = cliente.open("Usuarios_bd").worksheet("Info_Juegos")

        # Crear un DataFrame con los datos de la hoja Info_Juegos
        info_juegos_df = pd.DataFrame(info_juegos_sheet.get_all_records())

        # Filtrar los nombres de los juegos basados en los ID recomendados
        nombres_recomendados = info_juegos_df[info_juegos_df['ID_JUEGO'].astype(str).isin(recomendaciones)]['Nombre_Juego']

        if not nombres_recomendados.empty:
            # Mostrar los nombres de los juegos recomendados
            st.write("Juegos Recomendados:")
            for nombre in nombres_recomendados:
                st.write(nombre)
        else:
            st.write("No se encontraron juegos recomendados.")
    else:
        st.write("No hay juegos con calificaciones mayores a 3 en la base de datos.")

else:
    st.write("Inicia sesión para ver recomendaciones.")
