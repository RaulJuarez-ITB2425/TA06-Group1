import csv

# Funció per identificar el delimitador més comú
def identificar_delimitador(linia):
    delimitadors = [',', ';', '\t', ' ', '|']
    comptadors = {delim: linia.count(delim) for delim in delimitadors}
    delimitador_comun = max(comptadors, key=comptadors.get)
    return delimitador_comun

# Funció per llegir les primeres files de l'arxiu .dat i identificar columnes i delimitador
def analitzar_arxiu(arxiu):
    try:
        with open(arxiu, 'r', encoding='utf-8') as f:
            primeres_files = [f.readline() for _ in range(5)]  # Llegeix les primeres 5 files
            # Trobar el delimitador més comú en les primeres línies
            delimitador = identificar_delimitador(primeres_files[0])
            
            # Intentar llegir les dades amb el delimitador identificat
            csv_reader = csv.reader(primeres_files, delimiter=delimitador)
            num_columnes = len(next(csv_reader))  # Nombre de columnes a partir de la primera línia

            return num_columnes, delimitador
    except Exception as e:
        print(f"Error en llegir l'arxiu {arxiu}: {e}")
        return None, None

# Exemple d'ús
arxiu = '/home/eric.vicente.7e8/Baixades/precip.MIROC5.RCP60.2006-2100.SDSM_REJ/precip.P3.MIROC5.RCP60.2006-2100.REGRESION.dat'  # Posa el camí correcte del teu arxiu .dat
columnes, delimitador = analitzar_arxiu(arxiu)
if columnes is not None:
    print(f"Nombre de columnes: {columnes}")
    print(f"Delimitador utilitzat: '{delimitador}'")
