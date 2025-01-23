import os
import numpy as np
import pandas as pd
from scipy.stats import linregress

def calculate_annual_precipitation_trend(file_path):
    """
    Calcula la tendència de canvi anual de les precipitacions per un fitxer donat.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Processar les línies de dades
    data = []
    for line in lines[2:]:  # Saltar les dues primeres línies (capçalera i metadades)
        parts = line.split()
        year = int(parts[1])
        values = [float(x) for x in parts[3:] if x != '-999']  # Ignorar valors invàlids (-999)
        annual_precipitation = sum(values)
        data.append((year, annual_precipitation))

    # Crear un DataFrame
    df = pd.DataFrame(data, columns=['Year', 'AnnualPrecipitation'])

    # Agrupar per any i calcular la suma anual
    annual_data = df.groupby('Year').sum().reset_index()

    # Regresión lineal per calcular la taxa de canvi anual
    slope, intercept, r_value, p_value, std_err = linregress(annual_data['Year'], annual_data['AnnualPrecipitation'])

    return slope  # La taxa de canvi anual

def analyze_precipitation_folder(folder_path, output_csv):
    """
    Analitza tots els arxius d'una carpeta i calcula la tendència de canvi de les precipitacions.
    Desa els resultats en un fitxer CSV.
    """
    results = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.dat'):
            file_path = os.path.join(folder_path, file_name)
            trend = calculate_annual_precipitation_trend(file_path)
            results.append((file_name, trend))

    # Crear un DataFrame amb els resultats
    result_df = pd.DataFrame(results, columns=['FileName', 'AnnualPrecipitationTrend'])

    # Guardar els resultats en un fitxer CSV
    result_df.to_csv(output_csv, index=False)
    print(f"Resultats desats a: {output_csv}")

# Exemple d'execució
folder_path = '/home/eric.vicente.7e8/Baixades/precip.MIROC5.RCP60.2006-2100.SDSM_REJ/ArchivosDAT'  # Substituir pel camí a la carpeta amb els arxius
output_csv = 'resultats_precipitacions.csv'  # Nom del fitxer de sortida
analyze_precipitation_folder(folder_path, output_csv)

