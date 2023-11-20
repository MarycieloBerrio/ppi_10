# Importar las liberías requeridas
import streamlit as st
import pandas as pd
import requests

from streamlit import session_state
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Realizar la conexión a google sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive.file"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de Google Sheets
hoja = client.open("Usuarios_bd").get_worksheet(2)

# Configura el título y el favicon de la página
st.set_page_config(
    page_title="Gamer's Companion",
    page_icon="https://i.imgur.com/HaQOhdz.png",
)

# Configura tu clave API de IGDB
api_key = 'nw5q3ov9xfk9o0vsv1vqicx4xbvjbb'


def get_game_info(game_name):
    """
    Retorna la información de un juego ingresado por el usuario.
    
    Parámetros: 
    -game_name(str): nombre del juego del cual se quiere obtener información.

    -Retorna
    -str: Información del juego.
    -imagen: Imagen de la portada del juego.
    """

    # Define la URL y los encabezados para la solicitud de la API.

    url = 'https://api.igdb.com/v4/games'
    headers = {'Client-ID': 'ju1vfy05jqstzoclqv1cs2hsomw1au', 'Authorization': f'Bearer {api_key}'}


    # Define la consulta para buscar el juego
    body = f'''
    fields name, summary, involved_companies.company.name, platforms.name, cover.url;
    where name ~ "{game_name}";'''
    
    # Realiza la solicitud a la API
    response = requests.post(url, headers=headers, data=body)
    
    # Devuelve los datos del juego
    return response.json()


def borrar_comentario(indice):
    hoja.delete_row(indice)

# Imagen del encabezadoo
url_title = "https://i.imgur.com/xqohjCG.png"
st.markdown(f'<img src="{url_title}" alt="Encabezado" style="width: 100%;">',
            unsafe_allow_html=True)

# Si se introduce un nombre de juego, busca la información del juego
if game_name:
    game_info = get_game_info(game_name)
    
    # Verifica si game_info contiene algún elemento
    if game_info:
        # Muestra el nombre del juego en el centro en la parte superior
        st.write(f"<h1 style='text-align: center;'>{game_info[0]['name']}</h1>"
                 if 'name' in game_info[0] else "Nombre no disponible",
                 unsafe_allow_html=True)
        
        # Crea dos columnas para mostrar el cover y la información del juego
        col1, col2 = st.columns(2)
        
        # Muestra la portada del juego en la columna de la izquierda
        if 'cover' in game_info[0] and 'url' in game_info[0]['cover']:
            image_url = ('https://images.igdb.com/igdb/image/upload/t_cover_big/'
                         + game_info[0]['cover']['url'].split('/')[-1])
            col1.image(image_url, use_column_width=True)
        else:
            st.write("Imagen no disponible")

        # Muestra la información del juego en la columna de la derecha
        col2.write(f"**Sinopsis:** {game_info[0]['summary']}" if 'summary' in game_info[0] else "Sinopsis no disponible")
        col2.write(f"**Desarrollador:** {game_info[0]['involved_companies'][0]['company']['name']}" if 'involved_companies' in game_info[0] and game_info[0]['involved_companies'] else "Desarrollador no disponible")
        col2.write(f"**Plataformas:** {', '.join([platform['name'] for platform in game_info[0]['platforms']])}" if 'platforms' in game_info[0] and game_info[0]['platforms'] else "Plataformas no disponibles")

       
        # Se verifica si el usuario está logeado para que aparezca
        # la funcionalidad de calificar el juego
        if st.session_state['logged_in']:
             borrar = False
             new_rating = st.selectbox("Calificar este juego:", options=[0, 1, 2, 3, 4, 5])
             st.write(f"Has calificado {game_info[0]['name']} con {new_rating} ★")

            
             correos = hoja.col_values(2)
             juegos = hoja.col_values(3)
            
             comentado = False
             for i in range(1,len(correos)):
                if correos[i] == st.session_state.correo and juegos[i] == game_name:
                    comentado = True
            
             if comentado == False:
                # Crear el text area para los comentarios
                text_area = st.text_area("Comentario:", max_chars=100)
                if st.button("Enviar"):
                    nueva_fila = [text_area, st.session_state.correo, game_name]
                    hoja.append_row(nueva_fila)
                    st.success("¡Comentario realizado!")
               
                    
             else:
                st.write("Ya has escrito un comentario en este juego")
                st.write("Borralo, para poder escribir otro")
                if st.button("Borrar comentario"):
                    indice = 2
                    correos = hoja.col_values(2)  # Supongamos que los correos están en la columna A
                    juegos = hoja.col_values(3)  # Supongamos que los juegos están en la columna B
                        
                    for i in range(1, len(correos)):
                        if correos[i] == st.session_state.correo and juegos[i] == game_name:  
                            borrar_comentario(indice)
                            st.success("Has borrado tu comentario")
                            break
                        else:
                            indice += 1
        
    else:
        st.write("Lo siento, no pude encontrar ningún juego con ese nombre.")
