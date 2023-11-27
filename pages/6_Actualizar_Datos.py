# Se importan las librerias requeridas
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit import session_state

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
st.title("Formulario de Cambio de Datos")
st.write("Solo se cambiaran los datos en los cuales las casillas\
         NO estén vacías")

def obtenerNumeroFila(data):
    """
    Encuentra el número de fila de un usuario en una hoja de Google Sheets.

    Parámetros:
    -data : hoja de google sheets a trabajar.

    Retorna:
    - int: el número de fila correspondiente al correo del usuario logeado
    """

    # Obtiene todos los datos de la hoja
    data = hoja.get_all_values()
    index = 2
    # Busca el numero de fila correspondiente al correo
    for row in data[1:]:
          
        if row[5] == st.session_state.correo:  
            return index
        else:
            index +=1  
if st.session_state['logged_in']:
    # Datos personales
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    genero = st.selectbox("Género", ["Femenino", "Masculino",
                                    "Prefiero no decirlo"])
    videojuego_preferido = st.selectbox("Género de Videojuego Preferido",
                                        ["Estrategia", "Acción", "Sci-fi",
                                        "Misterio", "Horror", "Aventura"])

    # Datos de acceso
    contrasena = st.text_input("Contraseña", type="password")

    # Se crea botón para actualizar
    if st.button("Actualizar datos"):
        
        # Se obtiene número de fila
        numero_fila = obtenerNumeroFila(st.session_state.correo)
        
        # Se verifica si las casillas están vacías
        if nombre != "":
            hoja.update_cell(numero_fila,1, nombre)
        
        if apellido != "":
            hoja.update_cell(numero_fila,2,apellido)
        
        hoja.update_cell(numero_fila, 4, genero)

        hoja.update_cell(numero_fila, 5, videojuego_preferido)

        if contrasena != "":
            
            hoja.update_cell(numero_fila, 7, contrasena)

        st.success("Se han actualizado tus datos correctamente!")

else:
    st.warning("Para actualizar tus datos debes iniciar sesión")
        
   
        