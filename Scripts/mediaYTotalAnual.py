import os
import numpy as np
from collections import defaultdict

# Función para calcular la media y el total anual agrupando datos por año
def calcular_media_y_total_anual(archivo):
    precipitaciones_por_año = defaultdict(list)
    
    with open(archivo, 'r') as archivo:
        for linea_num, linea in enumerate(archivo, start=1):
            try:
                # Divide la línea en columnas
                columnas = linea.split()
                
                # Extrae el año (suponemos que está en la segunda columna, índice 1)
                año = int(columnas[1])  # Ajusta si el año está en otro índice
                
                # Ignora las primeras columnas no numéricas (ejemplo: P1, año, mes)
                datos = columnas[3:]  # Ajusta según el formato exacto
                
                # Convierte los valores en números flotantes
                valores = [float(x) for x in datos]
                
                # Filtra los valores ignorando los -999
                valores_filtrados = [v for v in valores if v != -999]
                
                # Agrega los valores válidos al año correspondiente
                if valores_filtrados:
                    precipitaciones_por_año[año].extend(valores_filtrados)
            except (ValueError, IndexError):
                # Ignorar líneas con formato incorrecto
                continue

    # Calcula la media y el total anual para cada año
    resultados_anuales = {
        año: {
            "media": np.mean(valores),
            "total": np.sum(valores)
        }
        for año, valores in precipitaciones_por_año.items()
    }
    return resultados_anuales

# Función principal para procesar todos los archivos en un directorio
def procesar_archivos_en_directorio(directorio, salida='resultados_medias_totales_anuales.txt'):
    resultados_totales = {}

    # Listar y ordenar los archivos por el número después de "P" en el nombre
    archivos = sorted(
        [archivo for archivo in os.listdir(directorio) if archivo.startswith('precip.')],
        key=lambda x: int(x.split('.')[1][1:])  # Extraer el número después de "P"
    )

    # Iterar sobre los archivos ordenados
    for archivo in archivos:
        ruta_completa = os.path.join(directorio, archivo)
        
        if os.path.isfile(ruta_completa):
            print(f"Procesando archivo: {archivo}")
            resultados_anuales = calcular_media_y_total_anual(ruta_completa)
            resultados_totales[archivo] = resultados_anuales

    # Guardar resultados en un archivo de salida
    with open(salida, 'w') as archivo_salida:
        for archivo, resultados in resultados_totales.items():
            archivo_salida.write(f"Archivo: {archivo}\n")
            for año, datos in sorted(resultados.items()):
                archivo_salida.write(
                    f"{año} --> Media anual: {datos['media']:.2f}, Total anual: {datos['total']:.2f}\n"
                )
            archivo_salida.write("\n")
    
    print(f"Resultados consolidados guardados en: {salida}")

# Ruta del directorio con los archivos
directorio_datos = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'

# Archivo de salida
archivo_salida = 'resultados_medias_totales_anuales.txt'

# Ejecutar el procesamiento
procesar_archivos_en_directorio(directorio_datos, archivo_salida)