# Importar las librerías requeridas
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Leer el archivo CSV con los datos de los juegos mejor valorados sin duplicados
df = pd.read_csv('Base_datos\juegos.csv')

# Realizar la conexión a google sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive.file"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Nombre de la hoja existente y creación de la nueva hoja
existing_spreadsheet = client.open('Usuarios_bd')
new_worksheet = existing_spreadsheet.add_worksheet(title='Info_Juegos', rows=1000, cols=6)  # Cambia las filas y columnas según sea necesario

# Leer el CSV con Pandas
df = pd.read_csv('Base_datos\juegos.csv')

# Convertir los NaN a 'NaN' (texto) en el DataFrame
df.fillna('NaN', inplace=True)

# Convertir el DataFrame a una lista de listas para subir a Google Sheets
data = df.values.tolist()

# Subir los datos a la nueva hoja de la hoja de cálculo existente
new_worksheet.update('A1', data)