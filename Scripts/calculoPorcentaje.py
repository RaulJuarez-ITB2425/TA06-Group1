#Este código calcula el porcentaje de ocasiones en que el valor -999 aparece en todos los 
#archivos del directorio 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'

import re
import os

# Ruta al directorio con los archivos
ruta_directorio = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'

# Array para contener todos los valores
valores_totales = []

# Recorremos todos los archivos en el directorio
for archivo in os.listdir(ruta_directorio):
    ruta_archivo = os.path.join(ruta_directorio, archivo)

    # Verificamos que sea un archivo y no un directorio
    if os.path.isfile(ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            # Leemos el contenido del archivo
            contenido = archivo.read()
            # Usamos una expresión regular para encontrar solo los números
            valores = re.findall(r'-?\d+', contenido)
            valores_totales.extend(valores)

# Cuenta las ocurrencias de "-999"
ocurrencias_999 = valores_totales.count('-999')

# Calcula el porcentaje
total_valores = len(valores_totales)
porcentaje_999 = (ocurrencias_999 / total_valores) * 100

print(f'El valor "-999" aparece {ocurrencias_999} veces en el archivo.')
print(f'Esto representa el {porcentaje_999:.2f}% del total de valores.')