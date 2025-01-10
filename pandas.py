import pandas as pd

# Funció per llegir el fitxer .dat i gestionar errors de lectura
def carregar_fitxer(path):
    try:
        # Suponem que el fitxer .dat està delimitat per tabuladors
        df = pd.read_csv(path, sep='\t', encoding='utf-8')  # Si el delimitador no és tabulador, canvia sep a ',' o el que correspongui
        print(f"Fitxer {path} carregat correctament.")
        return df
    except Exception as e:
        print(f"Error en llegir el fitxer {path}: {e}")
        return None

# Funció per netejar les dades
def netejar_dades(df):
    # Verificar tipus de dades i convertir les columnes a tipus esperats
    try:
        # Suposem que hi ha una columna 'data' que hauria de ser de tipus datetime
        df['data'] = pd.to_datetime(df['data'], errors='coerce')  # Convertir a NaT si hi ha errors

        # Suposem que hi ha una columna 'preu' que hauria de ser numèrica
        df['preu'] = pd.to_numeric(df['preu'], errors='coerce')  # Convertir a NaN si hi ha errors

        print("Tipus de dades verificats i corregits.")
    except KeyError as e:
        print(f"Columna no trobada: {e}")
    
    # Gestionar valors nuls o inexistents
    print("Comprovant valors nuls...")
    print(df.isnull().sum())  # Mostrar la quantitat de valors nuls per cada columna

    # Eliminar files amb valors nuls
    df = df.dropna()  # Si volem eliminar files amb qualsevol NaN

    # Omplir els valors nuls de 'preu' amb la mitjana (si existeix la columna 'preu')
    if 'preu' in df.columns:
        df['preu'].fillna(df['preu'].mean(), inplace=True)

    print("Valors nuls gestionats.")

    # Filtrar valors atípics
    print("Comprovant valors atípics...")
    if 'preu' in df.columns:
        df = df[df['preu'] >= 0]  # Filtrar valors atípics per a 'preu' (excloure valors negatius)

    # Comprovant estadístiques descriptives de la columna 'preu'
    if 'preu' in df.columns:
        print(df['preu'].describe())

    return df

# Funció per guardar el fitxer netejat
def guardar_fitxer(df, path_nou):
    try:
        df.to_csv(path_nou, index=False, sep='\t', encoding='utf-8')  # Guardar el fitxer en format .dat (tabulador)
        print(f"Fitxer netejat guardat a {path_nou}.")
    except Exception as e:
        print(f"Error en guardar el fitxer netejat: {e}")

# Script principal
if __name__ == "__main__":
    path_fitxer = '/home/eric.vicente.7e8/Baixades/precip.MIROC5.RCP60.2006-2100.SDSM_REJ/precip.P24.MIROC5.RCP60.2006-2100.REGRESION.dat'  # Canvia per la ruta del teu fitxer .dat
    path_nou = 'dades_netejades2.dat'  # Nom del fitxer de sortida

    # Carregar el fitxer
    df = carregar_fitxer(path_fitxer)
    
    if df is not None:
        # Netejar les dades
        df_netejat = netejar_dades(df)

        # Guardar el fitxer netejat
        guardar_fitxer(df_netejat, path_nou)

