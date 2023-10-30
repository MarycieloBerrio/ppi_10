"""
Este módulo genera toda la pantalla de inicio, además
de ser la página que streamlit lee por defecto para 
mostrar al usuario la aplicación
"""

# Importar librerias requeridas
import json
import requests
import streamlit as st
from st_clickable_images import clickable_images

# Configura el título y el favicon de la página
st.set_page_config(
    page_title="Gamer's Companion",
    page_icon="🎮",
    initial_sidebar_state="collapsed"
)

def local_css(file_name):
    """
    Carga un documento css y lo renderiza en la página.

    Parameters:
    file_name: Nombre del archivo a renderizar

    Returns:
    None.
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Llama a local_css con el nombre del archivo CSS
local_css("style.css")

# URL de la imagen del encabezado
url_imagen = "https://i.imgur.com/qQH31fg.png?1"

# Añade la imagen como encabezado de la aplicación de Streamlit
st.image(url_imagen)

# URL y credenciales para la API de IGDB
URL = "https://api.igdb.com/v4/games"
HEADERS = {
    'Client-ID': 'ju1vfy05jqstzoclqv1cs2hsomw1au',
    'Authorization': 'Bearer 8h1ymcezojqdpcvmz5fvwxal2myoxp',
}

# Parámetros de la consulta a la API de IGDB
BODY = 'fields id,name,cover.url; limit 100; sort rating desc;\
        where rating > 70; where rating_count > 1000;'

response = requests.post(URL, headers=HEADERS, data=BODY)

# Comprueba si la solicitud fue exitosa
if response.status_code == 200:
    # Convierte la respuesta en JSON
    games = json.loads(response.text)

    # Contador para llevar un registro de cuántos juegos se han mostrado
    count = 0

    query_params = st.experimental_get_query_params().keys()
    if 'page' not in query_params:
        st.experimental_set_query_params(
       
            page = 'main'
        )

    if st.experimental_get_query_params()['page'][0] == 'main':
        image_urls = []
        game_ids = []
        for i, game in enumerate(games):
            if 'cover' in game and count < 50:
                image_url = game['cover']['url'].replace('t_thumb', 't_cover_big')
                image_url = 'https:' + image_url

                # Incrementa el contador
                count += 1

                # Añade la URL de la imagen y el ID del juego a las listas
                image_urls.append(image_url)
                game_ids.append(game['id'])

        # Muestra las imágenes como imágenes clicables
        clicked = clickable_images(image_urls, key='games')

        # Si se hace clic en una imagen, redirige a la página de detalles del juego
        if clicked > -1:
            st.experimental_set_query_params(page='details', game_id=game_ids[clicked])

    elif st.experimental_get_query_params()['page'][0] == 'details':
        game_id = st.experimental_get_query_params()['game_id'][0]

        # Define la consulta para buscar el juego por ID
        body = f'fields name, summary, involved_companies.company.name,\
                platforms.name, cover.url; where id = {game_id};'

        # Realiza la solicitud a la API
        response = requests.post(URL, headers=HEADERS, data=body)

        # Obtiene los detalles del juego en formato JSON
        game_info = response.json()

        # Verifica si se obtuvo alguna información del juego
        if game_info:
            # Muestra el nombre del juego como título de la página
            st.title(game_info[0]['name'])

            # Crea dos columnas para mostrar la imagen y la información del juego
            col1, col2 = st.columns(2)

            # Muestra la imagen del juego en la columna de la izquierda
            if 'cover' in game_info[0] and 'url' in game_info[0]['cover']:
                image_url = ('https://images.igdb.com/igdb/image/upload/t_cover_big/'
                            + game_info[0]['cover']['url'].split('/')[-1])
                col1.image(image_url, use_column_width=True)
            else:
                st.write("Imagen no disponible")

            # Muestra la información del juego en la columna de la derecha
            col2.markdown(f"**Sinopsis:** {game_info[0]['summary']}")
            col2.markdown(f"**Desarrollador:** \
                            {game_info[0]['involved_companies'][0]['company']['name']}")
            col2.markdown(f"**Plataformas:** \
                            {', '.join([platform['name'] for platform in game_info[0]['platforms']])}")
        else:
            st.write("Lo siento, no pude encontrar ningún juego con ese ID.")
        
        # Muestra un botón "Volver" que llama a la función 'volver' cuando se hace clic
        if st.button('Volver', key='volver'):
            st.experimental_set_query_params(page='main')
            
# Información de los desarrolladores
developers = [
    {"name": "Juan Gabriel Goez Duque ", "email": "jgoezd@unal.edu.co"},
    {"name": "Jerónimo Vásquez Gónzalez ", "email": "jevasquez@unal.edu.co"},
    {"name": "Marycielo Berrio Zapata ", "email": "mberrioz@unal.edu.co"},
]

# Crea el HTML para el pie de página
footer_html = """
<footer style='width: 100%; background-color: #333; padding: 20px 0; color: #fff;'>
    <div style='max-width: 600px; margin: auto; text-align: left;'>
        <h2 style='margin-bottom: 20px; color: #fff;'>Informacion de contacto</h2>
"""

for dev in developers:
    footer_html += f"<p style='margin-bottom: 10px;'><strong style='color: #fff;'>\
                {dev['name']}</strong>:<a href='mailto:{dev['email']}' style='color:\
                #fff;'>{dev['email']}</a></p>"

footer_html += """
    </div>
</footer>
"""

# Agrega un espacio en blanco al final de la página antes del pie de página
st.write("<br/><br/><br/><br/>", unsafe_allow_html=True)

# Muestra el pie de página en Streamlit
st.markdown(footer_html, unsafe_allow_html=True)

# Se crea un contador para la sesión de estado
if 'count' not in st.session_state:
    st.session_state.count = 0

# Se crea la variable logged_in si es la primera vez
# que ingresa
if st.session_state.count == 0:
    st.session_state.logged_in = False

# Se actualiza el contador para mantener el valor
# de logged_in entre paginas
st.session_state.count += 1

