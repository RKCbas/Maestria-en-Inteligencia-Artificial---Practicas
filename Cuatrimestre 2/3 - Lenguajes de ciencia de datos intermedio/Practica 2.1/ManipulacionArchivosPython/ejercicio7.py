import os

# Nombre del archivo a verificar
archivo = "archivo1.txt"

# Obtener el directorio actual
directorio_actual = os.getcwd()

print(f"Verificando existencia del archivo '{archivo}'...")
print(f"Directorio actual: {directorio_actual}")
print("-" * 50)

# Verificar si el archivo existe
if os.path.exists(archivo):
    print(f"✓ El archivo '{archivo}' SÍ existe")
    
    # Información adicional del archivo
    ruta_completa = os.path.abspath(archivo)
    tamaño = os.path.getsize(archivo)
    
    print(f"  Ruta completa: {ruta_completa}")
    print(f"  Tamaño: {tamaño} bytes")
else:
    print(f"✗ El archivo '{archivo}' NO existe en el directorio actual")