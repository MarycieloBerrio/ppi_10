import streamlit as st
import pandas as pd

# Crear un DataFrame de ejemplo con información de películas
data = {
    'nombre': ['Pelicula 1', 'Pelicula 2', 'Pelicula 3', 'Otra Pelicula 1'],
    'imagen': ['https://url_imagen1.com', 'https://url_imagen2.com', 'https://url_imagen3.com', 'https://url_imagen4.com'],
    'calificacion': [0, 0, 0, 0]
}

df = pd.DataFrame(data)

# Función para mostrar la información de una película y permitir calificarla
def rate_movie(movie_name, idx):
    movie = df[df['nombre'] == movie_name].iloc[0]
    st.subheader(movie['nombre'])
    st.image(movie['imagen'], caption=movie['nombre'], use_column_width=True)
    
    st.write("Calificación actual:")
    st.write(f"{movie['calificacion']} ★")

    new_rating = st.selectbox(f"Calificar esta película {idx}:", options=[0, 1, 2, 3, 4, 5])
    st.write(f"Has calificado {movie['nombre']} con {new_rating} ★")

    # Actualizar la calificación en el DataFrame
    df.loc[df['nombre'] == movie_name, 'calificacion'] = new_rating

# Encabezado de la aplicación
st.title("Buscador de Películas con Calificación")

# Barra de búsqueda
movie_name = st.text_input("Buscar película por nombre")

# Filtrar el DataFrame según la búsqueda
if movie_name:
    filtered_movies = df[df['nombre'].str.contains(movie_name, case=False, na=False)]
    if not filtered_movies.empty:
        for idx, movie in filtered_movies.iterrows():
            rate_movie(movie['nombre'], idx)
    else:
        st.write("No se encontraron películas que coincidan con la búsqueda.")