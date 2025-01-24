import re
import os
import csv
import matplotlib.pyplot as plt

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
porcentaje_otros = 100 - porcentaje_999

# Crear el gráfico de pastel
etiquetas = ['-999', 'Otros valores']
tamaños = [porcentaje_999, porcentaje_otros]
colores = ['red', 'lightblue']

plt.figure(figsize=(6, 6))
plt.pie(tamaños, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores)
plt.title('Porcentaje de "-999" frente a otros valores')
plt.axis('equal')  # Asegura que el gráfico sea un círculo perfecto
plt.show()

# Guardar los resultados en un archivo CSV
ruta_csv = 'resultados.csv'
with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    # Escribir encabezados
    escritor_csv.writerow(['Ocurrencias de -999', 'Porcentaje'])
    # Escribir resultados
    escritor_csv.writerow([ocurrencias_999, f'{porcentaje_999:.2f}'])

print(f'El valor "-999" aparece {ocurrencias_999} veces en el archivo.')
print(f'Esto representa el {porcentaje_999:.2f}% del total de valores.')
print(f'Los resultados se han guardado en el archivo {ruta_csv}.')
