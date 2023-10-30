"""
Este modulo contiene las funciones para calcular la similitud entre
usuarios y entre juegos con la distancia del coseno.
Además, la función generar recomendaciones para juegos, donde se
utiliza la similitud entre juegos para obtener los 
datos de los juegos más parecidos entre si.
"""
import numpy as np
from scipy.spatial.distance import cosine


def calcular_similitud_juegos(data):
    """
    Calcula la matriz de similitud del coseno entre juegos
    a partir de una matriz de votos.

    Parameters:
    data (pd.DataFrame): Un DataFrame con los votos de los usuarios.

    Returns:
    np.ndarray: La matriz de similitud del coseno entre los juegos.
    """
    # Obtener la matriz de votos
    votos_matrix = data.to_numpy()

    # Calcular la matriz de similitud del coseno manualmente
    num_videojuegos = votos_matrix.shape[0]
    similarity_matrix = np.zeros((num_videojuegos, num_videojuegos))

    for i in range(num_videojuegos):
        for j in range(num_videojuegos):
            similarity_matrix[i, j] = 1 - cosine(votos_matrix[i, :], votos_matrix[j, :])

    return similarity_matrix


def calcular_similitud_usuarios(data):
    """
    Calcula la matriz de similitud del coseno entre usuarios
    a partir de una matriz de votos.

    Parameters:
    data (pd.DataFrame): Un DataFrame con los votos de los usuarios.

    Returns:
    np.ndarray: La matriz de similitud del coseno entre los usuarios.
    """
    # Obtener la matriz de votos
    votos_matrix = data.to_numpy()

    # Calcular la matriz de similitud del coseno manualmente
    num_usuarios = votos_matrix.shape[1]
    similarity_matrix = np.zeros((num_usuarios, num_usuarios))

    for i in range(num_usuarios):
        for j in range(num_usuarios):
            similarity_matrix[i, j] = 1 - cosine(votos_matrix[:, i], votos_matrix[:, j])

    return similarity_matrix
