import streamlit as st

# Configura el título y el favicon de la página
st.set_page_config(
    page_title="Gamer's Companion",
    page_icon="https://i.imgur.com/HaQOhdz.png",
)

# Título de la aplicación
url_title = "https://i.imgur.com/yIp4W2Z.png"
st.markdown(f'<img src="{url_title}" alt="Encabezado" style="width: 100%;">',
            unsafe_allow_html=True)

# Se verifica si el usuario está logeado
if st.session_state['logged_in']:
    
    # Si está logeado aparece el botón para mostrar perfil
    # Se muestran las variables de estado creadas al logearse
    if st.button("Mostrar Perfil"):
        st.subheader("Perfil del Usuario")
        st.write(f"Nombre: {st.session_state.nombre}")
        st.write(f"Apellido: {st.session_state.apellido}")
        st.write(f"Género: {st.session_state.sexo}")
        st.write(f"Género Favorito: {st.session_state.generofav}")
        st.write(f"Correo Electrónico: {st.session_state.correo}")
        st.subheader("Juegos Calificados")
        st.write("0")  
        st.subheader("Juegos Finalizados")
        st.write("0")  
        st.write(f'Estado {st.session_state.logged_in}')

else:
    st.warning("Para ver tu perfil debes iniciar sesión")
