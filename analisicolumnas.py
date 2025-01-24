import os
import csv

# Funció per identificar el delimitador més comú
def identificar_delimitador(linia):
    delimitadors = [',', ';', '\t', ' ', '|']
    comptadors = {delim: linia.count(delim) for delim in delimitadors}
    delimitador_comun = max(comptadors, key=comptadors.get)
    return delimitador_comun

# Funció per llegir les primeres files d'un arxiu .dat i identificar columnes i delimitador
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

# Funció per analitzar tots els arxius .dat en una carpeta de manera recursiva i guardar els resultats en un fitxer
def analitzar_carpeta(carpeta, fitxer_sortida):
    with open(fitxer_sortida, 'w', encoding='utf-8') as sortida:
        sortida.write("Arxiu,Nombre de columnes,Delimitador\n")  # Capçalera del fitxer CSV
        for root, _, files in os.walk(carpeta):
            for file in files:
                if file.endswith('.dat'):
                    ruta_arxiu = os.path.join(root, file)
                    print(f"Analitzant: {ruta_arxiu}")
                    columnes, delimitador = analitzar_arxiu(ruta_arxiu)
                    if columnes is not None:
                        sortida.write(f"{ruta_arxiu},{columnes},'{delimitador}'\n")

# Exemple d'ús
carpeta = '/home/eric.vicente.7e8/Baixades/precip.MIROC5.RCP60.2006-2100.SDSM_REJ/ArchivosDAT/'  # Posa el camí correcte de la carpeta
fitxer_sortida = 'resultats_analisi3.csv'
analitzar_carpeta(carpeta, fitxer_sortida)

print(f"Resultats desats a {fitxer_sortida}")
