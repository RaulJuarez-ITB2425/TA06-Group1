import pandas as pd
import os
import logging

# Configurar el logging para registrar los errores
logging.basicConfig(filename='errores_lectura.log', level=logging.ERROR,
                    format='%(asctime)s - %(message)s')

# Ruta del directorio donde se encuentran los archivos .dat
directorio = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ' 

# Verificar si el directorio existe
if not os.path.isdir(directorio):
    logging.error(f"El directorio '{directorio}' no existe.")
    print(f"El directorio '{directorio}' no existe.")
    exit(1)  # Detener la ejecución si el directorio no es válido

# Lista todos los archivos .dat en el directorio
archivos = [f for f in os.listdir(directorio) if f.endswith('.dat')]

# Verificar si hay archivos .dat
if not archivos:
    logging.error(f"No se encontraron archivos .dat en el directorio '{directorio}'.")
    print(f"No se encontraron archivos .dat en el directorio '{directorio}'.")
    exit(1)  # Detener si no hay archivos para procesar

# Lista para almacenar los DataFrames leídos correctamente
dfs = []

# Contador para archivos leídos correctamente
archivos_leidos_correctamente = 0

# Iterar sobre los archivos y leerlos
for archivo in archivos:
    ruta_archivo = os.path.join(directorio, archivo)
    try:
        # Intentamos leer el archivo .dat
        df = pd.read_csv(ruta_archivo, delimiter='\t')  # Ajusta el delimitador según sea necesario
        
        # Validar que el archivo tenga al menos algunas columnas
        if df.empty:
            raise ValueError(f"El archivo '{archivo}' está vacío.")
        
        # Si el archivo tiene valores incorrectos, también considerarlo un error
        if df.shape[1] < 2:
            raise ValueError(f"El archivo '{archivo}' tiene valores corruptos.")

        # Añadir el DataFrame a la lista
        dfs.append(df)
        archivos_leidos_correctamente += 1  # Incrementar el contador
    except pd.errors.ParserError as e:
        # Error relacionado con el parsing (por ejemplo, delimitador incorrecto)
        logging.error(f"Error de parsing en el archivo {archivo}: {e}")
    except ValueError as e:
        # Error relacionado con la validación de los datos (archivo vacío o columnas insuficientes)
        logging.error(f"Error en el archivo {archivo}: {e}")
    except UnicodeDecodeError as e:
        # Error relacionado con la codificación de caracteres
        logging.error(f"Error de codificación en el archivo {archivo}: {e}")
    except Exception as e:
        # Captura cualquier otro tipo de error
        logging.error(f"Error desconocido al leer el archivo {archivo}: {e}")

# Si se leyeron archivos correctamente, concatenar y guardar
if dfs:
    df_completo = pd.concat(dfs, ignore_index=True)
    df_completo.to_csv('datos_leidos.csv', index=False)
    print(f"Se leyeron correctamente {archivos_leidos_correctamente} archivos y se guardaron en 'datos_leidos.csv'.")
else:
    print("No se leyeron archivos correctamente.")
