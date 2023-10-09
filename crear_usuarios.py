"""
Módulo para generar usuarios aleatorios y exportarlos como archivo csv.
"""
import os
import pandas as pd
import faker

def generar_archivo_csv(df):
    """
    Transforma un dataframe de pandas en un archivo csv.
    Este lo genera en dónde se ejecuta el código.

    Args:
      df:Dataframe = Dataframe de pandas
    
    Returns:
    None
    """
    ruta_archivo = os.path.join(os.getcwd(), "usuarios.csv")
    df.to_csv(ruta_archivo)

# Generar 1000 usuarios aleatorios
def generar_usuarios(cantidad_usuarios:int) -> []:
    """
    Genera usuarios con información falsa sobre estos.

    Args:
    cantidad_usuarios:int = Cantidad de usuarios falsos a generar

    Returns:
    usuarios:[] = Lista con los usuarios falsos 
    """
    #  TODO: A estos usuarios falsos les falta tomar en cuenta los ratings
    #  de cada uno de los videojuegos. Agregar esta funcionalida
    fake = faker.Faker()

    usuarios = []

    for _ in range(cantidad_usuarios):
        usuario = {
          "nombre": fake.name(),
          "apellido": fake.last_name(),
          "correo": fake.email(),
          "contraseña": fake.password(),
      }
    usuarios.append(usuario)

    return usuarios

# Genero los usuarios falsos
usuarios_falsos = generar_usuarios(1000)
# Convertir los usuarios en un dataframe de pandas
df_usuarios = pd.DataFrame(usuarios_falsos)

# Generar el archivo CSV
generar_archivo_csv(df_usuarios)
