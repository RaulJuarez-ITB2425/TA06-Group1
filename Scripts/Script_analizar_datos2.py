import os
from collections import defaultdict
import csv
import matplotlib.pyplot as plt

# Ruta al directorio con los archivos
ruta_directorio = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'

# Diccionarios para acumular datos
suma_mensual = defaultdict(lambda: [0]*12)
conteo_mensual = defaultdict(lambda: [0]*12)
max_sequias = defaultdict(int)

# Procesar archivo línea por línea
def procesar_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        next(archivo)  # Saltar cabecera
        next(archivo)  # Saltar metadatos
        sequia_actual = defaultdict(int)
        for linea in archivo:
            partes = linea.strip().split()
            year = int(partes[1])
            month = int(partes[2])
            valores = [int(x) if x != '-999' else 0 for x in partes[3:]]
            
            # Actualizar suma y conteo mensual
            suma_mensual[year][month - 1] += sum(valores)
            conteo_mensual[year][month - 1] += len(valores)
            
            # Calcular duración de sequía
            for precip in valores:
                if precip == 0:
                    sequia_actual[year] += 1
                    max_sequias[year] = max(max_sequias[year], sequia_actual[year])
                else:
                    sequia_actual[year] = 0

# Procesar todos los archivos
for archivo in os.listdir(ruta_directorio):
    ruta_archivo = os.path.join(ruta_directorio, archivo)
    if os.path.isfile(ruta_archivo):
        procesar_archivo(ruta_archivo)

# Calcular índice de estacionalidad
print("Índice de estacionalidad por año:")
for year in sorted(suma_mensual.keys()):
    medias_mensuales = [suma / conteo if conteo != 0 else 0 
                        for suma, conteo in zip(suma_mensual[year], conteo_mensual[year])]
    media_anual = sum(medias_mensuales) / 12
    indice_estacionalidad = sum(abs(m - media_anual) for m in medias_mensuales) / 12
    print(f"{year}: {indice_estacionalidad:.2f}")

# Duración máxima de sequías
print("\nMáxima duración de sequías por año:")
for year in sorted(max_sequias.keys()):
    print(f"{year}: {max_sequias[year]} días")

# Crear el archivo CSV con el índice de estacionalidad y duración de sequías
with open('resumen_estadistico.csv', 'w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['Año', 'Índice de Estacionalidad', 'Duración Máxima de Sequías (días)'])
    
    # Escribir los resúmenes para cada año
    for year in sorted(suma_mensual.keys()):
        medias_mensuales = [suma / conteo if conteo != 0 else 0 
                            for suma, conteo in zip(suma_mensual[year], conteo_mensual[year])]
        media_anual = sum(medias_mensuales) / 12
        indice_estacionalidad = sum(abs(m - media_anual) for m in medias_mensuales) / 12
        duracion_sequia = max_sequias.get(year, 0)
        
        writer.writerow([year, round(indice_estacionalidad, 2), duracion_sequia])

# Crear el gráfico de estacionalidad
indices_estacionalidad = []
años = sorted(suma_mensual.keys())

for year in años:
    medias_mensuales = [suma / conteo if conteo != 0 else 0 
                        for suma, conteo in zip(suma_mensual[year], conteo_mensual[year])]
    media_anual = sum(medias_mensuales) / 12
    indice_estacionalidad = sum(abs(m - media_anual) for m in medias_mensuales) / 12
    indices_estacionalidad.append(indice_estacionalidad)

plt.figure(figsize=(10, 6))
plt.bar(años, indices_estacionalidad, color='skyblue')
plt.xlabel('Año')
plt.ylabel('Índice de Estacionalidad')
plt.title('Índice de Estacionalidad por Año')
plt.xticks(rotation=45)
plt.tight_layout()

# Guardar el gráfico de estacionalidad como imagen
plt.savefig('indice_estacionalidad.png')

# Crear el gráfico de la duración máxima de las sequías
duracion_sequias = [max_sequias.get(year, 0) for year in años]

plt.figure(figsize=(10, 6))
plt.plot(años, duracion_sequias, marker='o', color='red')
plt.xlabel('Año')
plt.ylabel('Duración Máxima de Sequías (días)')
plt.title('Duración Máxima de Sequías por Año')
plt.xticks(rotation=45)
plt.tight_layout()

# Guardar el gráfico de duración de sequías como imagen
plt.savefig('duracion_sequias.png')

# Mostrar los gráficos
plt.show()
