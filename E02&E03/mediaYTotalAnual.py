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
                columnas = linea.split()
                año = int(columnas[1])  # Ajustar si el año está en otro índice
                datos = columnas[3:]  # Ajusta según el formato exacto del archivo
                
                valores = [float(x) for x in datos if float(x) != -999]  # Filtra valores inválidos
                if valores:
                    precipitaciones_por_año[año].extend(valores)
            except (ValueError, IndexError):
                continue  # Ignorar líneas con formato incorrecto

    resultados_anuales = {
        año: {"media": np.mean(valores), "total": np.sum(valores)}
        for año, valores in precipitaciones_por_año.items()
    }
    
    return resultados_anuales, precipitaciones_por_año  # Devolver ambos

# Función principal para procesar archivos, guardar en CSV y generar gráficos
def procesar_archivos_en_directorio(directorio, salida='resultados_medias_totales_anuales.csv'):
    resultados_totales = []
    consolidado_anual = defaultdict(lambda: {"suma_precipitaciones": 0, "media_suma": 0, "conteo_datos": 0})

    archivos = sorted(
        [archivo for archivo in os.listdir(directorio) if archivo.startswith('precip.')],
        key=lambda x: int(x.split('.')[1][1:])  # Extraer el número después de "P"
    )

    for archivo in archivos:
        ruta_completa = os.path.join(directorio, archivo)
        if os.path.isfile(ruta_completa):
            print(f"Procesando archivo: {archivo}")
            resultados_anuales, precipitaciones_por_año = calcular_media_y_total_anual(ruta_completa)  # Ahora devuelve dos valores

            for año, datos in sorted(resultados_anuales.items()):
                resultados_totales.append({
                    "Archivo": archivo, "Año": año,
                    "Media Anual": datos["media"], "Total Anual": datos["total"]
                })

                # Consolidar datos por año
                consolidado_anual[año]["suma_precipitaciones"] += datos["total"]
                consolidado_anual[año]["media_suma"] += datos["media"]
                consolidado_anual[año]["conteo_datos"] += len(precipitaciones_por_año[año])  # Ahora sí está definido

    # Guardar resultados en CSV
    with open(salida, 'w', newline='') as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=["Archivo", "Año", "Media Anual", "Total Anual"])
        escritor.writeheader()
        escritor.writerows(resultados_totales)

    print(f"Resultados guardados en: {salida}")

    # Calcular medias consolidadas correctamente
    medias_consolidadas = {año: datos["media_suma"] / datos["conteo_datos"] for año, datos in consolidado_anual.items()}
    totales_consolidados = {año: datos["suma_precipitaciones"] for año, datos in consolidado_anual.items()}

    # Imprimir valores consolidados para verificar
    print("\nMedia y Total Anual Consolidados:")
    for año in sorted(medias_consolidadas.keys()):
        print(f"Año {año}: Media consolidada = {medias_consolidadas[año]:.2f}, Total consolidado = {totales_consolidados[año]:.2f}")

    # Generar gráficos separados
    generar_graficos_separados(medias_consolidadas, totales_consolidados)

# Función corregida para generar gráficos
def generar_graficos_separados(medias_consolidadas, totales_consolidados):
    años = sorted(totales_consolidados.keys())
    medias = [medias_consolidadas[año] for año in años]
    totales = [totales_consolidados[año] for año in años]

    # --- Gráfico de Media Anual ---
    plt.figure(figsize=(10, 6))
    plt.plot(años, medias, marker='o', color='blue', linestyle='-', label='Media Anual')
    plt.title('Media Anual de Precipitaciones')
    plt.xlabel('Año')
    plt.ylabel('Media de Precipitaciones')
    plt.legend()
    plt.grid(True)
    plt.ylim(min(medias) * 0.9, max(medias) * 1.1)  # Ajustar límites del eje Y
    plt.tight_layout()
    plt.savefig('media_anual.png')
    plt.show()

    # --- Gráfico de Total Anual ---
    plt.figure(figsize=(10, 6))
    plt.plot(años, totales, marker='s', color='green', linestyle='-', label='Total Anual')
    plt.title('Total Anual de Precipitaciones')
    plt.xlabel('Año')
    plt.ylabel('Total de Precipitaciones')
    plt.legend()
    plt.grid(True)

    # 🔹 Ajustar eje Y para que refleje correctamente los valores
    plt.ylim(min(totales) * 0.9, max(totales) * 1.1)  # Asegurar escala correcta
    plt.ticklabel_format(style='plain', axis='y')  # Evita notación científica
    plt.tight_layout()
    plt.savefig('total_anual.png')
    plt.show()

# Ejecutar el procesamiento
directorio_datos = 'E01\precip.MIROC5.RCP60.2006-2100.SDSM_REJ'
archivo_salida = 'resultados_medias_totales_anuales.csv'
procesar_archivos_en_directorio(directorio_datos, archivo_salida)
