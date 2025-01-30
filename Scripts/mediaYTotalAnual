import os
import csv
import numpy as np
import matplotlib.pyplot as plt
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

# Función principal para procesar archivos, guardar en CSV y generar gráficos
def procesar_archivos_en_directorio(directorio, salida='resultados_medias_totales_anuales.csv'):
    resultados_totales = []
    consolidado_anual = defaultdict(lambda: {"total": 0, "media_suma": 0, "conteo": 0})

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
            
            # Agregar resultados al total consolidado
            for año, datos in sorted(resultados_anuales.items()):
                # Para CSV
                resultados_totales.append({
                    "Archivo": archivo,
                    "Año": año,
                    "Media Anual": datos["media"],
                    "Total Anual": datos["total"]
                })

                # Para el consolidado anual
                consolidado_anual[año]["total"] += datos["total"]
                consolidado_anual[año]["media_suma"] += datos["media"]
                consolidado_anual[año]["conteo"] += 1

    # Guardar los resultados consolidados en un archivo CSV
    with open(salida, 'w', newline='') as archivo_csv:
        campos = ["Archivo", "Año", "Media Anual", "Total Anual"]
        escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
        
        escritor.writeheader()
        escritor.writerows(resultados_totales)

    print(f"Resultados consolidados guardados en: {salida}")

    # Calcular medias consolidadas por año
    medias_consolidadas = {año: datos["media_suma"] / datos["conteo"] for año, datos in consolidado_anual.items()}
    totales_consolidados = {año: datos["total"] for año, datos in consolidado_anual.items()}

    # Imprimir en terminal la media y el total anual general
    print("\nMedia y Total Anual Consolidados:")
    for año in sorted(medias_consolidadas.keys()):
        print(f"Año {año}: Media consolidada = {medias_consolidadas[año]:.2f}, Total consolidado = {totales_consolidados[año]:.2f}")

    # Generar los gráficos por separado
    generar_graficos_separados(medias_consolidadas, totales_consolidados)

# Nueva función para generar gráficos separados
def generar_graficos_separados(medias_consolidadas, totales_consolidados):
    años = sorted(medias_consolidadas.keys())
    medias = [medias_consolidadas[año] for año in años]
    totales = [totales_consolidados[año] for año in años]

    # **Gráfico de Media Anual**
    plt.figure(figsize=(10, 6))
    plt.plot(años, medias, label='Media Anual', marker='o', color='blue')
    plt.title('Media Anual de Precipitaciones (Consolidado)')
    plt.xlabel('Año')
    plt.ylabel('Media de Precipitaciones')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('media_anual.png')
    plt.show()
    plt.close()

    # **Gráfico de Total Anual** (se muestra al cerrar el grafico anterior)
    plt.figure(figsize=(10, 6))
    plt.plot(años, totales, label='Total Anual', marker='s', color='green')
    plt.title('Total Anual de Precipitaciones (Consolidado)')
    plt.xlabel('Año')
    plt.ylabel('Total de Precipitaciones')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('total_anual.png')
    plt.show()
    plt.close()

# Ruta del directorio con los archivos
directorio_datos = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'

# Archivo de salida
archivo_salida = 'resultados_medias_totales_anuales.csv'

# Ejecutar el procesamiento
procesar_archivos_en_directorio(directorio_datos, archivo_salida)
