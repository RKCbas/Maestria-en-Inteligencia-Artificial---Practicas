import os

# Nombre del archivo original y nuevo nombre
archivo_original = "archivo1.txt"
archivo_nuevo = "archivo1_renombrado.txt"

# Verificar si el archivo existe antes de renombrarlo
if os.path.exists(archivo_original):
    # Renombrar el archivo
    os.rename(archivo_original, archivo_nuevo)
    print(f"✓ Archivo renombrado exitosamente: '{archivo_original}' → '{archivo_nuevo}'")
else:
    print(f"✗ Error: El archivo '{archivo_original}' no existe en el directorio actual")
    print(f"Directorio actual: {os.getcwd()}")