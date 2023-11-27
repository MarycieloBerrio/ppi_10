"""
Este módulo genera toda la pantalla de inicio, además
de ser la página que streamlit lee por defecto para 
mostrar al usuario la aplicación
"""
# Importar las librerías requeridas
import json
import pandas as pd
import streamlit as st
from streamlit_image_select import image_select

# Configura el título y el favicon de la página
st.set_page_config(
    page_title="Gamer's Companion",
    page_icon="https://i.imgur.com/HaQOhdz.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Colores
#   Morado: 6b0b9b
#   Cyan: 21d4fd
#   Rosa: b81c99

# URL de la imagen del encabezado
url_title = "https://i.imgur.com/fdBE2Vx.png"
url_logo = "https://i.imgur.com/HaQOhdz.png"

# Crea una columna para centrar la imagen del logo
col1, col2, col3 = st.columns(3)
with col2:
    st.image(url_logo, use_column_width=True)

# Añade la imagen como encabezado de la aplicación de Streamlit
st.image(url_title)

# Cargar los datos desde el archivo CSV
df = pd.read_csv("Base_datos/juegos.csv")

# Comprobar si estamos en la página principal o de detalles
page = st.experimental_get_query_params().get('page', ['main'])[0]

if page == 'main':

    # Convertir cadenas JSON en diccionarios
    df['cover'] = df['cover'].apply(lambda x: json.loads(x.replace("'", '"'))
                                    if pd.notnull(x) else None)

    # Mostrar las imágenes como imágenes clicables
    clicked_index = image_select(
        label=" ",
        images=df['cover'].apply(lambda x: x['url'] if x and 'url' in x else None).tolist(),
        captions=df['name'].tolist(),
        return_value="index",
        use_container_width=False
    )

    st.write(clicked_index)

    # Redirigir a la página de detalles del juego
    if clicked_index:
        st.experimental_set_query_params(
            page='details', game_id=str(df.iloc[clicked_index]['id'])
        )

elif page == 'details':
    # Obtener el ID del juego desde la URL
    game_id = st.experimental_get_query_params().get('game_id', ['0'])[0]

    # Buscar el juego por ID en el DataFrame
    game_info = df[df['id'] == int(game_id)]

    if not game_info.empty:
        game_info = game_info.iloc[0]

        # Extraer la URL de la imagen del juego
        cover_info = game_info['cover']
        if isinstance(cover_info, str):
            # Si cover_info es una cadena, intentar cargarla como JSON
            try:
                cover_info = json.loads(cover_info.replace("'", '"'))
            except json.JSONDecodeError:
                # Si no se puede cargar como JSON, dejarla como una cadena
                cover_info = {'url': cover_info}

        # Obtener la URL de la imagen del juego
        cover_url = cover_info.get('url')

        # Agregar https: al principio de la URL
        if cover_url and not cover_url.startswith("https:"):
            cover_url = "https:" + cover_url

        # Mostrar la información detallada del juego
        st.title(game_info['name'])

        col1, col2 = st.columns(2)

        # Mostrar la imagen del juego
        if cover_url is not None:
            col1.image(cover_url, use_column_width=True)
        else:
            st.write("Imagen no disponible")

        col2.markdown(f"**Sinopsis:** {game_info['summary']}")
        col2.markdown(f"**Desarrollador:** {game_info['involved_companies']}")
        
        # Redondear total_rating a dos decimales
        rounded_rating = round(game_info['total_rating'], 2)
        
        # Mostrar el rating total con formato personalizado
        col2.markdown(f"<h3 style='color: #6b0b9b;'>Calificación: {rounded_rating}</h3>", 
                      unsafe_allow_html=True)

    else:
        st.write("Lo siento, no pude encontrar ningún juego con ese ID.")

    # Mostrar un botón "Volver" que llama a la función 'volver' cuando se hace clic
    if st.button('Volver', key='volver'):
        st.experimental_set_query_params(page='main', game_id='0')
            
# Información de los desarrolladores
developers = [
    {"name": "Juan Gabriel Goez Duque ", "email": "jgoezd@unal.edu.co"},
    {"name": "Jerónimo Vásquez Gónzalez ", "email": "jevasquez@unal.edu.co"},
    {"name": "Marycielo Berrio Zapata ", "email": "mberrioz@unal.edu.co"},
]

# Crea el HTML para el pie de página
footer_html = """
<footer style='width: 100%; background-color: #0c0c0c; padding: 20px 0; color: #6b0b9b;'>
<div style='max-width: 600px; margin: auto; text-align: left;'>
<h2 style='margin-bottom: 20px; color: #6b0b9b;'>Informacion de contacto</h2>
"""

for dev in developers:
    footer_html += f"<p style='margin-bottom: 10px;'><strong style='color: #6b0b9b;'>\
            {dev['name']}</strong>:<a href='mailto:{dev['email']}' style='color:\
            #21d4fd;'>{dev['email']}</a></p>"

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
