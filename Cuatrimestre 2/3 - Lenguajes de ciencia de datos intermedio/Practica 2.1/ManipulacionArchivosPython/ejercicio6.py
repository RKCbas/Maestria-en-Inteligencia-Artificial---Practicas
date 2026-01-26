import shutil
import os

# Nombres del archivo y directorio
archivo_a_mover = "archivo1.txt"
directorio_destino = "mi_directorio"

# Verificar si el archivo existe
if not os.path.exists(archivo_a_mover):
    print(f"✗ Error: El archivo '{archivo_a_mover}' no existe")
    print(f"Directorio actual: {os.getcwd()}")
elif not os.path.exists(directorio_destino):
    print(f"✗ Error: El directorio '{directorio_destino}' no existe")
    print("Debes crear el directorio primero")
else:
    # Construir la ruta de destino
    ruta_destino = os.path.join(directorio_destino, archivo_a_mover)
    
    # Mover el archivo
    shutil.move(archivo_a_mover, ruta_destino)
    print("✓ Archivo movido exitosamente:")
    print(f"  Origen: '{archivo_a_mover}'")
    print(f"  Destino: '{ruta_destino}'")