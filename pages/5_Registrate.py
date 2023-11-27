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
import streamlit.components.v1 as components
from streamlit_modal import Modal


# Configura el título y el favicon de la página
st.set_page_config(
    page_title="Gamer's Companion",
    page_icon="https://i.imgur.com/HaQOhdz.png",
)

# Título de la aplicación
url_title = "https://i.imgur.com/WPJInDQ.png"
st.markdown(f'<img src="{url_title}" alt="Encabezado" style="width: 100%;">',
            unsafe_allow_html=True)

# Realizar la conexión a google sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive.file"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de Google Sheets
hoja = client.open("Usuarios_bd").sheet1

# Obtener el número de usuarios actual
num_usuarios = len(hoja.get_all_records())

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

modal = Modal("Politica de tratamiento de datos", key="PTD")
modal.max_width = 500
if st.button("Politica de tratamiento de datos"):
   
    modal.open()
   
if modal.is_open():
    with modal.container():
        st.markdown("<span style=\"color:#000000\">En nuestra empresa, recolectamos datos relevantes con el consentimiento del usuario para mejorar nuestros servicios. Esta información puede incluir detalles personales como nombre o preferencias. Utilizamos estos datos para personalizar la experiencia del usuario y mejorar nuestros servicios, manteniendo la seguridad y protección de la información almacenada. Respetamos los derechos de los usuarios sobre sus datos, ofreciendo opciones para acceder, corregir o eliminar su información personal. Nunca compartimos datos personales con terceros sin consentimiento, a menos que sea requerido por ley. Esta política forma parte de nuestro compromiso con la privacidad y la seguridad de los datos de nuestros usuarios.</span>", unsafe_allow_html=True)

value = st.checkbox("Aceptar politica de tratamiento de datos")

if st.button("Registrar"):
    # Verificar si el correo ya existe en la hoja de Google Sheets
    valores = hoja.col_values(6)

    if correo in valores:
        usuario_existente = True
        st.error("El usuario ya se encuentra registrado.")
    else:

        if value:
            # Crear un diccionario con los datos del usuario
            usuario_id = num_usuarios + 1
            usuario = {
                "Nombre": nombre,
                "Apellido": apellido,
                "Fecha de Nacimiento": fecha_nacimiento.strftime("%Y-%m-%d"),
                "Género": genero,
                "Género de videojuego preferido": videojuego_preferido,
                "Correo": correo,
                "Contraseña": contrasena,
                "ID_Usuario": usuario_id

            }

            # Añadir una fila a la hoja de Google Sheets y registrar al usuario
            nueva_fila = [usuario["Nombre"], usuario["Apellido"], usuario["Fecha de Nacimiento"],
                            usuario["Género"], usuario["Género de videojuego preferido"],
                            usuario["Correo"], usuario["Contraseña"], usuario["ID_Usuario"]]
            hoja.append_row(nueva_fila)
            st.success("¡Registro exitoso!")

            value = False
        else:
            st.error("No has aceptado la politica de tratamiendo de datos")
       

