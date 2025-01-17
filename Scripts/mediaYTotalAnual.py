import numpy as np
from collections import defaultdict

# Función para calcular la media anual agrupando datos por año
def calcular_media_anual(archivo):
    precipitaciones_por_año = defaultdict(list)
    
    with open(archivo, 'r') as archivo:
        for linea_num, linea in enumerate(archivo, start=1):
            # Ignorar encabezados o líneas inválidas
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
            except ValueError:
                continue

    # Calcula la media anual para cada año
    medias_anuales = {año: np.mean(valores) for año, valores in precipitaciones_por_año.items()}
    return medias_anuales

# Ruta del archivo
ruta_archivo = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ/precip.P1.MIROC5.RCP60.2006-2100.REGRESION.dat'

# Cálculo de la media anual
medias_anuales = calcular_media_anual(ruta_archivo)

# Verifica si se generaron resultados
primer_año = 2006
ultimo_año = 2100

if medias_anuales:
    print("\nResultados:")
    for año in range(primer_año, ultimo_año + 1):
        if año in medias_anuales:
            print(f"Año {año}: Media anual de precipitaciones: {medias_anuales[año]:.2f}")
        else:
            print(f"Año {año}: No se encontraron datos válidos.")
else:
    print("No se encontraron datos válidos para calcular medias anuales.")
