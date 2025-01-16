import pandas as pd
import os
import logging

# Configurar el logging para registrar los errores
logging.basicConfig(filename='errores_lectura.log', level=logging.ERROR,
                    format='%(asctime)s - %(message)s')

# Ruta del directorio donde se encuentran los archivos .dat
directorio = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'  

# Lista todos los archivos .dat en el directorio
archivos = [f for f in os.listdir(directorio) if f.endswith('.dat')]

# Lista para almacenar los DataFrames leídos correctamente
dfs = []

# Contador para archivos leídos correctamente
archivos_leidos_correctamente = int(0)

# Iterar sobre los archivos y leerlos
for archivo in archivos:
    ruta_archivo = os.path.join(directorio, archivo)
    try:
        # Intentamos leer el archivo .dat
        df = pd.read_csv(ruta_archivo, delimiter='\t')  # Ajusta el delimitador según sea necesario
        dfs.append(df)
        archivos_leidos_correctamente += 1  # Incrementar el contador
    except Exception as e:
        # Si ocurre un error, lo registramos en el log
        logging.error(f"Error al leer el archivo {archivo}: {e}")

# Si deseas concatenar todos los DataFrames leídos correctamente:
if dfs:
    df_completo = pd.concat(dfs, ignore_index=True)
    print(f"Se leyeron correctamente {archivos_leidos_correctamente} archivos.")
else:
    print("No se leyeron archivos correctamente.")
