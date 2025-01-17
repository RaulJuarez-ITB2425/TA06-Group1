#Este código calcula el porcentaje de ocasiones en que el valor -999 aparece en un solo archivo.

import re

# Lee el archivo de texto
with open('precip.MIROC5.RCP60.2006-2100.SDSM_REJ/precip.P604.MIROC5.RCP60.2006-2100.REGRESION.dat', 'r') as archivo:
    contenido = archivo.read()

# Usa una expresión regular para encontrar solo los números
valores = re.findall(r'-?\d+', contenido)

# Cuenta las ocurrencias de "-999"
ocurrencias_999 = valores.count('-999')

# Calcula el porcentaje
total_valores = len(valores)
porcentaje_999 = (ocurrencias_999 / total_valores) * 100

print(f'El valor "-999" aparece {ocurrencias_999} veces en el archivo.')
print(f'Esto representa el {porcentaje_999:.2f}% del total de valores.')