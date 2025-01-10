import pandas as pd

# Cargar el DataFrame desde un archivo CSV (ajusta la ruta del archivo según sea necesario)
df = pd.read_csv('/media/raul.juarez.7e8/PortableSSD/0.ASIX/MDS/TA06-Group1/precip.MIROC5.RCP60.2006-2100.SDSM_REJ/precip.P1.MIROC5.RCP60.2006-2100.REGRESION.dat')

# Seleccionar las columnas específicas
columns_to_check = ['precip', 'MIROC5', 'RCP60', '2006-2100', 'SDSM_REJ']

# Verificar si hay valores faltantes en las columnas seleccionadas
missing_values = df[columns_to_check].isnull().sum()

# Verificar si hay valores duplicados en las columnas seleccionadas
duplicate_values = df[columns_to_check].duplicated().sum()

# Verificar si hay inconsistencias (por ejemplo, valores fuera de un rango esperado)
# Aquí asumimos que los valores deben estar entre 0 y 100, ajusta según sea necesario
inconsistent_values = df[columns_to_check][(df[columns_to_check] < 0) | (df[columns_to_check] > 100)].count()
# Leer los datos de las columnas especificadas
data = df[columns_to_check]

# Imprimir los datos
print("\nDatos de las columnas seleccionadas:")
print(data)
print("Valores faltantes por columna:")
print(missing_values)
print("\nValores duplicados:")
print(duplicate_values)
print("\nValores inconsistentes:")
print(inconsistent_values)
