import pandas as pd
import os
import logging

# Configurar el logging para registrar los errores
logging.basicConfig(filename='errores_lectura.log', level=logging.ERROR,
                    format='%(asctime)s - %(message)s')

# Ruta del directorio donde se encuentran los archivos .dat
directorio = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'  # Cambia esta ruta a la carpeta correspondiente

# Lista todos los archivos .dat en el directorio
archivos = [f for f in os.listdir(directorio) if f.endswith('.dat')]

# Lista para almacenar los DataFrames leídos correctamente
dfs = []

# Iterar sobre los archivos y leerlos
for archivo in archivos:
    ruta_archivo = os.path.join(directorio, archivo)
    try:
        # Intentamos leer el archivo .dat
        df = pd.read_csv(ruta_archivo, delimiter='\t')  # Ajusta el delimitador según sea necesario
        dfs.append(df)
    except Exception as e:
        # Si ocurre un error, lo registramos en el log
        logging.error(f"Error al leer el archivo {archivo}: {e}")

# Si deseas concatenar todos los DataFrames leídos correctamente:
if dfs:
    df_completo = pd.concat(dfs, ignore_index=True)
    print("Archivos leídos y concatenados correctamente.")
else:
    print("No se leyeron archivos correctamente.")
