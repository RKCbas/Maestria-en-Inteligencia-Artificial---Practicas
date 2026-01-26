import shutil
import os

# Nombres de los archivos
archivo_original = "archivo1.txt"
archivo_copia = "archivo1_copia.txt"

# Verificar si el archivo original existe
if os.path.exists(archivo_original):
    # Copiar el archivo
    shutil.copy(archivo_original, archivo_copia)
    print("✓ Archivo copiado exitosamente:")
    print(f"  Origen: '{archivo_original}'")
    print(f"  Destino: '{archivo_copia}'")
    
    # Mostrar el tamaño del archivo copiado
    tamaño = os.path.getsize(archivo_copia)
    print(f"  Tamaño: {tamaño} bytes")
else:
    print(f"✗ Error: El archivo '{archivo_original}' no existe en el directorio actual")
    print(f"Directorio actual: {os.getcwd()}")