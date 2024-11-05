import pandas as pd
import requests
import os
import time

# Cargar el archivo CSV
file_path = r"D:\PROGRAMAS\PROGRAMAS\Python\recoleccion de txt PLABASE DB\PLaBAse - PLaBA-db.csv"
data = pd.read_csv(file_path)

# Directorio de destino para los archivos descargados
output_dir = r"D:\PROGRAMAS\PROGRAMAS\Python\recoleccion de txt PLABASE DB\txts"
os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta si no existe

# URL base para el enlace de descarga
base_url = "https://plabase.cs.uni-tuebingen.de/pb/database/PLaBA-db/PGPT_IMG-KEGG/KEGG_File/"

# Función para descargar el archivo txt de cada ID
def descargar_txt(img_sample_id):
    download_url = f"{base_url}{img_sample_id}_pfar_kegg.txt"
    response = requests.get(download_url)
    
    # Guarda el archivo si la respuesta es exitosa
    if response.status_code == 200:
        file_path = os.path.join(output_dir, f"{img_sample_id}_pfar_kegg.txt")
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Archivo {img_sample_id}_pfar_kegg.txt descargado exitosamente en {output_dir}.")
    else:
        print(f"Error al descargar el archivo para IMG SAMPLE ID {img_sample_id}")

# Iterar sobre cada ID en la columna 'IMG SAMPLE ID' del CSV
for img_sample_id in data['IMG SAMPLE ID']:
    descargar_txt(img_sample_id)
    time.sleep(1)  # Agrega un retraso para evitar sobrecargar el servidor
