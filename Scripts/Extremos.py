import re
import os
from collections import defaultdict

# Ruta al directorio con los archivos
ruta_directorio = 'precip.MIROC5.RCP60.2006-2100.SDSM_REJ'

# Diccionario para acumular precipitación total por año
precipitacion_anual = defaultdict(int)

# Procesar archivo línea por línea
def procesar_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        next(archivo)  # Saltar cabecera
        next(archivo)  # Saltar metadatos
        for linea in archivo:
            partes = linea.strip().split()
            year = int(partes[1])
            valores = [int(x) if x != '-999' else 0 for x in partes[3:]]
            precipitacion_anual[year] += sum(valores)

# Procesar todos los archivos
for archivo in os.listdir(ruta_directorio):
    ruta_archivo = os.path.join(ruta_directorio, archivo)
    if os.path.isfile(ruta_archivo):
        procesar_archivo(ruta_archivo)

# Determinar los años más pluviosos y más secos
max_precipitacion = max(precipitacion_anual.values())
min_precipitacion = min(precipitacion_anual.values())

años_mas_pluviosos = [year for year, total in precipitacion_anual.items() if total == max_precipitacion]
años_mas_secos = [year for year, total in precipitacion_anual.items() if total == min_precipitacion]

# Resultados
print("Años más pluviosos:")
for year in años_mas_pluviosos:
    print(f"{year}: {max_precipitacion} mm")

print("\nAños más secos:")
for year in años_mas_secos:
    print(f"{year}: {min_precipitacion} mm")
