import os
from collections import defaultdict

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