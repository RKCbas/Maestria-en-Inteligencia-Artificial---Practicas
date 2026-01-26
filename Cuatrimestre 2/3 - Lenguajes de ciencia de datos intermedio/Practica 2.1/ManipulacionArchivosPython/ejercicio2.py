import os

# Nombre del archivo a eliminar
archivo_a_eliminar = "archivo2.txt"

# Verificar si el archivo existe antes de eliminarlo
if os.path.exists(archivo_a_eliminar):
    # Eliminar el archivo
    os.remove(archivo_a_eliminar)
    print(f"✓ Archivo eliminado exitosamente: '{archivo_a_eliminar}'")
else:
    print(f"✗ Error: El archivo '{archivo_a_eliminar}' no existe en el directorio actual")
    print(f"Directorio actual: {os.getcwd()}")