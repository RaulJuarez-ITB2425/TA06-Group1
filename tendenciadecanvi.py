import os
import numpy as np
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt

def calculate_annual_precipitation_trend(file_path):
    """
    Calcula la tendència de canvi anual de les precipitacions per un fitxer donat en percentatge.
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

    # Calcular el canvi percentual respecte al valor mitjà
    mean_precipitation = annual_data['AnnualPrecipitation'].mean()

    if mean_precipitation == 0:
        print(f"Advertència: La mitjana de precipitacions és zero per l'arxiu {file_path}.")
        return 0

    percentage_change = (slope / mean_precipitation) * 100

    # Imprimir valors intermedis per depuració
    print(f"Fitxer: {file_path}")
    print(f"Mitjana de precipitacions: {mean_precipitation:.2f}")
    print(f"Pendents anuals (slope): {slope:.2f}")
    print(f"Canvi percentual anual: {percentage_change:.2f}%")

    return percentage_change  # La taxa de canvi anual en percentatge

def analyze_precipitation_folder(folder_path, output_csv):
    """
    Analitza tots els arxius d'una carpeta i calcula la tendència de canvi de les precipitacions.
    Desa els resultats en un fitxer CSV i genera un gràfic.
    També mostra la suma total de les tendències de canvi anuals.
    """
    results = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.dat'):
            file_path = os.path.join(folder_path, file_name)
            trend = calculate_annual_precipitation_trend(file_path)
            results.append((file_name, trend))

    # Crear un DataFrame amb els resultats
    result_df = pd.DataFrame(results, columns=['FileName', 'AnnualPrecipitationTrendPercentage'])

    # Guardar els resultats en un fitxer CSV
    result_df.to_csv(output_csv, index=False)
    print(f"Resultats desats a: {output_csv}")


    # Crear un gràfic sense noms dels arxius
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(result_df)), result_df['AnnualPrecipitationTrendPercentage'], color='skyblue')
    plt.xlabel('Index')
    plt.ylabel('Annual Precipitation Trend (%)')
    plt.title('Tendència de canvi anual de les precipitacions (%)')
    plt.tight_layout()
    plt.savefig('precipitation_trend_plot.png')  # Desa el gràfic com a imatge
    plt.show()

# Exemple d'execució
folder_path = '/home/eric.vicente.7e8/Baixades/precip.MIROC5.RCP60.2006-2100.SDSM_REJ/ArchivosDAT'  # Substituir pel camí a la carpeta amb els arxius
output_csv = 'resultats_precipitacions.csv'  # Nom del fitxer de sortida
analyze_precipitation_folder(folder_path, output_csv)
